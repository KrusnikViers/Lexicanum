from lookup.wiktionary.types.definition import PartOfSpeech


class DefinitionComponent:
    def __init__(self, level: int):
        self.level = level

    def __str__(self):
        return '|' * self.level + '- '


class PartOfSpeechDC(DefinitionComponent):
    def __init__(self, pos: PartOfSpeech, level: int):
        super().__init__(level)
        self.part_of_speech = pos

    def __str__(self):
        return super().__str__() + 'pos: {}'.format(self.part_of_speech.name)


class ReadableFormDC(DefinitionComponent):
    def __init__(self, text: str, level: int):
        super().__init__(level)
        self.text = text

    def __str__(self):
        return super().__str__() + 'rdf: {}'.format(self.text)


class TranslationDC(DefinitionComponent):
    def __init__(self, lang: str, text: str, level: int):
        super().__init__(level)
        self.lang = lang
        self.text = text

    def __str__(self):
        return super().__str__() + 'tr-{}: {}'.format(self.lang, self.text)
