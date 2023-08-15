from dataclasses import dataclass
from typing import List, Any

from core.util import if_none
from lookup.wiktionary.languages.base.translations_list_builder import TranslationsListBuilder
from lookup.wiktionary.types import Definition, DefinitionComponent, DCType


@dataclass
class _LeveledCache:
    level: int
    value: Any


class DefinitionsComposer:
    def __init__(self, article_title: str, translation_codes_ordered: List[str]):
        self.article_title: str = article_title
        self.translation_codes_ordered = translation_codes_ordered
        self.readable_form_cache = _LeveledCache(-1, None)
        self.part_of_speech_cache = _LeveledCache(-1, None)
        self.grammar_form_cache = _LeveledCache(-1, None)
        self.translations_level: int = -1
        self.translations = TranslationsListBuilder(self.translation_codes_ordered)

    def _reset_cache(self):
        self.readable_form_cache = _LeveledCache(-1, None)
        self.part_of_speech_cache = _LeveledCache(-1, None)
        self.grammar_form_cache = _LeveledCache(-1, None)
        self.translations_level: int = -1
        self.translations = TranslationsListBuilder(self.translation_codes_ordered)

    def _compose_from_cache(self) -> List[Definition]:
        if not self.readable_form_cache or not self.part_of_speech_cache or not self.translations.result():
            self._reset_cache()
            return []
        result = []
        if self.readable_form_cache.value and self.part_of_speech_cache.value:
            result.append(Definition(self.part_of_speech_cache.value,
                                     self.article_title,
                                     self.readable_form_cache.value,
                                     if_none(self.grammar_form_cache.value, ''),
                                     translation_articles=self.translations.result()))
        self._reset_cache()
        return result

    @staticmethod
    def _update_cache(cache: _LeveledCache, component: DefinitionComponent):
        if cache.level == -1 or component.level < cache.level:
            cache.value = component.value
            cache.level = component.level

    def build(self, definition_components: List[DefinitionComponent]) -> List[Definition]:
        result: List[Definition] = []
        for component in definition_components:
            match component.dc_type:
                case DCType.Separator:
                    result += self._compose_from_cache()
                case DCType.ReadableForm:
                    self._update_cache(self.readable_form_cache, component)
                case DCType.PartOfSpeech:
                    self._update_cache(self.part_of_speech_cache, component)
                case DCType.GrammarNote:
                    self._update_cache(self.grammar_form_cache, component)
                case DCType.Translation:
                    self.translations.add(translation=component.value.text, language_code=component.value.lang)
        result += self._compose_from_cache()
        return result
