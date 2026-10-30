XML_NOTE_ORDER = (
"grace", #(Required)
# Exactly one of the following
# In this order
# In this order
"chord", #(Optional)
#Exactly one of the following
"pitch",
"unpitched",
"rest",
"tie", #(0 to 2 times)
#In this order
"cue", #(Required)
#In this order
"chord", #(Optional)
#Exactly one of the following
"pitch",
"unpitched",
"rest",
#In this order
"cue", #(Required)
#In this order
"chord", #(Optional)
#Exactly one of the following
"pitch",
"unpitched",
"rest",
"duration", #(Required)
#In this order
#In this order
"chord", #(Optional)
#Exactly one of the following
"pitch",
"unpitched",
"rest",
"duration", #(Required)
"tie", #(0 to 2 times)
"instrument", #(Zero or more times)
#In this order
"footnote", #(Optional)
"level", #(Optional)
"voice", #(Optional)
"type", #(Optional)
"dot", #(Zero or more times)
"accidental", #(Optional)
"time-modification", #(Optional)
"stem", #(Optional)
"notehead", #(Optional)
"notehead-text", #(Optional)
"staff", #(Optional)
"beam", #(0 to 8 times)
"notations", #(Zero or more times)
"lyric", #(Zero or more times)
"play", #(Optional)
"listen", #(Optional)
)

XML_MEASURE_ATTRIBUTE_ORDER = (
#In this order
"footnote", #(Optional)
"level", #(Optional)
"divisions", #(Optional)
"key", #(Zero or more times)
"time", #(Zero or more times)
"staves", #(Optional)
"part-symbol", #(Optional)
"instruments", #(Optional)
"clef", #(Zero or more times)
"staff-details", #(Zero or more times)
#Exactly one of the following
"transpose", #(Zero or more times)
"for-part", #(Zero or more times)
"directive", #(Zero or more times)
"measure-style", #(Zero or more times)

)