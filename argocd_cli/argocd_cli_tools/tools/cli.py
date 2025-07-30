from kubiya_sdk.tools import Arg
from .base import ArgoCDCLITool
from kubiya_sdk.tools.registry import tool_registry

argocd_cli_tool = ArgoCDCLITool(
    name="argocd_cli_command",
    description="Execute any ArgoCD CLI command",
    content="""
    #!/bin/bash
    set -e

    # Validate required parameters
    if [ -z "$command" ]; then
        echo "Error: Command is required"
        exit 1
    fi
    
    # Strip protocol from server URL if present
    SERVER_URL="${ARGOCD_SERVER#https://}"
    SERVER_URL="${SERVER_URL#http://}"
    
    echo "Executing: argocd $command"
    echo "Server: $SERVER_URL"
    echo ""
    
    # Execute the command directly (no explicit login needed with auth token)
    argocd $command --server "$SERVER_URL" --auth-token "$ARGOCD_AUTH_TOKEN" --grpc-web --insecure
    """,
    args=[
        Arg(
            name="command", 
            type="str", 
            description="The command to pass to the ArgoCD CLI (e.g., 'app list', 'project create my-project')",
            required=True
        ),
    ],
    image="argoproj/argocd:latest"
)

# ArgoCD App Get Tool - automatically prepends "argocd/" to application names
argocd_app_get_tool = ArgoCDCLITool(
    name="argocd_app_get",
    description="Get detailed information about a specific ArgoCD application (automatically prepends 'argocd/' to app name)",
    content="""
    #!/bin/bash
    set -e

    # Validate required parameters
    if [ -z "$app_name" ]; then
        echo "Error: Application name is required"
        exit 1
    fi
    
    # Strip protocol from server URL if present
    SERVER_URL="${ARGOCD_SERVER#https://}"
    SERVER_URL="${SERVER_URL#http://}"
    
    # Automatically prepend "argocd/" to the application name
    FULL_APP_NAME="argocd/$app_name"
    
    echo "Getting application details for: $FULL_APP_NAME"
    echo "Server: $SERVER_URL"
    echo "Executing: argocd app get \"$FULL_APP_NAME\" --server \"$SERVER_URL\" --auth-token \"$ARGOCD_AUTH_TOKEN\" --grpc-web --insecure"
    echo ""
    
    # Execute the app get command with the prefixed name
    argocd app get "$FULL_APP_NAME" --server "$SERVER_URL" --auth-token "$ARGOCD_AUTH_TOKEN" --grpc-web --insecure
    """,
    args=[
        Arg(
            name="app_name", 
            type="str", 
            description="The application name (without 'argocd/' prefix - it will be added automatically)",
            required=True
        ),
    ],
    image="argoproj/argocd:latest"
)

# ArgoCD App List Tool - supports grep filtering
argocd_app_list_tool = ArgoCDCLITool(
    name="argocd_app_list",
    description="List ArgoCD applications with optional grep filtering",
    content="""
    #!/bin/bash
    set -e
    
    # Strip protocol from server URL if present
    SERVER_URL="${ARGOCD_SERVER#https://}"
    SERVER_URL="${SERVER_URL#http://}"
    
    echo "Listing ArgoCD applications..."
    echo "Server: $SERVER_URL"
    if [ ! -z "$grep_filter" ]; then
        echo "Filtering with: $grep_filter"
    fi
    echo ""
    
    # Execute the app list command
    if [ ! -z "$grep_filter" ]; then
        # Use grep filtering if provided
        argocd app list --server "$SERVER_URL" --auth-token "$ARGOCD_AUTH_TOKEN" --grpc-web --insecure | grep "$grep_filter"
    else
        # List all applications without filtering
        argocd app list --server "$SERVER_URL" --auth-token "$ARGOCD_AUTH_TOKEN" --grpc-web --insecure
    fi
    """,
    args=[
        Arg(
            name="grep_filter", 
            type="str", 
            description="Optional grep filter to apply to the application list (e.g., 'Synced', 'OutOfSync', 'myapp')",
            required=False
        ),
    ],
    image="argoproj/argocd:latest"
)

tool_registry.register("argocd_cli", argocd_cli_tool)
tool_registry.register("argocd_app_get", argocd_app_get_tool)
tool_registry.register("argocd_app_list", argocd_app_list_tool) 