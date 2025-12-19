import sys
from pathlib import Path

from dotenv import load_dotenv

project_root = Path(__file__).resolve().parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

env_path = project_root / ".env"
load_dotenv(env_path if env_path.exists() else None)

from app import create_app

application = create_app()
