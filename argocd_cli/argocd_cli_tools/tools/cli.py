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
    
    echo "=== Environment Debug Information ==="
    echo "ARGOCD_SERVER: '$ARGOCD_SERVER'"
    echo "ARGOCD_AUTH_TOKEN: '$ARGOCD_AUTH_TOKEN'"
    echo "ARGOCD_AUTH_TOKEN length: ${#ARGOCD_AUTH_TOKEN}"
    echo "Current working directory: $(pwd)"
    echo "User: $(whoami)"
    echo "Hostname: $(hostname)"
    echo ""
    
    echo "=== ArgoCD CLI Authentication ==="
    echo "Server: $ARGOCD_SERVER"
    # Use cut instead of bash string slicing for better compatibility
    token_preview=$(echo "$ARGOCD_AUTH_TOKEN" | cut -c1-10)
    echo "Token: ${token_preview}... (truncated for security)"
    echo ""
    
    # Test basic connectivity
    echo "=== Testing Connectivity ==="
    server_host=$(echo "$ARGOCD_SERVER" | sed 's|^https://||' | sed 's|^http://||' | cut -d: -f1)
    server_port=$(echo "$ARGOCD_SERVER" | sed 's|^https://||' | sed 's|^http://||' | cut -d: -f2)
    server_port=${server_port:-443}  # Default to 443 if no port specified
    
    echo "Extracted host: $server_host"
    echo "Extracted port: $server_port"
    
    # Test DNS resolution
    if nslookup "$server_host" >/dev/null 2>&1; then
        echo "✅ DNS resolution successful for $server_host"
    else
        echo "❌ DNS resolution failed for $server_host"
        echo "Trying to resolve with dig:"
        dig "$server_host" || echo "dig command not available"
    fi
    
    # Test port connectivity
    if timeout 5 bash -c "</dev/tcp/$server_host/$server_port" 2>/dev/null; then
        echo "✅ Port $server_port is reachable on $server_host"
    else
        echo "❌ Port $server_port is not reachable on $server_host"
        echo "This could indicate:"
        echo "  - Firewall blocking the connection"
        echo "  - ArgoCD server is not running"
        echo "  - Wrong port number"
        echo "  - Network connectivity issues"
    fi
    echo ""
    
    # Perform ArgoCD login to initialize context and trust settings
    echo "=== Attempting ArgoCD Login ==="
    echo "Command: argocd login \"$ARGOCD_SERVER\" --auth-token \"[TOKEN]\" --insecure"
    echo ""
    
    if argocd login "$ARGOCD_SERVER" --auth-token "$ARGOCD_AUTH_TOKEN" --insecure; then
        echo "✅ Successfully logged into ArgoCD"
    else
        echo "❌ Failed to login to ArgoCD"
        echo ""
        echo "=== Troubleshooting Information ==="
        echo "1. Verify ARGOCD_SERVER is correct: $ARGOCD_SERVER"
        echo "2. Verify ARGOCD_AUTH_TOKEN is valid"
        echo "3. Check if ArgoCD server is running and accessible"
        echo "4. Verify network connectivity and firewall rules"
        echo "5. Try with --insecure flag (already included)"
        echo "6. Check ArgoCD server logs for authentication errors"
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