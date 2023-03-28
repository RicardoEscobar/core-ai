"""
This module records audio from the default microphone and saves it to a WAV file.
"""
import sounddevice as sd
import soundfile as sf
import numpy as np

# Set the audio file parameters
FILENAME = "recording_open_mic.wav"
SAMPLERATE = 16000
CHANNELS = 1
SUBTYPE = "PCM_16"
DURATION = 5  # in seconds
THRESHOLD = 0  # Amplitude threshold for detecting speech

def record_voice():
    """
    Detects if the user is talking (open mic) and records the audio into a wave file.
    
    If the user is talking, the function will record the audio until he or she stops talking then save it to a wave file.

    There is no specified duration for the recording. Keep recording until the user stops talking.
    """

    print("Recording started. Speak into the microphone...")
    frames = []
    while True:
        # Record audio for `duration` seconds
        recording = sd.rec(int(SAMPLERATE * DURATION), samplerate=SAMPLERATE, channels=CHANNELS)
        sd.wait()

        # Append new recording to list of frames
        frames.append(recording)

        # Convert list of frames to numpy array and normalize
        audio = np.concatenate(frames, axis=0)
        audio /= np.max(np.abs(audio))

        # Detect if the user is speaking
        if np.max(audio) > THRESHOLD:
            print("User is speaking...")
        else:
            print("User stopped speaking.")

            # Save audio to file and reset list of frames
            sf.write(FILENAME, audio, SAMPLERATE)
            frames = []



    
def record_voice_duration(duration: int = 5):
    # Record audio from the default microphone
    print(f"Recording {duration} seconds of audio...")
    recording = sd.rec(int(duration * SAMPLERATE), samplerate=SAMPLERATE, channels=CHANNELS)
    sd.wait()

    # Save the recording to a WAV file
    print(f"Saving recording to {FILENAME}...")
    sf.write(FILENAME, recording, SAMPLERATE, subtype=SUBTYPE)

    print("Done!")

def main():
    # record_voice_duration(DURATION)
    record_voice()

if __name__ == "__main__":
    main()
