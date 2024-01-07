"""Get voices from Eleven Labs."""
from elevenlabs import voices, clone, generate, play
from controller.load_openai import load_openai
from typing import List


_ = load_openai()

def get_voices(name:str) -> List[str]:
    # Load Eleven Labs API key
    load_openai()

    voices_list = voices()
    for voice in voices_list:
        if voice.name == name:
            voz = voice
            print(repr(voice))

    audio = generate(text="Hola, la voz ha sido encontrada.", voice=voz, model="eleven_multilingual_v2")

    play(audio)
    return voz

def get_voice_by_id(id:str) -> None:
    """Get a voice from Eleven Labs by id.
    args:
        id: The id of the voice to get."""

    for voice in voices():
        if voice.voice_id == id:
            print(repr(voice))
            print(type(voice))
            return voice

    

def clone_voice() -> None:
    """Clone a voice from Eleven Labs.
    args:
        voice: The voice to clone."""

    voice = clone(
        name="Ceci2",
        description="Delete me", # Optional
        files=["./sample.mp3"],
    )

    audio = generate(text="Hola, soy una voz clonada.", voice=voice)

    play(audio)

if __name__ == "__main__":
    voz = get_voices("Cecilia Cortes Morales")
    print(repr(voz))
