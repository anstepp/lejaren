# *lejaren*
Computer-Aided Musical Prototyping in Python

![](https://github.com/anstepp/lejaren/workflows/tests/badge.svg)

*lejaren* has replaced [Py2MusicXML](https://github.com/anstepp/py2musicxml).

## What does *lejaren* do?

This python library is designed for compositional tasks. There's a handful of notation-based objects (Score, Note, etc.) that interact. You can then manipulate these objects in Python to create "music." You can spit out the notation of what you created into MusicXML, and notation software will open it (and it might be useful!).

## What can *lejaren* do for you?

Well, what do you want it to do? Things that can be good uses:

- Write a piece of music using Python
- Import MusicXML to do algorithmic procedures on your input file
- Design a machine learning algorithm to analyze your an input file
- "Translate" a non-musical idea into Python, then into *lejaren*

The advantages lie in the following aspects incorporated into *lejaren*:

* Python, with it's data friendly format
* MusicXML, as a score interchange project
* An open-ended, object-oriented approach - use existing musical objects in custom ones

And more...

## Ok, I'm hooked. How do I *lejaren* like a pro?

[[There will be a pip install soon... stay tuned...]]

If you're a music person, more than a programmer person, I recommend you look into venv as a way to work on *lejaren* (or Python) projects. It really can help a lot.

Clone this repository. Use a local pip...

```shell
cd [path/to/lejaren]
pip install .
```

The package management should do a great job getting any prerequisites.

Now we can hack some *lejaren*!

Create a Python file... it should end in .py. In the file, the "Hello, World!" of *lejaren* can be typed thusly:

```python
from lejaren.notation import Note, Part, Score

middle_c = Note(4,4,0)
time_signature = [(4,4)]
note_list = [middle_c]
our_first_part = Part(note_list, time_signature)
our_first_score = Score([our_first_part])
```

Bam! Middle C!

If you want to get a file you can *see* the middle C in...

```python
from lejaren.notation import Note, Part, Score

middle_c = Note(4,4,0)
time_signature = [(4,4)]
note_list = [middle_c]
our_first_part = Part(note_list, time_signature)
our_first_score = Score([our_first_part])

our_first_score.convert_to_xml("path/to/output.musicxml")
```

You can open the MusicXML in your favorite flavor of notation/engraving software.

## So, I love *lejaren* so much I have a billion ideas to improve it.

Great! I love it! And, I want them!

Here's the thing - it's just me (passion project!), and I probably can't make your request happen *just because*.

You'd be welcome to create a pull request for a feature! Just request access, and I'm happy to review.