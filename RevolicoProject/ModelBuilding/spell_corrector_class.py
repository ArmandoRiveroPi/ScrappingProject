from spellchecker import SpellChecker
from nltk import word_tokenize


class SpellCheck(object):
    def __init__(self):
        self.spell = SpellChecker(language='es')
        self.spell.word_frequency.load_text_file(
            '/home/gauss/arm/importante/work/ai/projects/revolico/revolico_code/resources/frequencies/es_no_hapaxes.txt')

    def correct_phrase(self, phrase):
        words = word_tokenize(phrase)
        misspelled = self.spell.unknown(words)
        for index in range(len(words)):
            word = words[index]
            if word in misspelled:
                print('Correction:', word, self.spell.correction(word))
                words[index] = self.spell.correction(word)
        corrected = ' '.join(words)
        return corrected
