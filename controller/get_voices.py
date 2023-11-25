# add the project root directory to the system path
if __name__ == "__main__":
    from pathlib import Path

    project_directory = Path(__file__).parent.parent
    import sys

    # sys.path.insert(0, str(project_directory))
    sys.path.append(str(project_directory))


from elevenlabs import voices, generate

from controller.load_openai import load_openai

client = load_openai()

voices = voices()
# audio = generate(text="Hello there!", voice=voices[0])
print(voices)
with open("voices.py", "w", encoding="utf-8") as f:
    f.write(str(voices))