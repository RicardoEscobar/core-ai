import wave
import pyaudio


def get_audio_device_index(device_name: str) -> int:
    """Get the audio device index from the device name."""
    # Create the PyAudio object
    audio = pyaudio.PyAudio()

    # Get the device index
    device_index = None
    for i in range(audio.get_device_count()):
        device = audio.get_device_info_by_index(i)
        if device['name'] == device_name:
            device_index = device['index']
            break

    # Raise an error if the device was not found
    if device_index is None:
        raise ValueError(f"Device '{device_name}' not found.")

    # Return the device index
    return device_index

def play_audio(audio_file_path: str):
    # Open the WAV file
    with wave.open(audio_file_path, 'rb') as wave_file:
        # Validate wave_file is a valid WAV file
        if wave_file.getnchannels() != 1:
            raise ValueError('Audio file must be single channel')
        print(f"wave_file.getnchannels(): {wave_file.getnchannels()}")
        # Get the audio file's format
        audio_format = pyaudio.paInt16 if wave_file.getsampwidth() == 2 else pyaudio.paUInt8

        # Create the PyAudio object
        audio = pyaudio.PyAudio()

        # # Print out the list of output devices ID for playback audio
        # print("List of output devices ID for playback audio:")
        # for i in range(audio.get_device_count()):
        #     device = audio.get_device_info_by_index(i)
        #     if device['maxOutputChannels'] > 0:
        #         print(f"    {device['index']}: {device['name']}")

        output_device_index = get_audio_device_index("VoiceMeeter Aux Input (VB-Audio")

        # Open a PyAudio stream for playback
        stream = audio.open(format=audio_format,
                            channels=wave_file.getnchannels(),
                            rate=wave_file.getframerate(),
                            output=True,
                            output_device_index=output_device_index
                            )

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
