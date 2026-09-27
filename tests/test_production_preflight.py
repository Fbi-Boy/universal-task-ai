from scripts.production_preflight import DIGEST


def test_production_image_requires_immutable_digest():
    assert DIGEST.fullmatch("ghcr.io/acme/universal-task-ai@sha256:" + "a" * 64)
    assert not DIGEST.fullmatch("ghcr.io/acme/universal-task-ai:latest")
