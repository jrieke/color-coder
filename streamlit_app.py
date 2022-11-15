import re

import streamlit as st


def icon(emoji: str):
    """Shows an emoji as a Notion-style page icon."""
    st.write(
        f'<span style="font-size: 78px; line-height: 1">{emoji}</span>',
        unsafe_allow_html=True,
    )


st.set_page_config("Color-code your writing", "🌈")

icon("🌈")
st.title("Color-code your writing")
st.write(
    """
    Just add some text below and this app will color-code it based on sentence length. 
    Good texts vary the sentence length, so they should have <span style="background-color: #F8F4C6">lots</span> <span style="background-color: #FAD1F0">of</span> <span style="background-color: #C8F6C9">colors</span>! 
    """,
    unsafe_allow_html=True,
)

sample_text = """This sentence has five words. Here are five more words. Five-word sentences are fine. But several together become monotonous. Listen to what is happening. The writing is getting boring. The sound of it drones. It’s like a stuck record. The ear demands some variety. 

Now listen. I vary the sentence length, and I create music. Music. The writing sings. It has a pleasant rhythm, a lilt, a harmony. I use short sentences. And I use sentences of medium length. And sometimes, when I am certain the reader is rested, I will engage him with a sentence of considerable length, a sentence that burns with energy and builds with all the impetus of a crescendo, the roll of the drums, the crash of the cymbals–sounds that say listen to this, it is important.

So write with a combination of short, medium, and long sentences. Create a sound that pleases the reader's ear. Don't just write words. Write music."""

# From https://stackoverflow.com/a/31505798
alphabets = "([A-Za-z])"
prefixes = "(Mr|St|Mrs|Ms|Dr)[.]"
suffixes = "(Inc|Ltd|Jr|Sr|Co)"
starters = "(Mr|Mrs|Ms|Dr|He\s|She\s|It\s|They\s|Their\s|Our\s|We\s|But\s|However\s|That\s|This\s|Wherever)"
acronyms = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
websites = "[.](com|net|org|io|gov)"
digits = "([0-9])"


def split_into_sentences(text):
    text = " " + text + "  "
    text = text.replace("\n", " ")
    text = re.sub(prefixes, "\\1<prd>", text)
    text = re.sub(websites, "<prd>\\1", text)
    text = re.sub(digits + "[.]" + digits, "\\1<prd>\\2", text)
    if "..." in text:
        text = text.replace("...", "<prd><prd><prd>")
    if "Ph.D" in text:
        text = text.replace("Ph.D.", "Ph<prd>D<prd>")
    text = re.sub("\s" + alphabets + "[.] ", " \\1<prd> ", text)
    text = re.sub(acronyms + " " + starters, "\\1<stop> \\2", text)
    text = re.sub(
        alphabets + "[.]" + alphabets + "[.]" + alphabets + "[.]",
        "\\1<prd>\\2<prd>\\3<prd>",
        text,
    )
    text = re.sub(alphabets + "[.]" + alphabets + "[.]", "\\1<prd>\\2<prd>", text)
    text = re.sub(" " + suffixes + "[.] " + starters, " \\1<stop> \\2", text)
    text = re.sub(" " + suffixes + "[.]", " \\1<prd>", text)
    text = re.sub(" " + alphabets + "[.]", " \\1<prd>", text)
    if "”" in text:
        text = text.replace(".”", "”.")
    if '"' in text:
        text = text.replace('."', '".')
    if "!" in text:
        text = text.replace('!"', '"!')
    if "?" in text:
        text = text.replace('?"', '"?')
    text = text.replace(".", ".<stop>")
    text = text.replace("?", "?<stop>")
    text = text.replace("!", "!<stop>")
    text = text.replace("<prd>", ".")
    sentences = text.split("<stop>")
    sentences = sentences[:-1]
    sentences = [s.strip() for s in sentences]
    return sentences


def color_code_sentence(sentence):
    words = len(sentence.split(" "))
    if words <= 2:
        color = "#F8F4C6"
    elif words <= 5:
        color = "#FAD1F0"
    elif words <= 10:
        color = "#C8F6C9"
    else:
        color = "#A5F6EF"
    return f'<span style="background-color: {color}">{sentence}</span>'


text = st.text_area("Your text", sample_text, label_visibility="collapsed")
paragraphs = text.split("\n")
colored_text = ""
for paragraph in paragraphs:
    sentences = split_into_sentences(paragraph)
    colored_text += " ".join(map(color_code_sentence, sentences)) + "\n"

st.write(colored_text, unsafe_allow_html=True)
