from pathlib import Path

def test_production_container_is_non_root() -> None:
    dockerfile=Path("Dockerfile").read_text()
    assert "USER app" in dockerfile
    assert "HEALTHCHECK" in dockerfile

def test_production_compose_drops_capabilities() -> None:
    compose=Path("docker-compose.prod.yml").read_text()
    assert "cap_drop: [ALL]" in compose
    assert "read_only: true" in compose
    assert "no-new-privileges:true" in compose
