import pathlib

import streamlit as st

APP_DIR = pathlib.Path(__file__).parents[1]
IMAGE_DIR = APP_DIR / "pages" / "images"


def main():
    st.header("Tutorial Five: More *Sogetto Cavato*, with Conditions")

    st.subheader("Introduction")

    st.markdown(
        """In Tutorial Four, we created a function that would return solfège from the
        vowels in a string."""
    )

    st.markdown(
        """In this tutorial, we'll add some conditions to our function. These
        conditions will help to accommodate other possibilities and situations that
        might come up. Even though it's more code, it's code that can produce more
        interesting results, as well as deal with situations we couldn't anticipate
        in the previous tutorial."""
    )

    st.subheader("What Conditions Exist?")

    st.markdown(
        """In our previous example, we could only deal with the *sogetto cavato*
        directly used in Josquin's *Vive le roi*. In effect, the code written only
        deals with four conditions, mapped to the four notes in the *cantus firmus*.
        Those letters are 'v,' 'e,' 'i,' and 'o.' Even though we can render a
        *Vive le roi*, there's plenty of letters left in the alphabet we haven't dealt
        with, not to mention non-letter parts of strings like spaces and periods."""
    )

    st.markdown(
        """For now, let's keep things simple, and focus just on the possibilities for
        solfège. If we keep the "ut" for "do," and ignore "ti" (as Josquin didn't have
        a "ti" to work with), we'd have these possible vowels (plus 'v'):"""
    )

    with st.echo():
        solefge_list = ["a", "e", "i", "o", "u", "v"]

    st.markdown(
        """The fact that these map to our vowels isn't an accident. But wait! If we go
        through solfège, we have "do, re, mi, fa, sol, la" - two 'a' situations!"""
    )

    st.markdown(
        """We can totally address this in the code. The good news is that Python
    dictionaries don't let you have two identical key values. This is great for
    solving the problem, but we still have two possible interpretations of translating
    'a' to a note."""
    )

    st.markdown(
        """This is where using conditions can help. We can create a "fa" and a "la"
    in our list, and use some programming to accommodate having both these conditions."""
    )

    st.markdown(
        """And, as we move on to dealing with these conditions, we should note we
        already used a condition in the previous tutorial! This line of code:"""
    )

    # fmt:off
    st.markdown(
        """```
if letter in solfege_vowels:
```"""
    )
    # fmt:on

    st.markdown(
        """Evaluates if the letter is one we can deal with. Let's make this more
        sophisticated and have more options."""
    )

    st.subheader("The New Solfège Dictionary")

    st.markdown(
        """Our new dictionary with all the possibilities would look something like this:"""
    )

    with st.echo():
        solefge_dict = {
            "u": 0,
            "v": 0,
            "e": 2,
            "i": 4,
            "fa": 5,
            "o": 7,
            "la": 9,
        }

    st.markdown(
        """Now, we've dealt with the fact we could have 'fa' or 'la'. There's a problem,
    though. The previous tutorial code that iterates through the string iterates through
    each letter individually. It will never return a `5` or `9` because the keys are
    two letters long. Therefore, our previous tutorial will need adjustments to
    accommodate our two letter strings `fa` and `la`."""
    )

    st.markdown("**Concatenating to Produce 2-letter Strings**")

    st.markdown(
        """Python is nice and has overloaded operators for math symbols. It's fun
        because we can "add" two strings together to get a longer string. Super fun.
        So, adding 'l' and 'a' will give us 'la'. This is great, because it's exactly
        what we need. In action:"""
    )

    with st.echo():
        l = "l"
        a = "a"

        la = l + a

    st.markdown("**Indexing to Get Other Locations in an Iteration**")

    st.markdown(
        """Python allows us simply to iterate over any iterable data type. This is nice,
        but sometimes we need an index to solve some problems. To allow this, Python
        has an `enumerate` function that will allow access to the indices."""
    )

    st.markdown("""To use `enumerate` we simply add it to a loop, like so:""")

    # fmt:off
    st.markdown("""```
vlr = "viveleroi"

for idx, letter in enumerate(vlr):
    print(idx, letter)
```""")

    st.markdown(
        """This will print this:
```
    0, 'v'
    1, 'i'
    2, 'v'
    3, 'e'
    4, 'l'
    5, 'e'
    6, 'r'
    7, 'o'
    8, 'i'
```"""
    )
    # fmt:on

    st.subheader("Combining `enumerate` and Concatenation")

    st.markdown(
        """If we combine both of the last bits of code, we can create a function that
        will iterate over a string, and return a plus whatever letter comes before it."""
    )

    with st.echo():
        from lejaren.notation import Note, Part, Score

        vlr = "viveleroi"

        solefge_dict = {
            "u": 0,
            "v": 0,
            "e": 2,
            "i": 4,
            "fa": 5,
            "o": 7,
            "la": 9,
        }

        solfege_vowels = []

        for key in solefge_dict.keys():
            solfege_vowels.append(key)

        def modified_get_cantus_firmus(string_to_convert):
            note_list = []
            for idx, letter in enumerate(string_to_convert):
                if letter == "a" and idx != 0:
                    concat_letter = string_to_convert[idx - 1] + letter
                    note_list.append(
                        Note(
                            duration=4,
                            octave=4,
                            pitch_class=solefge_dict[concat_letter],
                        )
                    )
                elif letter in solfege_vowels:
                    note_list.append(
                        Note(duration=4, octave=4, pitch_class=solefge_dict[letter])
                    )
                else:
                    pass

            return note_list

        vlr_note_list = modified_get_cantus_firmus(vlr)

        time_sig = [(2, 2)]

        vlr_part = Part(vlr_note_list, time_sig)

        vlr_score = Score([vlr_part])

        vlr_score.convert_to_xml("vlr_cantus_firmus.musicxml")

    st.markdown("""The result will be the same as our previous tutorial:""")

    st.image(str(IMAGE_DIR / "vive_cantus.jpeg"))

    st.markdown(
        """Of course, the *Vive le roi* letters don't use our new code!
    Let's try some letters that will invoke our code."""
    )

    with st.echo():
        from lejaren.notation import Note, Part, Score

        vlr = "landolakes"

        solefge_dict = {
            "u": 0,
            "v": 0,
            "e": 2,
            "i": 4,
            "fa": 5,
            "o": 7,
            "la": 9,
        }

        solfege_vowels = []

        for key in solefge_dict.keys():
            solfege_vowels.append(key)

        def modified_get_cantus_firmus(string_to_convert):
            note_list = []
            for idx, letter in enumerate(string_to_convert):
                if letter == "a" and idx != 0:
                    concat_letter = string_to_convert[idx - 1] + letter
                    note_list.append(
                        Note(
                            duration=4,
                            octave=4,
                            pitch_class=solefge_dict[concat_letter],
                        )
                    )
                elif letter in solfege_vowels:
                    note_list.append(
                        Note(duration=4, octave=4, pitch_class=solefge_dict[letter])
                    )
                else:
                    pass

            return note_list

        vlr_note_list = modified_get_cantus_firmus(vlr)

        time_sig = [(2, 2)]

        vlr_part = Part(vlr_note_list, time_sig)

        vlr_score = Score([vlr_part])

        vlr_score.convert_to_xml("vlr_cantus_firmus.musicxml")

    st.markdown(
        """We can, just like Josquin, write a mass based on a text. In our case,
        we're using delicious cream and dairy products. But, if we run this code,
        we'll get this as a result:"""
    )

    st.image(str(IMAGE_DIR / "sc_landolakes.jpeg"))

    st.markdown(
        """I'll leave it as a task for the reader to decide how to deal with an 'a'
        without and 'f' or 'l' before it, and how to write that code. So many
        possibilities!"""
    )
