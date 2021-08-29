import pathlib

import streamlit as st

APP_DIR = pathlib.Path(__file__).parents[1]
IMAGE_DIR = APP_DIR / "pages" / "images"


def main():
    st.header("Tutorial Three: Major Scales, Another Way")

    st.markdown(
        """In Tutorial Two, we built a major scale by hard coding the
    pitch classes from a C. We concluded by writing a function that would return a
    list of notes that was a major scale, based on our selected starting pitch."""
    )

    st.markdown(
        """There are more sophisticated ways of creating series of pitches,
    namely by using intervals. In this manner, we can create more abstract
    representations of compositional content, allowing for more complex uses.
    This is, in essence, the founding principle of `lejaren` - prototyping for
    compositional purposes."""
    )

    st.markdown(
        """Below is the previous tutorial code, rewritten to instead focus
    on interval instead of direct pitch classes."""
    )

    with st.echo():
        from lejaren.notation import Note, Part, Score

        duration = 1
        octave = 4

        note_list = []

        major_scale_intervals = [2, 2, 1, 2, 2, 2, 1]

        pc = 0

        for interval in major_scale_intervals:
            pc += interval
            note_list.append(Note(duration, octave, pc))

        time_signature = [(4, 4)]

        part = Part(note_list, time_signature)

        part_list = [part]

        score = Score(part_list)

        score.convert_to_xml("diatonic_scale.musicxml")

    st.image(str(IMAGE_DIR / "c_major.jpeg"))

    st.markdown(
        """The big changes from Tutorial Two are the `major_scale_intervals`
    and the `for` loop."""
    )

    st.markdown(
        """The list `major_scale_intervals`, instead of containing the pitch
    classes for a C major scale, instead consist of distances - whole or half steps.
    In this case, we will be procedurally following these distances by altering the
    `pc` variable in the `for` loop that follows."""
    )

    st.markdown(
        """The `for` loop is similar to the loop in Tutorial Two, but instead
    of simply substituting the values of the major scale pitch classes, we increase
    the `pc` variable by the distance of the current value in the
    `major_scale_intervals` variable, as seen below."""
    )

    with st.echo():
        pc = 0

        for interval in major_scale_intervals:
            pc += interval
            note_list.append(Note(duration, octave, pc))

    st.markdown(
        """Just as in Tutorial Two, abstracting this loop into a function
    allows for more variability and use cases."""
    )

    # fmt:off
    with st.echo():
        def create_major_scale(starting_pc):
            duration = 1
            octave = 4

            scale = []

            pc = starting_pc

            major_scale_intervals = [2, 2, 1, 2, 2, 2, 1]

            for interval in major_scale_intervals:
                pc += interval
                scale.append(Note(duration, octave, pc))

            return scale
    # fmt:on

    st.image(str(IMAGE_DIR / "e_flat_major.jpeg"))

    st.markdown(
        """Encapsulating the major scale function like this allows for more expansive
    uses if one continues to abstract what is possible in the function."""
    )

    # fmt:off
    with st.echo():
        def create_scale(starting_pc, intervals):
            duration = 1
            octave = 4
            pc = starting_pc

            scale = []

            for interval in intervals:
                pc += interval
                scale.append(Note(duration, octave, pc))

            return scale

        octatonic = [0, 1, 2, 1, 2, 1, 2]
        pentatonic = [0, 2, 2, 3, 2, 3]

        octatonic_scale = create_scale(0, octatonic)
        pentatonic_scale = create_scale(0, pentatonic)
    # fmt:on

    st.image(str(IMAGE_DIR / "octatonic_pentatonic.jpeg"))

    st.markdown(
        """Abstraction like this can be used to generate more sophisticated
    musical structures, such as *Sogetto Cavato*, as seen in Tutorial Four."""
    )
