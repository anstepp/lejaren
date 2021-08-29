import pathlib

import streamlit as st

APP_DIR = pathlib.Path(__file__).parents[1]
AUDIO_DIR = APP_DIR / "samples"


def main():
    st.header("AutoTranscriber")

    st.markdown(
        """The AutoTranscriber allows you to take a monophonic `.wav` file and
        transcribe the pitch into `lejaren` `Note` objects. More generally, this means
        that you can take a melody and convert it into musical notation."""
    )

    st.markdown(
        """We'll start by importing `lejaren` and selecting a sample file.
    The `F0` range, which serves as the "best guess" of heard pitch of the sound,
    is prepopulated for each sample."""
    )

    with st.echo():
        import lejaren as lj

    audio_file_name = st.selectbox(
        "Select the audio file for transcription:",
        ("violinclip1.wav", "y2monoChunk.wav"),
    )

    audio_filepath = AUDIO_DIR / audio_file_name
    audio_file = open(audio_filepath, "rb")
    audio_bytes = audio_file.read()

    st.audio(audio_bytes, format="audio/wav")

    f0_map = {"violinclip1.wav": (24, 48), "y2monoChunk.wav": (27, 37)}

    f0_range = f0_map[audio_file_name]
    st.markdown(f"`f0_range = {f0_range}`")

    st.markdown(
        """To use the AutoTranscriber, we create a `lejaren` `AutoTranscribe` object
        and initialize it with a FFT size and `Tempo`. We then supply the selected
        audio sample to the transcriber and smooth the resulting transcribed notes."""
    )

    with st.echo():
        # Define FFT size and tempo.
        fft_size = 2048
        tempo = lj.notation.Tempo(60, 1)

        # Create the AutoTranscribe object and give it the audio file.
        transcriber = lj.analysis.AutoTranscribe(fft_size, tempo)
        transcriber._supply_audio(audio_filepath)

        # Use the transcriber, along with a guessed pitch range,
        # to generate the audio file notes.
        resulting_pitches = transcriber.get_note_list(f0_range)

        smoothed_and_quantized = transcriber.smooth_notes(resulting_pitches, fft_size)

    st.markdown(
        """Below, you can view the resulting `lejaren` `Note` objects (one per line)
        that were transcribed from the sample audio file. Currently, these notes are
        simply displayed as `lejaren` objects, but in the future I plan to implement
        the ability to display notes visually as music notation."""
    )

    for pitch in smoothed_and_quantized:
        st.write(pitch)
