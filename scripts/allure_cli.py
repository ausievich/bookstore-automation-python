"""Bootstrap and run the Allure CLI from .allure-cli/."""

from __future__ import annotations

import platform
import subprocess
import sys
import tarfile
import urllib.request
from pathlib import Path

ALLURE_VERSION = "2.34.0"
ROOT = Path(__file__).resolve().parent.parent
ALLURE_HOME = ROOT / ".allure-cli" / f"allure-{ALLURE_VERSION}"
ALLURE_BIN = ALLURE_HOME / "bin" / ("allure.bat" if platform.system() == "Windows" else "allure")
RESULTS_DIR = ROOT / "allure-results"
REPORT_DIR = ROOT / "allure-report"


def install() -> Path:
    if ALLURE_BIN.exists():
        return ALLURE_BIN

    ALLURE_HOME.parent.mkdir(parents=True, exist_ok=True)
    archive = ALLURE_HOME.parent / f"allure-{ALLURE_VERSION}.tgz"
    url = (
        f"https://github.com/allure-framework/allure2/releases/download/"
        f"{ALLURE_VERSION}/allure-{ALLURE_VERSION}.tgz"
    )

    print(f"Downloading Allure {ALLURE_VERSION}...")
    urllib.request.urlretrieve(url, archive)

    print("Extracting...")
    with tarfile.open(archive, "r:gz") as tar:
        tar.extractall(path=ALLURE_HOME.parent)

    archive.unlink(missing_ok=True)

    if not ALLURE_BIN.exists():
        raise SystemExit(f"Allure binary not found at {ALLURE_BIN}")

    print(f"Allure installed to {ALLURE_HOME}")
    return ALLURE_BIN


def run_allure(args: list[str]) -> None:
    bin_path = install()
    result = subprocess.run([str(bin_path), *args], cwd=ROOT, check=False)
    raise SystemExit(result.returncode)


def main() -> None:
    if len(sys.argv) < 2:
        raise SystemExit("Usage: python scripts/allure_cli.py <install|generate|open>")

    command = sys.argv[1]
    if command == "install":
        install()
        return

    if command == "generate":
        if not RESULTS_DIR.exists() or not any(RESULTS_DIR.iterdir()):
            raise SystemExit(
                f"No Allure results in {RESULTS_DIR}. Run tests first: uv run task test"
            )
        run_allure(["generate", str(RESULTS_DIR), "--clean", "-o", str(REPORT_DIR)])
        return

    if command == "open":
        if not REPORT_DIR.exists():
            raise SystemExit(
                f"No report at {REPORT_DIR}. Run: uv run task allure-gen"
            )
        run_allure(["open", str(REPORT_DIR)])
        return

    raise SystemExit(f"Unknown command: {command}")


if __name__ == "__main__":
    main()
