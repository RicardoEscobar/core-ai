import wave
import pyaudio

def play_audio(audio_file_path: str):
    # Open the WAV file
    with wave.open(audio_file_path, 'rb') as wave_file:
        # Get the audio file's format
        audio_format = pyaudio.paInt16 if wave_file.getsampwidth() == 2 else pyaudio.paUInt8

        # Create the PyAudio object
        audio = pyaudio.PyAudio()

        # Open a PyAudio stream for playback
        stream = audio.open(format=audio_format,
                            channels=wave_file.getnchannels(),
                            rate=wave_file.getframerate(),
                            output=True)

        # Read data from the file and play it through the stream
        data = wave_file.readframes(1024)
        while data:
            stream.write(data)
            data = wave_file.readframes(1024)

        # Cleanup
        stream.stop_stream()
        stream.close()
        audio.terminate()

if __name__ == "__main__":
    play_audio('example.wav')
