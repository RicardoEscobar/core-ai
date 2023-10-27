import os
import wave
from typing import Any, Dict, List

from mutagen.mp3 import MP3
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

def get_audio_devices() -> List[Dict[str, Any]]:
    """Get the audio devices."""
    # Create the PyAudio object
    audio = pyaudio.PyAudio()

    # Get the device index
    devices = []
    for i in range(audio.get_device_count()):
        device = audio.get_device_info_by_index(i)
        devices.append(device)

    # Return the device index
    return devices

def play_audio(audio_file_path: str, output_device_name: str = "VoiceMeeter Aux Input (VB-Audio"):
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

        output_device_index = get_audio_device_index(output_device_name)

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

def get_audio_duration(audio_file_path: str) -> float:
    """Get the duration of an audio file (WAV, MP3) in seconds."""
    # Get the file extension
    file_extension = os.path.splitext(audio_file_path)[1]

    if file_extension == '.wav':
        with wave.open(audio_file_path, 'rb') as wave_file:
            # Get the frame rate
            frame_rate = wave_file.getframerate()

            # Get the number of frames
            num_frames = wave_file.getnframes()

            # Calculate the duration
            duration = num_frames / frame_rate

            # Return the duration
            return duration
    elif file_extension == '.mp3':
        audio = MP3(audio_file_path)
        return audio.info.length
    else:
        raise ValueError(f"Unsupported file extension: {file_extension}. This function supports only WAV and MP3 files.")

if __name__ == "__main__":
    from pathlib import Path

    filepath = Path(r'D:\conversation-ai\005-Loona-V4\2023-07-23_03-18-58_Loona.wav')
    #play_audio('example.wav')
    print(f'duration = {get_audio_duration(str(filepath))} seconds it should be 37 seconds')
