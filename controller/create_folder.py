from pathlib import Path


def create_folder(folder_path: str = ".") -> Path:
    """Create a folder if it does not already exist.

    Args:
        folder_path (str): The path to the folder.

    Returns:
        Path: The path to the folder.
    """
    if folder_path == ".":
        returned_folder_path = Path(__file__).parent / "conversations"
    else:
        returned_folder_path = Path(folder_path)

    if not returned_folder_path.exists():
        returned_folder_path.mkdir(parents=True, exist_ok=True)

    return returned_folder_path