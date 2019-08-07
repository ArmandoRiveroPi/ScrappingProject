# from spellchecker import SpellChecker
from nltk import word_tokenize
import hunspell

dicFile = '/home/gauss/arm/importante/work/ai/projects/revolico/revolico_code/resources/es_ANY.dic'
affFile = '/home/gauss/arm/importante/work/ai/projects/revolico/revolico_code/resources/es_ANY.aff'
freqFile = '/home/gauss/arm/importante/work/ai/projects/revolico/revolico_code/resources/frequencies/es_no_hapaxes.txt'


class SpellCheck(object):
    def __init__(self):
        # SpellChecker(language='es')
        self.spell = hunspell.HunSpell(dicFile, affFile)
        # self.spell.word_frequency.load_text_file(freqFile)

    def correct_word(self, word):
        # Don't correct words with caps
        if word.lower() != word:
            return word
        if not self.spell.spell(word):
            corrections = self.spell.suggest(word)
            if len(corrections):
                word = corrections[0]
        return word

    def correct_phrase(self, phrase):
        words = word_tokenize(phrase)
        print('Words ====> ', words)
        corrected = ' '.join(self.correct_word(word) for word in words)
        # misspelled = self.spell.unknown(words)
        # for index in range(len(words)):
        #     word = words[index]
        #     if word in misspelled:
        #         print('Correction:', word, self.spell.correction(word))
        #         words[index] = self.spell.correction(word)
        # corrected = ' '.join(words)
        return corrected
