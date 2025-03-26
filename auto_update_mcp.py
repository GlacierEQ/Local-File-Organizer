import json
import sys
import os
from typing import Any, Dict

# Ensure the CONFIG_PATH here is consistent with blackbox_ai.py if reused.
CONFIG_PATH: str = r'C:\Users\casey\AppData\Roaming\Code\User\globalStorage\blackboxapp.blackboxagent\settings\blackbox_mcp_settings.json'

def load_config() -> Dict[str, Any]:
    """Load configuration synchronously from CONFIG_PATH with error handling."""
    try:
        with open(CONFIG_PATH, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Configuration file not found at {CONFIG_PATH}.")
        return {}
    except json.JSONDecodeError:
        print(f"Error decoding JSON from the configuration file at {CONFIG_PATH}.")
        return {}

def save_config(cfg: Dict[str, Any]) -> None:
    """Save configuration synchronously to CONFIG_PATH with error handling."""
    try:
        with open(CONFIG_PATH, 'w') as f:
            json.dump(cfg, f, indent=2)
    except IOError as e:
        print(f"Error saving configuration to {CONFIG_PATH}: {e}")

def add_or_update_server(name: str, url: str, api_key: str) -> None:
    """Add or update a server entry synchronously with error handling."""
    cfg = load_config()
    if 'mcpServers' not in cfg:
        cfg['mcpServers'] = {}
    cfg['mcpServers'][name] = {"url": url, "apiKey": api_key}
    save_config(cfg)

def main() -> None:
    """
    Main function for synchronous server update.
    Usage: auto_update_mcp.py <serverName> <url> <apiKey>
    """
    if len(sys.argv) != 4:
        print("Usage: auto_update_mcp.py <serverName> <url> <apiKey>")
        sys.exit(1)
    server_name, url, api_key = sys.argv[1], sys.argv[2], sys.argv[3]
    add_or_update_server(server_name, url, api_key)
    print(f"Server '{server_name}' updated automatically.")

if __name__ == '__main__':
    main()
