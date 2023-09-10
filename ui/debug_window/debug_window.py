import time
from typing import List, Dict

from PySide6.QtCore import Slot, QMargins
from PySide6.QtWidgets import QDialog, QMainWindow, QTextBrowser, QToolBox, QTreeWidget, QTreeWidgetItem

from lookup.wiktionary.interface import LookupInterface
from lookup.wiktionary.types import DebugInterface
from lookup.wiktionary.types import MarkupTree, DefinitionComponent, DCType
from ui.gen.debug_window.debug_window_uic import Ui_DebugWindow


class DebugWindow(QDialog, DebugInterface):
    def __init__(self, parent: QMainWindow, lookup_interface: LookupInterface):
        super().__init__(parent)
        self._lookup_interface = lookup_interface

        self._ui = Ui_DebugWindow()
        self._ui.setupUi(self)
        self.setModal(True)
        self.show()
        self.setGeometry(parent.geometry().marginsRemoved(QMargins(5, 5, 5, 5)))

        self._general_log_browser = QTextBrowser(self)
        self._ui.tab_widget.addTab(self._general_log_browser, 'General Log')

        self._overall_timer = time.perf_counter()
        self._last_event_timer = self._overall_timer

        self._widgets_map: Dict[str, QToolBox] = dict()

        self._ui.finish_button.clicked.connect(self.on_finish_clicked)
        self._ui.lookup_button.clicked.connect(self.on_lookup_clicked)

    @Slot()
    def on_finish_clicked(self):
        self.done(QDialog.DialogCode.Accepted)

    @Slot()
    def on_lookup_clicked(self):
        self._reset()

        lookup_text = self._ui.lookup_text_edit.text().strip()
        self.progress_message('Lookup for <b>{}</b>'.format(lookup_text))

        is_lookup_from_answer = self._ui.lookup_type_cbox.currentIndex() == 0
        if is_lookup_from_answer:
            result = self._lookup_interface.lookup_by_answer(lookup_text, self)
        else:
            result = self._lookup_interface.lookup_by_question(lookup_text, self)

        if result.is_error():
            self.progress_message(result.status)
        else:
            result_string = ''
            for card in result.value:
                result_string += ('<br/><b>{} => {}</b>, {}<br/>' +
                                  '<i>{}<br/>{}<br/></i>').format(
                    card.question, card.answer, card.card_type.name,
                    card.grammar_note, card.meaning_note
                )
            self.progress_rich_message('Resulting cards', result_string)

    def _reset(self):
        self._widgets_map.clear()
        while self._ui.tab_widget.count() > 1:
            self._ui.tab_widget.removeTab(self._ui.tab_widget.count() - 1)
        self._general_log_browser.clear()
        self._overall_timer = time.perf_counter()
        self._last_event_timer = self._overall_timer

    def progress_message(self, message: str):
        new_timer_value = time.perf_counter()
        message = '<br/><i>{:.3f}:+{:.3f}</i><br/>{}'.format(
            new_timer_value - self._overall_timer,
            new_timer_value - self._last_event_timer,
            message
        )
        self._last_event_timer = new_timer_value
        self._general_log_browser.append(message)

    def progress_rich_message(self, title: str, message: str):
        message = message.replace('\n', '<br/>')
        self.progress_message('<b>{}</b><br/>{}'.format(title, message))

    def _toolbox(self, wiki_title: str, language: str) -> QToolBox:
        key = '{} / {}'.format(wiki_title, language)
        if key in self._widgets_map:
            return self._widgets_map[key]

        new_widget = QToolBox(self._ui.tab_widget)
        self._ui.tab_widget.addTab(new_widget, key)
        self._widgets_map[key] = new_widget
        return new_widget

    def show_raw_wiki_content(self, wiki_title: str, language: str, content: str):
        toolbox = self._toolbox(wiki_title, language)
        text_browser = QTextBrowser(toolbox)
        toolbox.addItem(text_browser, 'Raw wiki content')
        text_browser.setText(content)

    def show_markup_tree(self, wiki_title: str, language: str, tree: MarkupTree):
        toolbox = self._toolbox(wiki_title, language)
        new_widget = QTreeWidget(toolbox)
        new_widget.setHeaderLabels(['Name', 'Level', 'Follow-up text', 'PArgs', 'KArgs'])
        toolbox.addItem(new_widget, 'Markup tree')
        for child_node in tree.children:
            new_item = QTreeWidgetItem(new_widget)
            self._extend_markup_tree(new_item, child_node)
            new_widget.addTopLevelItem(new_item)

    @classmethod
    def _extend_markup_tree(cls, item: QTreeWidgetItem, node: MarkupTree):
        item.setText(0, node.name)
        item.setText(1, str(node.level))
        item.setText(2, node.following_text)
        item.setText(3, '; '.join(node.plain_args))
        item.setText(4, '; '.join(['{}:{}'.format(key, value) for key, value in node.keyed_args.items()]))
        for child_node in node.children:
            new_item = QTreeWidgetItem(item)
            cls._extend_markup_tree(new_item, child_node)
            item.addChild(new_item)

    def show_components_list(self, wiki_title: str, language: str, components: List[DefinitionComponent]):
        toolbox = self._toolbox(wiki_title, language)
        text_browser = QTextBrowser(toolbox)
        toolbox.addItem(text_browser, 'Definition components tree')
        for component in components:
            prefix = '..' * component.level
            match component.dc_type:
                case DCType.Separator:
                    text_browser.append(prefix + '_____________________')
                case DCType.GrammarNote:
                    text_browser.append(prefix + 'grammar : {}'.format(component.value))
                case DCType.ReadableForm:
                    text_browser.append(prefix + 'readable : {}'.format(component.value))
                case DCType.PartOfSpeech:
                    text_browser.append(prefix + component.value.name)
                case DCType.Translation:
                    text_browser.append(prefix + ' tr-{} : {}'.format(component.value.lang, component.value.text))
