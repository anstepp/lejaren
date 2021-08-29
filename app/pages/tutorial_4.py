import pathlib

import streamlit as st

APP_DIR = pathlib.Path(__file__).parents[1]
IMAGE_DIR = APP_DIR / "pages" / "images"


def main():
    st.header("Tutorial Four: *Sogetto Cavato*")

    st.subheader("What is *Sogetto Cavato*?")

    st.markdown(
        """Composer [Josquin des Prez](https://en.wikipedia.org/wiki/Josquin_des_Prez)
        explored using [solfège](https://en.wikipedia.org/wiki/Solfège]) syllables 
        to create words in music, a practice he called *sogetto cavato*."""
    )

    st.markdown(
        """A famous example is his work
        [Vive le roi](https://imslp.org/wiki/Vive_le_Roy_(Josquin_Desprez)), where in
        he transliterates "Long live the king" (*vive le roi*) into solfège syllables.
        If we were contemporaries of Josquin, instead of *do* for the tonic pitch,
        we would use *ut*, which stands in for the 'v' in *vive le roi*.
        If we translate that into notation:"""
    )

    st.image(str(IMAGE_DIR / "vive_le_roi.jpeg"))

    st.markdown(
        """This sequence of pitches is then used as the *cantus firmus* for
        *Vive le roi*."""
    )

    st.subheader("Creating *Sogetto Cavato* in lejaren")

    st.markdown(
        """*Sogetto cavato* translates text into notation. As Python can do this task,
        we can create a little bit of software that will translate a string into
        notation. This is handy, in no small part because we can make it reusable,
        but because it offers us possibilities for other things to translate."""
    )

    st.markdown("**Dictionaries**")

    st.markdown(
        """In Python, there's a data type called a dictionary that is comprised of
        *key* and *value* pairs. It's sort of like a phone book - there's the key,
        or the person you're trying to call, and there's the value, the phone number.
        There are lots of other ways to look at this too, one of which could be a key,
        or a note, and a value, or letters that could be represented by that note."""
    )

    st.markdown(
        """A simple dictionary that would complete Josquin's task above would be like
        this, using set theory numbers for the pitch values:"""
    )

    with st.echo():
        sc_dict = {
            "v": 0,
            "e": 2,
            "i": 4,
            "o": 7,
        }

    st.markdown(
        """We can then create a little logic to make sure we're skipping letters that
        aren't in the list of keys."""
    )

    with st.echo():
        solfege_vowels = []

        for key in sc_dict.keys():
            solfege_vowels.append(key)

    st.markdown(
        """We can then write a function that will take a string, and translate it to
        a list of pitch classes."""
    )

    # fmt:off
    with st.echo():
        def convert_to_sogetto(string_to_convert):
            sc_dict = {
                'v': 0,
                'e': 2,
                'i': 4,
                'o': 7,
            }
            solfege_vowels = []

            for key in sc_dict.keys():
                solfege_vowels.append(key)

            pc_list = []
            for letter in string_to_convert:
                if letter in solfege_vowels:
                    pc_to_add = sc_dict[letter]
                    pc_list.append(pc_to_add)

            return pc_list
    # fmt:on

    st.markdown("""We can then call this function, passing in our string:""")

    with st.echo():
        vlr = "viveleroi"

        vive_pc = convert_to_sogetto(vlr)

    st.markdown(
        """And then convert, using `lejaren`, into an xml document with a
        *cantus firmus* from this conversion process."""
    )

    with st.echo():
        from lejaren.notation import Note, Part, Score

        vive_note_list = []

        for pc in vive_pc:
            vive_note_list.append(Note(4, 4, pc))

        time_sig = [(2, 2)]

        vive_cantus_firmus = Part(vive_note_list, time_sig)

        vive_score = Score([vive_cantus_firmus])

        vive_score.convert_to_xml("viveleroi.musicxml")

    st.markdown("""Opening in engraving software would lead to this result:""")

    st.image(str(IMAGE_DIR / "vive_cantus.jpeg"))

    st.markdown(
        """Tutorial Five takes the *sogetto cavato* idea to even more abstraction!"""
    )
