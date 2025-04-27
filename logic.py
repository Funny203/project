import pyshorteners
import speech_recognition as sr
from deepmultilingualpunctuation import PunctuationModel



def shorten_url(url):
    return pyshorteners.Shortener().clckru.short(url)


def voice_to_text(voice):
    r = sr.Recognizer()
    p = PunctuationModel()
    message = sr.AudioFile(voice)
    with message as source:
        audio = r.record(source)
    result = r.recognize_google(audio, language="ru_RU")
    punctuated_text = p.restore_punctuation(result)
    return punctuated_text

