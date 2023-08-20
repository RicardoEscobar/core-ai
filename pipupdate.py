"""This script updates all pip packages in the current environment."""
import subprocess
import sys
from typing import List

import pkg_resources


def get_outdated_packages() -> List[str]:
    """Returns a list of outdated packages."""
    args = [sys.executable, "-m", "pip", "list", "--outdated"]
    result = subprocess.run(args, stdout=subprocess.PIPE)
    output = result.stdout.decode("utf-8")
    lines = output.split("\n")
    packages = []
    for line in lines[2:-1]:
        package = line.split(" ")[0]
        packages.append(package)
    return packages

def update_packages(packages: List[str]) -> None:
    """Updates the given packages."""
    args = [sys.executable, "-m", "pip", "install", "--upgrade"] + packages
    subprocess.run(args)

def main() -> None:
    """Updates all pip packages in the current environment."""
    packages = get_outdated_packages()
    update_packages(packages)


if __name__ == "__main__":
    main()
