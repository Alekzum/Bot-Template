from utils.runtime_platform import in_venv, start_venv
import subprocess
import sys


def main():
    if not in_venv():
        try:
            returncode = start_venv()
        except KeyboardInterrupt:
            return
        exit(returncode)

    # in theory we are in venv
    process = subprocess.Popen([sys.executable, "main.py"])
    try:
        process.wait()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
