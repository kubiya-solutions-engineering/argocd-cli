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
    
    # Perform ArgoCD login
    echo "=== ArgoCD Login ==="
    argocd login "$SERVER_URL" --auth-token "$ARGOCD_AUTH_TOKEN" --insecure
    echo ""
    
    # Execute the command
    echo "=== Executing Command ==="
    argocd $command
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