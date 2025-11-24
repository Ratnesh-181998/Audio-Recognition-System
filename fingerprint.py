# fingerprint.py
"""Core fingerprint generation for the Shazam prototype.

The algorithm follows the classic Shazam approach:
1. Load audio (mono, 22050 Hz).
2. Compute a magnitude spectrogram.
3. Identify spectral peaks (local maxima).
4. Create hash pairs from peak coordinates (frequency, time).

The output is a set of hash strings that can be used as keys in a fingerprint database.
"""

import numpy as np
import librosa

# Configuration constants – tweak for better performance
SR = 22050          # Sample rate for processing
N_FFT = 4096        # FFT window size
HOP_LENGTH = 512    # Hop length between frames
PEAK_NEIGHBORHOOD_SIZE = 20  # Neighborhood size for peak picking
FAN_VALUE = 15      # Number of neighbouring peaks to pair with each anchor peak


def load_audio(file_path: str) -> np.ndarray:
    """Load an audio file and return a mono waveform at the target sample rate."""
    y, _ = librosa.load(file_path, sr=SR, mono=True)
    return y


def compute_spectrogram(y: np.ndarray) -> np.ndarray:
    """Return the magnitude spectrogram (in dB) of the audio signal."""
    S = np.abs(librosa.stft(y, n_fft=N_FFT, hop_length=HOP_LENGTH))
    return S


def get_peaks(S: np.ndarray) -> list:
    """Detect spectral peaks in the spectrogram.

    Returns a list of (frequency_bin, time_bin) tuples.
    """
    # Convert to log‑scale for better peak detection
    log_S = librosa.amplitude_to_db(S, ref=np.max)
    # Use a simple local maximum filter
    from scipy.ndimage import maximum_filter
    neighborhood = maximum_filter(log_S, size=PEAK_NEIGHBORHOOD_SIZE)
    peaks = (log_S == neighborhood) & (log_S > np.median(log_S))
    freq_bins, time_bins = np.where(peaks)
    return list(zip(freq_bins, time_bins))


def generate_hashes(peaks: list) -> set:
    """Create hash strings from peak pairs.

    For each anchor peak we pair it with the next ``FAN_VALUE`` peaks in time.
    The hash format is ``f1|f2|dt`` where ``f1`` and ``f2`` are frequency bins and
    ``dt`` is the time difference (in frames).
    """
    hashes = set()
    for i, anchor in enumerate(peaks):
        for j in range(1, FAN_VALUE + 1):
            if i + j >= len(peaks):
                break
            target = peaks[i + j]
            f1, t1 = anchor
            f2, t2 = target
            dt = t2 - t1
            hash_str = f"{f1}|{f2}|{dt}"
            hashes.add(hash_str)
    return hashes


def fingerprint_file(file_path: str) -> set:
    """Convenience wrapper – load, compute spectrogram, detect peaks, generate hashes."""
    y = load_audio(file_path)
    S = compute_spectrogram(y)
    peaks = get_peaks(S)
    return generate_hashes(peaks)

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python fingerprint.py <audio_file.wav>")
        sys.exit(1)
    hashes = fingerprint_file(sys.argv[1])
    print(f"Generated {len(hashes)} hashes")
