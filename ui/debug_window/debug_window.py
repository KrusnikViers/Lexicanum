import time
from typing import Type, Tuple, List

from PySide6.QtCore import Slot, QMargins
from PySide6.QtWidgets import QDialog, QMainWindow

from core.types import Card
from core.util import StatusOr
from lookup.wiktionary.interface import WiktionaryInterface
from lookup.wiktionary.internal_logic import match_definition_sets
from lookup.wiktionary.internal_logic.web_api import search_articles, retrieve_articles, WebArticle
from lookup.wiktionary.languages.base import LocalizedParser
from lookup.wiktionary.types import DefinitionSet, MarkupTree, build_definition_set
from ui.debug_window.text_tab import TextTab
from ui.gen.debug_window.debug_window_uic import Ui_DebugWindow


class DebugWindow(QDialog):
    def __init__(self, parent: QMainWindow, lookup_interface: WiktionaryInterface):
        super().__init__(parent)
        self.lookup_interface = lookup_interface

        self.ui = Ui_DebugWindow()
        self.ui.setupUi(self)
        self.setModal(True)
        self.show()
        self.setGeometry(parent.geometry().marginsRemoved(QMargins(5, 5, 5, 5)))

        self.timings_tab = TextTab(self)
        self.ui.tab_widget.addTab(self.timings_tab, 'Timings')

        self._overall_timer = time.perf_counter()
        self._last_event_timer = self._overall_timer

        self.ui.finish_button.clicked.connect(self.on_finish_clicked)
        self.ui.lookup_button.clicked.connect(self.on_lookup_clicked)

    @Slot()
    def on_finish_clicked(self):
        self.done(QDialog.DialogCode.Accepted)

    def _reset(self):
        while self.ui.tab_widget.count() > 1:
            self.ui.tab_widget.removeTab(self.ui.tab_widget.count() - 1)
        self.timings_tab.ui.text_browser.clear()
        self._overall_timer = time.perf_counter()
        self._last_event_timer = self._overall_timer

    def _log_event(self, text: str):
        new_timer_value = time.perf_counter()
        message = '{:.3f}:+{:.3f} - {}'.format(
            new_timer_value - self._overall_timer,
            new_timer_value - self._last_event_timer,
            text
        )
        self._last_event_timer = new_timer_value
        self.timings_tab.ui.text_browser.append(message)

    @Slot()
    def on_lookup_clicked(self):
        self._reset()

        lookup_text = self.ui.lookup_text_edit.text().strip()
        self._log_event('Lookup for <b>{}</b>'.format(lookup_text))

        is_lookup_from_answer = self.ui.lookup_type_cbox.currentIndex() == 0
        if is_lookup_from_answer:
            self._on_answer_lookup(lookup_text)
        else:
            self._on_question_lookup(lookup_text)

    def _log_cards(self, cards: List[Card]):
        for card in cards:
            self._log_event('<b>{}</b> - <i>{}</i> - <b>{}</b> <br/>grammar: {} <br/>meaning: {}<br/>IPA: {}'.format(
                card.answer, card.card_type.name, card.question,
                card.grammar_note,
                card.meaning_note,
                card.ipa_note
            ))

    def _on_answer_lookup(self, lookup_text: str):
        lookup_status = self._lookup_definition_sets(
            lookup_text,
            source_parser=self.lookup_interface.answer_parser,
            translations_parser=self.lookup_interface.question_parser)
        if lookup_status.is_error():
            self._log_event(lookup_status.status)
            return

        answers_set, questions_set = lookup_status.value
        cards_list = match_definition_sets(answers_set, questions_set, order_by_question=False)
        self._log_event('<b>{}</b> cards were constructed'.format(len(cards_list)))
        self._log_cards(cards_list)

    def _on_question_lookup(self, lookup_text: str):
        lookup_status = self._lookup_definition_sets(
            lookup_text,
            source_parser=self.lookup_interface.question_parser,
            translations_parser=self.lookup_interface.answer_parser)
        if lookup_status.is_error():
            self._log_event(lookup_status.status)
            return

        questions_set, answers_set = lookup_status.value
        cards_list = match_definition_sets(answers_set, questions_set, order_by_question=True)
        self._log_event('<b>{}</b> cards were constructed'.format(len(cards_list)))
        self._log_cards(cards_list)

    def _lookup_definition_sets(
            self, search_text: str,
            source_parser: Type[LocalizedParser],
            translations_parser: Type[LocalizedParser]) -> StatusOr[Tuple[DefinitionSet, DefinitionSet]]:

        self._log_event('Searching for <b>{}</b> in <b>{}</b> wiktionary'.format(
            search_text, source_parser.api_language_code()))
        source_articles_status = search_articles(search_text, source_parser.api_language_code())
        if source_articles_status.is_error():
            return source_articles_status.to_other()

        self._log_event('<b>{}</b> articles fetched: <br/><b>{}</b>'.format(
            len(source_articles_status.value),
            '<br/>'.join([article.title for article in source_articles_status.value])
        ))

        source_definition_set = self._articles_to_definition_set(
            source_articles_status.value, source_parser, translations_parser)
        unique_translation_titles = list(set([title
                                              for definitions_list in source_definition_set.values()
                                              for definition in definitions_list
                                              for title in definition.translation_articles]))
        self._log_event('Getting <b>{}</b> articles for translations:<br/><b>{}</b>'.format(
            len(unique_translation_titles), '<br/>'.join(unique_translation_titles)))
        if not unique_translation_titles:
            return StatusOr(status="Not enough data extracted from search request")

        # Fetch translation articles
        translation_articles_status = retrieve_articles(unique_translation_titles,
                                                        translations_parser.api_language_code())
        if translation_articles_status.is_error():
            return translation_articles_status.to_other()

        self._log_event('<b>{}</b> articles fetched: <br/><b>{}</b>'.format(
            len(translation_articles_status.value),
            '<br/>'.join([article.title for article in translation_articles_status.value])
        ))

        # Create translations definition set
        translation_definition_set = self._articles_to_definition_set(translation_articles_status.value,
                                                                      translations_parser, source_parser)
        return StatusOr((source_definition_set, translation_definition_set))

    def _articles_to_definition_set(self, articles: List[WebArticle],
                                    article_parser: Type[LocalizedParser],
                                    translations_parser: Type[LocalizedParser]) -> DefinitionSet:
        extracted_definitions = []
        for article in articles:
            markup_tree = MarkupTree.build(article.title, article.content)
            extracted_definitions += article_parser.extract_definitions(
                markup_tree, article.title, translations_parser.language_codes_for_translations())
        self._log_event('<b>{}</b> definitions found:<br/>{}'.format(
            len(extracted_definitions),
            '<br/>'.join(['<b>{}</b> - <i>{}</i>'.format(definition.readable_name, definition.part_of_speech.name)
                          for definition in extracted_definitions])
        ))
        return build_definition_set(extracted_definitions)
