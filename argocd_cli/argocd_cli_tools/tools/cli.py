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
    
    echo "=== Environment Variables ==="
    echo "ARGOCD_SERVER: $ARGOCD_SERVER"
    echo "ARGOCD_AUTH_TOKEN: $ARGOCD_AUTH_TOKEN"
    echo ""
    
    # Strip protocol from server URL if present
    SERVER_URL="${ARGOCD_SERVER#https://}"
    SERVER_URL="${SERVER_URL#http://}"
    echo "=== Processed Server URL ==="
    echo "SERVER_URL: $SERVER_URL"
    echo ""
    
    # Set ArgoCD CLI environment variables for authentication
    export ARGOCD_SERVER="$SERVER_URL"
    export ARGOCD_AUTH_TOKEN="$ARGOCD_AUTH_TOKEN"
    export ARGOCD_OPTS="--grpc-web --insecure"
    
    echo "=== ArgoCD Configuration ==="
    echo "Using server: $ARGOCD_SERVER"
    echo "Using options: $ARGOCD_OPTS"
    echo ""
    
    # Execute the command directly (no explicit login needed with auth token)
    echo "=== Executing Command ==="
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

tool_registry.register("argocd_cli", argocd_cli_tool) 