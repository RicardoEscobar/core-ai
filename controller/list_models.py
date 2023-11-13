# If this file is running alone, then add the root folder to the Python path
if __name__ == "__main__":
    import sys
    from pathlib import Path

    root_folder = Path(__file__).parent.parent
    sys.path.append(str(root_folder))

import json

from controller.load_openai import load_openai


client = load_openai()

models = client.models.list()

print(models)
with open("models.py", "w", encoding="utf-8") as file:
    json.dump(repr(models), file, indent=4)
