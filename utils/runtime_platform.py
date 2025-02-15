import subprocess, logging, venv, sys, os


logger = logging.getLogger(__name__)


# i know only about two paths xd
if sys.platform == "linux":
    VENV = [".venv", "bin"]
    _PYTHON = ["python"]

else:
    VENV = [".venv", "Scripts"]
    _PYTHON = ["python.exe"]


PYTHON = VENV + _PYTHON
PATH_TO_PYTHON = os.sep.join(PYTHON)


def in_venv():
    current_prefix = sys.prefix  # ...\This-Project\.venv
    system_prefix = sys.base_prefix  # ...\Python\Python313
    return current_prefix != system_prefix


def check_platform() -> int:
    # if venv not exists then create it
    if not os.path.isfile(PATH_TO_PYTHON):
        print("Creating .venv...")
        venv.create(".venv", with_pip=True)
        returncode = install_packages()
        if returncode != 0:
            print(f"Something wrong with packages installing! {returncode=}")
            return returncode

    if not in_venv():
        returncode = start_venv()
        if returncode != 0:
            print(f"Something wrong with starting venv! {returncode=}")
        return returncode

    return 0


def install_packages() -> int:
    custom_requirements = "requirements.txt"
    command = [PATH_TO_PYTHON, "-m", "pip", "install", "-r", custom_requirements]
    print(f"Starting install packages from {custom_requirements!r}")

    p = subprocess.Popen(command)
    returncode = p.wait()
    if returncode != 0:
        logger.error(
            "idk what happened. write to me, maybe i can do something: https://a1ekzfame.t.me"
        )
        return returncode
    
    print("Packages installed")
    return 0


def install_package(package: str) -> bool:
    command = [PATH_TO_PYTHON, "-m", "pip", "install", package]
    print(f"Starting install package {package!r}")

    p = subprocess.Popen(command)
    returncode = p.wait()
    if returncode != 0:
        logger.error("idk what happened. something goes wrong")
        return False
    print("Package installed")
    return True


def start_venv() -> int:
    command = [PATH_TO_PYTHON, "main.py"]
    print(f"Starting main.py with {PATH_TO_PYTHON!r}")
    p = subprocess.Popen(command)
    returncode = p.wait()
    return returncode


check_platform()
