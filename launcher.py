import sys
from pathlib import Path

# Make sure the compiled application directory is on sys.path
APP_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(APP_DIR))

from streamlit.web.bootstrap import run


if __name__ == "__main__":
    script_path = str(APP_DIR / "app_prototype.py")

    run(
        script_path,
        "streamlit run",
        [],
        {},
    )