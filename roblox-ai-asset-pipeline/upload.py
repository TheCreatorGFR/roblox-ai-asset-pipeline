"""Step 3: upload an FBX to Roblox with the Open Cloud Assets API."""
import argparse
import json
import time
from pathlib import Path

import requests

from config import ROBLOX_API_KEY, ROBLOX_CREATOR_ID

ASSETS_URL = "https://apis.roblox.com/assets/v1/assets"
OPERATION_URL = "https://apis.roblox.com/assets/v1/operations/{}"
HEADERS = {"x-api-key": ROBLOX_API_KEY}


def upload_model(fbx_path: Path, display_name: str, description: str) -> str:
    """Upload an FBX as a Roblox Model asset and return its asset ID."""
    asset_request = {
        "assetType": "Model",
        "displayName": display_name,
        "description": description,
        "creationContext": {"creator": {"userId": ROBLOX_CREATOR_ID}},
    }
    with fbx_path.open("rb") as fbx_file:
        response = requests.post(
            ASSETS_URL,
            headers=HEADERS,
            files={
                "request": (None, json.dumps(asset_request), "application/json"),
                "fileContent": (fbx_path.name, fbx_file, "model/fbx"),
            },
            timeout=120,
        )
    if not response.ok:
        raise RuntimeError(f"Upload failed: {response.status_code} {response.text}")
    return wait_for_asset(response.json())


def wait_for_asset(operation: dict, interval: float = 3, timeout: float = 300) -> str:
    """Poll an Open Cloud operation until Roblox finishes processing the upload."""
    operation_id = operation.get("operationId") or operation["path"].split("/")[-1]
    deadline = time.monotonic() + timeout

    while not operation.get("done"):
        if time.monotonic() > deadline:
            raise TimeoutError(f"Operation {operation_id} still processing after {timeout}s")
        time.sleep(interval)
        response = requests.get(OPERATION_URL.format(operation_id), headers=HEADERS, timeout=30)
        if not response.ok:
            raise RuntimeError(f"Polling failed: {response.status_code} {response.text}")
        operation = response.json()

    return operation["response"]["assetId"]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Upload an FBX model to Roblox.")
    parser.add_argument("fbx", type=Path, help="Path to the .fbx file")
    parser.add_argument("--name", help="Display name (default: the file name)")
    parser.add_argument("--description", default="", help="Asset description")
    args = parser.parse_args()
    asset_id = upload_model(args.fbx, args.name or args.fbx.stem, args.description)
    print(f"Uploaded: rbxassetid://{asset_id}")
