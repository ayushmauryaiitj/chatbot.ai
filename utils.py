from googletrans import Translator

translator = Translator()

def translate_text(text, lang):
    if lang == "English":
        return text
    return translator.translate(text, dest="hi").text
