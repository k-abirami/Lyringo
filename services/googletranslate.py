import googletrans
from googletrans import Translator

translator = Translator()

text1 = "testing translate"

print((translator.translate('이 문장은 한글로 쓰여졌습니다.', dest='en')).text)
text2 = (translator.translate('hello my name is', dest='fr'))
print(text2.text)


