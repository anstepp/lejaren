from collections import namedtuple
from math import ceil, floor, log2
from typing import List, Tuple

import numpy as np
import scipy.io.wavfile as scwav
from scipy.signal import find_peaks
from scipy.fft import rfft

import py2musicxml.log as logger
from py2musicxml.notation import Note, Tempo
from py2musicxml.notation.measure import TimeSignature
from py2musicxml.notation.score import Score

log = logger.get_logger()

fft_peak = namedtuple("fft_peak", ["start", "freq", "amp", "dur"])
mtp_peak = namedtuple("mtp_peak", ["freq", "distance", "amp"])
freq_amp_pair = namedtuple("freq_amp_pair", ["freq", "amp"])

C0 = 16.35
C1 = 32.7

DEFAULT_ZERO_PADDING_FACTOR = 6
DEFAULT_F0_RANGE = (32, 60)
DEFAULT_SAMPLING_RATE = 44100

DEFAULT_P = 0.5
DEFAULT_Q = 1.4
DEFAULT_R = 0.5
DEFAULT_NUM_PARTIALS = 8

HOP_SIZE = 2


def twelve_tet_gen(f0: float = C0):
    """
    Generator for producing frequency (Hz) for piano
    key pitches.
        f0: base pitch for frequency (default, C0)

    Returns:
        Generator object
    """
    starting_pitch = f0
    next_half_step = f0
    while True:
        yield next_half_step
        next_half_step = (starting_pitch) * (2 ** (1 / 12))
        starting_pitch = next_half_step


pitchgen = twelve_tet_gen(C1)
TWELVETET = [next(pitchgen) for x in range(128)]


class AutoTranscribe:
    """
    Class to code a soundfile into py2musicxml objects.

    Members:

    Methods:
    """

    def __init__(self, N, tempo: Tempo, fname=None):
        """
        Constructor for AutoTranscribe.

        Args:
            N: fft size (before zero-padding)
            tempo: a Tempo object

        Returns:
            an AutoTranscribe object

        """
        self.array = None
        self.tempo = tempo

        if fname:
            self._supply_audio(fname)
        else:
            self.fs = None
            self.audio = None

        # Check if N is a power of 2.
        if ceil(log2(N)) == floor(log2(N)):
            self.N = N
        else:
            log.error(f"N ({N}) is not a power of 2")
            raise ValueError(f"N ({N}) is not a power of 2")

    def _supply_audio(self, fname):
        """
        Get an audio file and convert it to NumPy array.

        Args:
            fname: file name

        returns:
            None
        """

        self.fs, self.audio = scwav.read(fname)

        try:
            self.filedur = len(self.audio)
        except FileNotFoundError as e:
            log.error(e)
            raise

    def get_note_list(self, f0_range: Tuple[int,]):
        start = 0
        notes = []

        frames = self._transform_x(self.N, self.audio)

        for frame_idx, frame in enumerate(frames):
            f0_range = DEFAULT_F0_RANGE

            best_guess = self._two_way_mismatch(frame, f0_range)
            octave, pc = self._get_pitch(best_guess)
            dur = self._get_fractional_beats(self.N, self.tempo.note_value)

            new_note = Note(dur, octave, pc)

            start += self.N

            if frame_idx > 0:
                if (new_note.octave == notes[-1].octave) and (
                    new_note.pc == notes[-1].pc
                ):
                    summed_duration = new_note.dur + notes[-1].dur
                    new_note = Note(summed_duration, new_note.octave, new_note.pc)
                    notes[-1] = new_note
                else:
                    notes.append(new_note)
            else:
                notes.append(new_note)

        return notes

    def _transform_x(
        self,
        N: int,  # sample size of FFT
        audio_array: np.ndarray,
        zpf: int = DEFAULT_ZERO_PADDING_FACTOR,
    ):
        """
        Transforms x with a FFT.

        Args:
            zpf: zero padding factor
        """

        start = 0
        frames = []
        hann = np.hamming(N)

        for stop in range(N, len(audio_array) - 1, int(N/HOP_SIZE)):

            x = audio_array[start:start+N]
            if len(x) < N:
                x = np.concatenate([x, np.zeros(N-len(x))])
            xw = x * hann

            # Create zero padding and zero pad signal.
            zp = np.zeros(N * (zpf - 1))
            xzp = np.concatenate([xw, zp])
            xzerophase = np.concatenate([xzp[int(N/HOP_SIZE)+1:], xzp[0:int(N/HOP_SIZE)]])

            # Take real FFT.
            Xr = rfft(xzerophase)

            # Get amplitude of bins lower than 800.
            Xrmag = abs(Xr)[:1200]
            max_height = max(Xrmag)

            peaks, _ = find_peaks(Xrmag, prominence=max_height * 0.05)
            frame = self._convert_to_frame(start, peaks, Xrmag, N, zpf)
            frames.append(frame)
            start = stop

        return frames

    def _convert_to_frame(
        self, start: int, peaks: np.ndarray, Xrmag: np.ndarray, N: int, zpf: int
    ) -> List[fft_peak]:
        frame = []
        for peak in peaks:
            freq, amp = self._parabolic_bin_to_pitch(peak, Xrmag, N, zpf)
            #             if freq > 20:
            new_peak = fft_peak(start, freq, amp, N)
            frame.append(new_peak)

        return frame

    def _parabolic_bin_to_pitch(self, k_star, fft_r, N, zpf):
        #          fft_r, real fft, kstar is bin index of peak
        y0 = abs(fft_r[k_star])
        yn1 = abs(fft_r[k_star - 1])
        y1 = abs(fft_r[k_star + 1])

        p = (yn1 - y1) / (2.0 * (yn1 - 2 * y0 + yn1))
        est_peak = k_star + p
        freq = est_peak * self.fs / (N * zpf)

        amp = 0.5 * (yn1 - 2 * y0 + y1)

        return freq, amp

    def _two_way_mismatch(
        self,
        peaks: List[fft_peak],
        f0_range: Tuple[int, int],
        reverb: bool = True,
        p: float = DEFAULT_P,
        q: float = DEFAULT_Q,
        r: float = DEFAULT_R,
    ):
        """ p q r weird coefficients
            figure the difference between the measured(peaks passed in) to ideal 
            (predicted) and vice versa
        """

        A_max = max(peaks, key=lambda x: x.amp)[2]

        # Guesses for the fundamental frequency of this frame.
        if isinstance(f0_range, list):
            # we guess the things in the list
            f0_guesses = f0_range

        elif isinstance(f0_range, tuple):
            # lowest and highest indicies of twelvetet
            f0_guesses = TWELVETET[f0_range[0] : f0_range[1]]

        Err_total_list = []

        num_partials = DEFAULT_NUM_PARTIALS

        for guess in f0_guesses:

            if len(peaks) > num_partials:
                K = num_partials
                peaks = peaks[:num_partials]
            else:
                K = len(peaks) + 1

            Err_p_m, Err_m_p = 0, 0

            otg = self._overtone_generator(guess)

            predicted_spectrum = [next(otg) for x in range(num_partials)]

            if num_partials > 0:
                reported_peaks_with_amp = [
                    freq_amp_pair(this_peak.freq, this_peak.amp) for this_peak in peaks
                ]
                # Measured to predicted.
                mtp_mean = self._measured_to_ideal_mismatch(
                    reported_peaks_with_amp, predicted_spectrum, num_partials
                )
                mtp_min_distance = min(mtp_mean, key=lambda x: x.distance)

                for this_mean in mtp_mean:
                    fn = this_mean.freq
                    delta_fn = abs(this_mean.distance)
                    if abs(mtp_min_distance.distance) == delta_fn:
                        A_n = A_max
                    else:
                        A_n = this_mean.amp
                    Err_p_m += delta_fn * pow(fn, -p) + (A_n / A_max) * (
                        q * delta_fn * pow(fn, -p) - r
                    )

                # Predicted to measured.
                ptm_mean = self._ideal_to_measured_mismatch(
                    reported_peaks_with_amp, predicted_spectrum
                )

                for k, mean in enumerate(ptm_mean):
                    fk = abs(peaks[k].freq)
                    delta_fk = mean
                    if delta_fk == min(ptm_mean):
                        A_k = A_max
                    else:
                        A_k = peaks[k].amp
                    Err_m_p += delta_fk * pow(fk, -p) + (A_k / A_max) * (
                        q * delta_fk * pow(fk, -p) - r
                    )

            if reverb:
                Err_total = Err_p_m / num_partials + (0.5 * Err_m_p) / K
            else:
                Err_total = Err_p_m / num_partials + (0.33 * Err_m_p) / K

            Err_total_list.append((Err_total, guess))

        thing = min(Err_total_list, key=lambda x: x[0])[1]

        return thing

    def _overtone_generator(self, f0):
        starting_freq = f0
        overtone = f0
        while True:
            yield overtone
            overtone = starting_freq + f0
            starting_freq = overtone

    def _get_fractional_beats(self, num_samples: int, note_value: float) -> float:
        return ((num_samples * note_value)/HOP_SIZE) / DEFAULT_SAMPLING_RATE

    def _get_pitch(self, freq):
        rounded_pitch = round(12 * log2(freq / C0))
        octave = rounded_pitch // 12
        pc = rounded_pitch % 12
        return octave, pc

    def _get_frequency_range(self, idx, ideal_spectrum, num_partials):
        """
        Get limits of range around a frequency in a spectrum.

        Args:
            idx: current index
            ideal_spectrum: the spectrum to get ranges on
            num_partials: max_partials to consider

        Returns:
            tuple: (int, int) range
        """
        partial_frequency = ideal_spectrum[idx]
        if idx == 0:
            last_distance = 0
            next_distance = partial_frequency + (
                (ideal_spectrum[idx + 1] - partial_frequency) / 2
            )
            tracking_range = (last_distance, next_distance)
        elif idx == (num_partials - 1):
            last_distance = partial_frequency + (
                (partial_frequency - ideal_spectrum[idx - 1]) / 2
            )
            next_distance = self.fs / 2
            tracking_range = (last_distance, next_distance)
        elif idx > 0:
            last_distance = partial_frequency - (
                (partial_frequency - ideal_spectrum[idx - 1]) / 2
            )
            next_distance = partial_frequency + (
                (ideal_spectrum[idx + 1] - partial_frequency) / 2
            )
            tracking_range = (last_distance, next_distance)
        return tracking_range

    def _measured_to_ideal_mismatch(self, reported_peaks, ideal_spectrum, num_partials):
        closest_peaks = []
        for idx, partial_frequency in enumerate(ideal_spectrum):
            frequency_range = self._get_frequency_range(
                idx, ideal_spectrum, num_partials
            )
            candidate_partials_with_amps = [
                (partial[0], partial[1])
                for partial in reported_peaks
                if frequency_range[0] < partial[0] < frequency_range[1]
            ]
            # impossible distance and index to get overwritten by first partial, regardless of distance
            if candidate_partials_with_amps:
                for idx, partial in enumerate(candidate_partials_with_amps):
                    distance = mtp_peak(
                        partial[0], partial_frequency - partial[0], partial[1]
                    )
                closest_peaks.append(distance)
        return closest_peaks

    def _ideal_to_measured_mismatch(self, peaks, ideal_spectrum):
        reported_peaks = peaks
        if ideal_spectrum:
            differences = list(
                map(
                    lambda x: abs(
                        x.freq - min(ideal_spectrum, key=lambda y: abs(x.freq - y))
                    ),
                    reported_peaks,
                )
            )
            return differences
        else:
            return [0]

    def smooth_notes(self, note_list: List[Note], N: int):
        one_frame_indices = []
        one_frame_dur = self._get_fractional_beats(N, 1)
        for idx, note in enumerate(note_list):
            if note.dur == one_frame_dur:
                one_frame_indices.append(idx)

        return one_frame_indices

    def get_score(self, time_signature: TimeSignature, n_parts: int) -> Score:
        """
        Get a Score that is auto-transcribed from a soundfile.

        Args:
            time_signature: a TimeSignature
            n_parts: number of parts to return
        """
        part_list = []
        for partial in self.partials[:n_parts]:
            part = partial.convert_list_to_part(time_signature)
            part_list.append(part)
        return Score(part_list)
