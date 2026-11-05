"""Load API credentials from environment variables.

Never put keys in code. Set these as user environment variables instead:
CLOUDFLARE_ACCOUNT_ID, CLOUDFLARE_API_TOKEN, ROBLOX_API_KEY, ROBLOX_CREATOR_ID
"""
import os


def require_env(name: str) -> str:
    """Read a secret from the environment, failing loudly if it's missing."""
    value = os.environ.get(name)
    if not value:
        raise RuntimeError(f"Missing environment variable: {name}")
    return value


CLOUDFLARE_ACCOUNT_ID = require_env("CLOUDFLARE_ACCOUNT_ID")
CLOUDFLARE_API_TOKEN = require_env("CLOUDFLARE_API_TOKEN")
ROBLOX_API_KEY = require_env("ROBLOX_API_KEY")
ROBLOX_CREATOR_ID = require_env("ROBLOX_CREATOR_ID")
