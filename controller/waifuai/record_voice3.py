"""
This script records audio from the default microphone and saves it to a WAV file.
There are two functions:
    - start_recording: records audio from the default microphone and waits for stop_recording call.
    - stop_recording: stops recording audio and saves it to a WAV file.
"""
import sounddevice as sd
import soundfile as sf
import numpy as np
import time
import threading

# Set the audio file parameters
FILENAME = "recording_open_mic.wav"
SAMPLERATE = 16000
CHANNELS = 1
SUBTYPE = "PCM_16"
DURATION = 5  # in seconds
THRESHOLD = 0  # Amplitude threshold for detecting speech

def start_recording():
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

def stop_recording():
    # Record audio from the default microphone
    print(f"Recording {DURATION} seconds of audio...")
    recording = sd.rec(int(DURATION * SAMPLERATE), samplerate=SAMPLERATE, channels=CHANNELS)
    sd.wait()

    # Save the recording to a WAV file
    print(f"Saving recording to {FILENAME}...")
    sf.write(FILENAME, recording, SAMPLERATE, subtype=SUBTYPE)

def main():
    # Start recording thread
    recording_thread = threading.Thread(target=start_recording)
    recording_thread.start()

    # Wait for 10 seconds
    time.sleep(10)

    # Stop recording thread
    stop_recording()

if __name__ == "__main__":
    main()