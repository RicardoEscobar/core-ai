import pyaudio
import numpy as np
import threading
import asyncio

async def print_sound():
    print("Sound detected! Hello, World!")

# Function to check for sound
def check_for_sound():
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    THRESHOLD = 500  # Adjust this threshold to suit your environment

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("Listening for sound...")

    while True:
        data = np.frombuffer(stream.read(CHUNK), dtype=np.int16)
        if np.max(data) > THRESHOLD:
            # print("Sound detected! Hello, World!")
            asyncio.run(print_sound())

# Start a separate thread for sound detection
sound_thread = threading.Thread(target=check_for_sound)
sound_thread.daemon = True
sound_thread.start()

try:
    while True:
        pass
except KeyboardInterrupt:
    print("Stopped listening.")
