import streamlit as st
import lejaren as lj

st.header("lejaren AutoTranscriber")

st.markdown("""`lejaren` is a Python library that enables Computer-Aided Composition 
and musical prototpying. [Check out the lejaren repo here](https://github.com/anstepp/lejaren).""")

st.markdown("We start by creating an `AutoTranscribe` object.")

audio_file_name = st.selectbox(
    "Select the audio file for transcription:",
    ("violinclip1.wav", "y2monoChunk.wav"))

audio_filepath = f"app/samples/{audio_file_name}"
audio_file = open(audio_filepath, "rb")
audio_bytes = audio_file.read()

st.audio(audio_bytes, format="audio/wav")

st.slider("F0 Range", 12, 72, (24, 36))

with st.echo():
    # Define FFT size and tempo.
    fft_size = 2048
    tempo = lj.notation.Tempo(60, 1)

    # Create the AutoTranscribe object and give it the audio file.
    transcriber = lj.analysis.AutoTranscribe(fft_size, tempo)
    transcriber._supply_audio(audio_filepath)

    # Use the transcriber, along with a guessed pitch range,
    # to generate the audio file notes.
    f0_range = (24, 48)
    resulting_pitches = transcriber.get_note_list(f0_range)

st.markdown("**`resulting_pitches`**:")
for pitch in resulting_pitches:
    st.write(pitch)