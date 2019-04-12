from pathlib import Path
import os

from src.config import SOURCE_DIRECTORY


if __name__ == "__main__":
    path_setup = os.path.join(SOURCE_DIRECTORY, "setup.py")
    wd = Path(path_setup).parent.parent
    os.chdir(str(wd))
    print(os.getcwd())
    cmd = "python {} build_ext --inplace".format(path_setup)
    os.system(cmd)
