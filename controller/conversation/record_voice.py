"""
This script records audio from the default input device and saves it to a WAV file named "output.wav".
"""
import wave
import pyaudio
from typing import List




def record_voice() -> List[bytes]:
    """It uses the pyaudio library to access the audio device and record the audio. The stream object is created using pyaudio.open(), which takes in parameters such as the audio format, number of channels, sampling rate, and frames per buffer. In this case, it's set to record 16-bit integer audio samples at a sampling rate of 44.1kHz with a buffer size of 1024 frames.
    
    returns:
        frames: List[bytes]
    """

    audio = pyaudio.PyAudio()
    stream = audio.open(
        format=pyaudio.paInt16,
        channels=1, rate=44100,
        input=True,
        frames_per_buffer=1024
    )

    frames = []

    # The script then enters a loop that reads the audio data from the input stream in chunks of 1024 frames and appends them to the frames list. This loop will continue indefinitely until the user interrupts it with a keyboard interrupt (Ctrl+C).
    try:
        while True:
            data = stream.read(1024)
            frames.append(data)
    except KeyboardInterrupt:
        pass

    # Once the user interrupts the loop, the input stream is stopped, closed, and the audio object is terminated to release the resources used by the library.

    stream.stop_stream()
    stream.close()
    audio.terminate()

    return frames

def save_wav_file(filename: str = "output.wav", audio: pyaudio.PyAudio = None, frames: List = None):
    """
    Finally, the script creates a WAV file using the wave library and writes the recorded audio data to it. The WAV file is configured with the same audio format, channel count, and sampling rate as the input stream. The frames list is joined into a single byte string and written to the WAV file using the writeframes() method. Finally, the WAV file is closed.
    """
    sound_file = wave.open(filename, "wb")
    sound_file.setnchannels(1)
    sound_file.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
    sound_file.setframerate(44100)
    sound_file.writeframes(b"".join(frames))
    sound_file.close()

def main():
    frames = record_voice()
    save_wav_file(frames=frames, audio=pyaudio.PyAudio())



if __name__ == "__main__":
    main()
