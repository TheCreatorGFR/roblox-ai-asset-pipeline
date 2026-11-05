"""Step 1: generate a modeling-reference concept image with FLUX on Cloudflare Workers AI."""
import argparse
import base64
from pathlib import Path

import requests

from config import CLOUDFLARE_ACCOUNT_ID, CLOUDFLARE_API_TOKEN

FLUX_URL = (
    "https://api.cloudflare.com/client/v4/accounts/"
    f"{CLOUDFLARE_ACCOUNT_ID}/ai/run/@cf/black-forest-labs/flux-1-schnell"
)


def generate_concept(subject: str, out_path: Path, steps: int = 4) -> Path:
    """Generate a modeling-reference image of `subject` and save it as a JPEG."""
    prompt = (
        f"{subject}, single object, three-quarter view, "
        "plain light grey background, soft even lighting, "
        "clean low-poly style with flat colors, "
        "no text, no watermark, no logo"
    )
    response = requests.post(
        FLUX_URL,
        headers={"Authorization": f"Bearer {CLOUDFLARE_API_TOKEN}"},
        json={"prompt": prompt, "steps": steps},  # steps: 1-8, higher = more detail
        timeout=60,
    )
    if not response.ok:
        raise RuntimeError(f"FLUX request failed: {response.status_code} {response.text}")

    image_b64 = response.json()["result"]["image"]
    out_path.write_bytes(base64.b64decode(image_b64))
    return out_path


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a concept image with FLUX.")
    parser.add_argument("subject", help='What to draw, e.g. "wooden treasure chest"')
    parser.add_argument("--out", default="concept.jpg", help="Output file (default: concept.jpg)")
    parser.add_argument("--steps", type=int, default=4, help="1-8; higher = more detail")
    args = parser.parse_args()
    print(f"Saved {generate_concept(args.subject, Path(args.out), args.steps)}")
