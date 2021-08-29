import pathlib

import streamlit as st

APP_DIR = pathlib.Path(__file__).parents[1]
IMAGE_DIR = APP_DIR / "pages" / "images"


def main():
    st.header("Tutorial One: Hello, World!")

    st.write(
        "The below code will output a MusicXML file that contains just a Middle C."
    )

    with st.echo():
        from lejaren.notation import Note, Part, Score

        duration = 4
        octave = 4
        pitch_class = 0

        middle_c = Note(duration, octave, pitch_class)

        time_signature = [(4, 4)]

        our_part = Part([middle_c], time_signature)

        our_score = Score([our_part])

        our_score.convert_to_xml("middle_c.musicxml")

    st.markdown(
        """Each line does something unique that allows us to create our
    importable MusicXML file. We can walk through each line together."""
    )

    st.markdown(
        """This line is an import statement that is used to give our script
    access to the `Note`, `Part`, and `Score` objects from the `lejaren.notation`
    namespace."""
    )

    with st.echo():
        from lejaren.notation import Note, Part, Score

    st.markdown(
        """Without this line, we can't use `lejaren`! It is also important to
    note we're not importing all of `lejaren`, just the three objects we need for this
    score. If you wanted to, you could import other libraries here, but we don't need any."""
    )

    st.markdown("""On the next three lines:""")

    with st.echo():
        duration = 4
        octave = 4
        pitch_class = 0

    st.markdown(
        """we declare three variables called `duration`, `octave`, and
    `pitch_class`. We assign them values that are integers. Each value represents
    something musically. In `lejaren`, a duration of 1 represents a quarter note.
    So, we assign a 4 to `duration` to get a whole note. `lejaren` handles all that
    under the hood - you don't have to worry about how, just that if you want a
    duration, relate it to a quarter note = 1. We assign a 4 to `octave`,
    and a `pitch_class` of 0. `lejaren` uses [scientific pitch notation](https://en.wikipedia.org/wiki/Scientific_pitch_notation)
    for the octave, and musical set theory pitch class notation."""
    )

    st.markdown("""The next line is where things get good.""")

    with st.echo():
        middle_c = Note(duration, octave, pitch_class)

    st.markdown(
        """This is where we create a Note using `lejaren`. Congratulations!
    In this case, we just create a Middle C, just one note. Notice that the `Note`
    object has three variables in the parenthesis where we call it, called `duration`,
    `octave`, and `pitch_class`. These are the three variables we just declared in
    the previous bit of code. This is convenient, so we can remember what goes where.
    We could name them whatever we want (which could be very useful!), just as long as
    the arguments supplied to create a note are always in this order:
    duration`, octave, and pitch class."""
    )

    st.markdown("""Next we make a time signature.""")

    with st.echo():
        time_signature = [(4, 4)]

    st.markdown("""The following code:""")

    with st.echo():
        our_part = Part([middle_c], time_signature)

    st.markdown(
        """We create a `Part` from a list of `Note`s. In this case, we just
    have one note, `middle_c`, that we enclose in brackets `[]`, with is Python
    shorthand for a list. If we had more notes (or, better, a preexisting list of
    notes), we could feed them all in like this. The cool bit here is that `lejaren`
    will break everything into measures for you. It will cycle endlessly through the
    time signatures we feed it."""
    )

    st.markdown(
        """Just like creating a `Part` and using a list of `Note`s, we create
    a `Score` with a list of `Part`s."""
    )

    with st.echo():
        our_score = Score([our_part])

    st.markdown(
        """Now, there's a `Score` object called `our_score`. To convert this
    score to MusicXML, there's a method we call on it with dot notation like so:"""
    )

    with st.echo():
        our_score.convert_to_xml("middle_c.musicxml")

    st.markdown(
        """The argument is the filename we want python to create and fill
    with the MusicXML."""
    )

    st.markdown(
        """If you are to open the `middle_c.musicxml` file in engraving software,
    you'll get the following:"""
    )

    st.image(str(IMAGE_DIR / "middle_c.jpeg"))

    st.markdown(
        """Continue on to Tutorial Two for instructions on how to complete a Major Scale."""
    )
