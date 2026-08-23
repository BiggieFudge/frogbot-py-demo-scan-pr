"""Order-receipt signing, backed by cryptography."""

import base64
import json
import os

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, hmac


def _key():
    secret = os.environ.get("ORDERS_SIGNING_KEY")
    if not secret:
        raise RuntimeError("ORDERS_SIGNING_KEY is not set")
    return secret.encode("utf-8")


def sign_receipt(receipt):
    """Return a base64 HMAC-SHA256 signature over the canonical receipt JSON."""
    payload = json.dumps(receipt, sort_keys=True, separators=(",", ":")).encode("utf-8")
    signer = hmac.HMAC(_key(), hashes.SHA256(), backend=default_backend())
    signer.update(payload)
    return base64.urlsafe_b64encode(signer.finalize()).decode("ascii")


def verify_receipt(receipt, signature):
    payload = json.dumps(receipt, sort_keys=True, separators=(",", ":")).encode("utf-8")
    verifier = hmac.HMAC(_key(), hashes.SHA256(), backend=default_backend())
    verifier.update(payload)
    try:
        verifier.verify(base64.urlsafe_b64decode(signature.encode("ascii")))
    except Exception:
        return False
    return True
