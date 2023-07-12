from typing import List, Dict


# The logic is following:
# - Words are generally ordered as they are in their language code.
# - Words from code with lower priority moved two positions further from previous code
# - Each word mention improves its position by 1
class TranslationsListBuilder:
    def __init__(self, language_codes_ordered: List[str]):
        self.language_code_priority = {language: index for index, language in enumerate(language_codes_ordered)}
        self.language_counter: Dict[str, int] = {language: 0 for language in language_codes_ordered}

        self.positions: Dict[str, int] = dict()
        self.mentions: Dict[str, int] = dict()

    def add(self, translation: str, language_code: str):
        assert language_code in self.language_code_priority
        raw_position = self.language_counter[language_code] + 2 * self.language_code_priority[language_code]
        self.language_counter[language_code] += 1

        if translation in self.positions:
            raw_position -= self.mentions[translation]
            self.mentions[translation] += 1
            if raw_position < self.positions[translation]:
                # If new position is better, use it
                self.positions[translation] = raw_position
            else:
                # Advance due to new mention
                self.positions[translation] -= 1
        else:
            self.mentions[translation] = 1
            self.positions[translation] = raw_position

    def result(self) -> List[str]:
        all_translations = [(position, word) for word, position in self.positions.items()]
        all_translations.sort()
        return [translation_pair[1] for translation_pair in all_translations]
