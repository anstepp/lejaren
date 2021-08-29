import pathlib

import streamlit as st

APP_DIR = pathlib.Path(__file__).parents[1]
IMAGE_DIR = APP_DIR / "pages" / "images"


def main():
    st.header("Tutorial Two: Major Scales")

    st.markdown("""The following code produces a major scale.""")

    with st.echo():
        from lejaren.notation import Note, Part, Score

        duration = 1
        octave = 4

        note_list = []

        major_scale = [0, 2, 4, 5, 7, 9, 11, 12]

        for pc in major_scale:
            note_list.append(Note(duration, octave, pc))

        time_signature = [(4, 4)]

        part = Part(note_list, time_signature)

        score = Score([part])

        score.convert_to_xml("diatonic_scale.musicxml")

    st.image(str(IMAGE_DIR / "c_major.jpeg"))

    st.markdown(
        """Some of this will look familiar from the Hello, World tutorial.
    The main difference is this bit of code:"""
    )

    with st.echo():
        major_scale = [0, 2, 4, 5, 7, 9, 11, 12]

        for pc in major_scale:
            note_list.append(Note(duration, octave, pc))

    st.markdown(
        """In this code, we have a list of pitch classes that constitute a
    major scale in the `major_scale` variable. The `for` loop iterates through the
    `major_scale` list, and with each iteration the corresponding `pc` variable is
    used to create a `Note` object that is appended to `note_list`."""
    )

    st.markdown(
        """Note that we've hard-coded the pitch classes. We could start on
    another pitch by offsetting to these pitches. This would produce an E flat major
    scale."""
    )

    with st.echo():
        major_scale = [0, 2, 4, 5, 7, 9, 11, 12]

        starting_pitch = 3

        for pc in major_scale:
            note_list.append(Note(duration, octave, pc + starting_pitch))

    st.markdown(
        """We could generalize this procedure to define a function to produce
    our major scale."""
    )

    st.markdown("""For instance:""")

    # fmt:off
    with st.echo():
        def major_scale_creator(octave, starting_pitch):
            dur = 1
            major_scale = [0, 2, 4, 5, 7, 9, 11, 12]
            scale_list = []

            for pc in major_scale:
                scale_list.append(Note(dur, octave, starting_pitch + pc))

            return scale_list
    # fmt:on

    st.markdown(
        """This function could then be called to create the major scale
    with more specificity than when the pitch classes were hard coded. Like so:"""
    )

    with st.echo():
        e_flat_major = major_scale_creator(4, 3)

    st.image(str(IMAGE_DIR / "e_flat_major.jpeg"))

    st.markdown("""Explore Tutorial Three for another way of building a Major Scale.""")
