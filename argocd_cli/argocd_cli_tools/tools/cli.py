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
    
    echo "=== ArgoCD CLI Authentication ==="
    echo "Server: $ARGOCD_SERVER"
    echo ""
    
    # Perform ArgoCD login to initialize context and trust settings
    echo "Logging into ArgoCD server..."
    if argocd login "$ARGOCD_SERVER" --auth-token "$ARGOCD_AUTH_TOKEN" --insecure; then
        echo "✅ Successfully logged into ArgoCD"
    else
        echo "❌ Failed to login to ArgoCD"
        exit 1
    fi
    
    echo ""
    echo "=== Executing ArgoCD CLI Command ==="
    echo "Command: argocd $command"
    echo ""
    
    # Execute the command
    if eval "argocd $command"; then
        echo "✅ Command executed successfully"
    else
        echo "❌ Command failed: argocd $command"
        exit 1
    fi
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