import os
import azure.cognitiveservices.speech as speechsdk
from dotenv import load_dotenv

def get_speech_synthesizer(selected_voice: str = 'Larissa') -> speechsdk.SpeechSynthesizer:
    """Get a speech synthesizer.
    
    Returns:
        speechsdk.SpeechSynthesizer: A speech synthesizer.
    """
    # Constants for speech synthesis configuration
    SPEECH_KEY = os.environ.get('SPEECH_KEY')
    SPEECH_REGION = os.environ.get('SPEECH_REGION')
    VOICE_NAME = {
        'Jenny': 'en-US-JennyNeural',
        'Marina': 'es-MX-MarinaNeural',
        'Beatriz': 'es-MX-BeatrizNeural',
        'Nuria': 'es-MX-NuriaNeural',
        'Renata': 'es-MX-RenataNeural',
        'Larissa': 'es-MX-LarissaNeural',
        'Dalia' : 'es-MX-DaliaNeural',
        'Carlota' : 'es-MX-CarlotaNeural',
        'Candela' : 'es-MX-CandelaNeural',
        'Camila' : 'es-PE-CamilaNeural',
        'Elena' : 'es-AR-ElenaNeural',
        'Tania' : 'es-PY-TaniaNeural',
        'Salome' : 'es-CO-SalomeNeural',
        'Juan' : 'es-CR-JuanNeural',
        'Bernd' : 'de-DE-BerndNeural',
        'Gisela' : 'de-DE-GiselaNeural',
        'Amala' : 'de-DE-AmalaNeural',
    }

    # This example requires environment variables named "SPEECH_KEY" and "SPEECH_REGION"
    speech_config = speechsdk.SpeechConfig(subscription=SPEECH_KEY, region=SPEECH_REGION)
    audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)

    # The language of the voice that speaks.
    speech_config.speech_synthesis_voice_name=VOICE_NAME[selected_voice]

    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
    return speech_synthesizer

def speak_text(speech_synthesizer: speechsdk.SpeechSynthesizer, text: str):
    """Speak the text.
    
    Args:
        speech_synthesizer (speechsdk.SpeechSynthesizer): A speech synthesizer.
        text (str): The text to speak.
    """
    speech_synthesis_result = speech_synthesizer.speak_text_async(text).get()

    if speech_synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print(f"Speech synthesized for text [{text}]")
    elif speech_synthesis_result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = speech_synthesis_result.cancellation_details
        print(f"Speech synthesis canceled: {cancellation_details.reason}")
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            if cancellation_details.error_details:
                print(f"Error details: {cancellation_details.error_details}")
                print("Did you set the speech resource key and region values?")

def main():
    # Load environment variables from .env file
    load_dotenv()

    # Constants for speech synthesis configuration
    SELECTED_VOICE = 'Larissa'

    # Get text from the console and synthesize to the default speaker.
    text = input(f"Introduce un texto que desees que hable {SELECTED_VOICE} >")

    # Get a speech synthesizer
    speech_synthesizer = get_speech_synthesizer(SELECTED_VOICE)

    # Speak the text
    speak_text(speech_synthesizer, text)


if __name__ == '__main__':
    main()