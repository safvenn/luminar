
from deep_translator import GoogleTranslator
def trans(word,lang):
    print(GoogleTranslator(source="en", target=lang).translate(word))


while True:
    l = input('select Language: ')
    w= input("enter word: ")
    trans(w,l)

    