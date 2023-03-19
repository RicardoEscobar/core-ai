"""
This script records audio from the default microphone and saves it to a WAV file.
"""
import sounddevice as sd
import soundfile as sf

# Set the audio file parameters
FILENAME = "recording.wav"
SAMPLERATE = 16000
CHANNELS = 1
SUBTYPE = "PCM_16"

# Record audio from the default microphone for 5 seconds
DURATION = 5  # in seconds
print(f"Recording {DURATION} seconds of audio...")
recording = sd.rec(int(DURATION * SAMPLERATE), samplerate=SAMPLERATE, channels=CHANNELS)
sd.wait()

# Save the recording to a WAV file
print(f"Saving recording to {FILENAME}...")
sf.write(FILENAME, recording, SAMPLERATE, subtype=SUBTYPE)

print("Done!")
