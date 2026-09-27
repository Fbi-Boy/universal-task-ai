import os
from pathlib import Path


def main() -> int:
    env_path = Path('.env')
    if not env_path.is_file():
        print('Missing .env. Copy .env.example to .env first.')
        return 1

    browser = os.environ.get('UTA_BROWSER_ENABLED', 'false').lower() == 'true'
    sandbox = os.environ.get('UTA_PYTHON_SANDBOX_ENABLED', 'false').lower() == 'true'
    roots = bool(os.environ.get('UTA_LOCAL_ROOTS', '').strip())
    print(f'browser_enabled={browser}')
    print(f'local_roots_configured={roots}')
    print(f'python_sandbox_enabled={sandbox}')
    if browser and not os.environ.get('UTA_BROWSER_ALLOWED_HOSTS', '').strip():
        print('Browser is enabled but UTA_BROWSER_ALLOWED_HOSTS is empty.')
        return 2
    if sandbox and '@sha256:' not in os.environ.get('UTA_SANDBOX_IMAGE', ''):
        print('Python sandbox requires an immutable sha256 image reference.')
        return 3
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
