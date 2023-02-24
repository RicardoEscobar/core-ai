"""
Set PYTHONPATH variable to the root directory of the project
"""
import os
from pathlib import Path


def set_pythonpath(root_path: Path = Path('.')):
    """
    This function is used to set the PYTHONPATH variable to the root directory of the project.
    """
    print(f'$PYTHONPATH = {root_path.resolve()}')
    os.environ['PYTHONPATH'] = str(root_path.resolve())


# Call the function
set_pythonpath(Path('C:/Users/Jorge/git/core-ai'))

if __name__ == '__main__':
    set_pythonpath()
    print(os.environ['PYTHONPATH'])
