"""
Instead of adding silence at start and end of recording (values=0) I add the original audio.
This makes audio sound more natural as volume is >0. See trim().
I also fixed issue with accumulated silence counter needs to be cleared once recording is resumed.
See record().
"""

from array import array
from struct import pack
from sys import byteorder
import copy
import wave

import pyaudio


THRESHOLD = 1000  # audio levels not normalised.
CHUNK_SIZE = 1024
SILENT_CHUNKS = 3 * 44100 / 1024  # about 3sec
FORMAT = pyaudio.paInt16
FRAME_MAX_VALUE = 2**15 - 1
NORMALIZE_MINUS_ONE_DB = 10 ** (-1.0 / 20)
RATE = 44100
CHANNELS = 1
TRIM_APPEND = RATE / 4


def is_silent(data_chunk):
    """Returns 'True' if below the 'silent' threshold"""
    return max(data_chunk) < THRESHOLD


def normalize(data_all):
    """Amplify the volume out to max -1dB"""
    # MAXIMUM = 16384
    normalize_factor = float(NORMALIZE_MINUS_ONE_DB * FRAME_MAX_VALUE) / max(
        abs(i) for i in data_all
    )

    normalized_data = array("h")
    for i in data_all:
        normalized_data.append(int(i * normalize_factor))
    return normalized_data


def trim(data_all):
    """Trim the blank spots at the start and end"""
    _from = 0
    _to = len(data_all) - 1
    for i, sample in enumerate(data_all):
        if abs(sample) > THRESHOLD:
            _from = max(0, i - TRIM_APPEND)
            break

    for i, sample in enumerate(reversed(data_all)):
        if abs(sample) > THRESHOLD:
            _to = min(len(data_all) - 1, len(data_all) - 1 - i + TRIM_APPEND)
            break

    return copy.deepcopy(data_all[int(_from) : (int(_to) + 1)])


def record():
    """Record a word or words from the microphone and
    return the data as an array of signed shorts."""

    py_audio = pyaudio.PyAudio()
    stream = py_audio.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        output=True,
        frames_per_buffer=CHUNK_SIZE,
    )

    silent_chunks = 0
    audio_started = False
    data_all = array("h")

    while True:
        # little endian, signed short
        data_chunk = array("h", stream.read(CHUNK_SIZE))
        if byteorder == "big":
            data_chunk.byteswap()
        data_all.extend(data_chunk)

        silent = is_silent(data_chunk)

        if audio_started:
            if silent:
                silent_chunks += 1
                if silent_chunks > SILENT_CHUNKS:
                    break
            else:
                silent_chunks = 0
        elif not silent:
            audio_started = True

    sample_width = py_audio.get_sample_size(FORMAT)
    stream.stop_stream()
    stream.close()
    py_audio.terminate()

    # we trim before normalize as threshhold applies to un-normalized wave
    # (as well as is_silent() function)
    data_all = trim(data_all)
    data_all = normalize(data_all)
    return sample_width, data_all


def record_to_file(path):
    "Records from the microphone and outputs the resulting data to 'path'"
    sample_width, data = record()
    data = pack("<" + ("h" * len(data)), *data)

    wave_file = wave.open(path, "wb")
    wave_file.setnchannels(CHANNELS)
    wave_file.setsampwidth(sample_width)
    wave_file.setframerate(RATE)
    wave_file.writeframes(data)
    wave_file.close()


if __name__ == "__main__":
    print("Wait in silence to begin recording; wait in silence to terminate")
    record_to_file("demo.wav")
    print("done - result written to demo.wav")
