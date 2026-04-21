from typing import Any

from PySide6.QtCore import QPoint, QRect, QSize, Qt
from PySide6.QtWidgets import QLayout, QSizePolicy


class FixedFlowLayout(QLayout):
    """Displays a grid of widgets. Each widget is forced to maintain `item_size` geometry."""

    def __init__(self, parent=None, margin=0, spacing=-1):
        super().__init__(parent)
        self._item_size: QSize | None = None
        self._items: list[Any] = []

        if margin != -1:
            self.setContentsMargins(margin, margin, margin, margin)
        self.setSpacing(spacing)

    def __del__(self):
        while self.count():
            self.takeAt(0)

    def set_item_size(self, item_size: QSize) -> None:
        if self._item_size is not None:
            raise AssertionError("Item size could not be set multiple times for the same layout.")
        self._item_size = item_size

    def _do_layout(self, rect: QRect, *, apply_geometry: bool) -> int:
        m = self.contentsMargins()
        effective_rect = rect.adjusted(m.left(), m.top(), -m.right(), -m.bottom())

        x = effective_rect.x()
        y = effective_rect.y()

        item_w = self._item_size.width()
        item_h = self._item_size.height()
        space = self.spacing()

        for item in self._items:
            # Check if we need to wrap to the next row
            if x + item_w > effective_rect.right() and x > effective_rect.x():
                x = effective_rect.x()
                y += item_h + space

            if apply_geometry:
                item.setGeometry(QRect(QPoint(x, y), self._item_size))

            x += item_w + space

        # Return the resulting total height needed.
        return y + item_h + m.bottom() - rect.y()

    # QLayout overrides.
    ####################
    def addItem(self, item: Any) -> None:
        self._items.append(item)

    def addWidget(self, widget):
        if self._item_size is None:
            raise AssertionError("Item size should be set before adding any children.")
        widget.setFixedSize(self._item_size)
        # Ensure the widget's size policy doesn't conflict
        widget.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        super().addWidget(widget)

    def count(self) -> int:
        return len(self._items)

    def itemAt(self, index: int) -> Any | None:
        return self._items[index] if 0 <= index < len(self._items) else None

    def takeAt(self, index: int) -> Any | None:
        return self._items.pop(index) if 0 <= index < len(self._items) else None

    def expandingDirections(self) -> Qt.Orientation:
        return Qt.Orientation(0)

    def hasHeightForWidth(self) -> bool:
        return True

    def heightForWidth(self, width: int) -> int:
        return self._do_layout(QRect(0, 0, width, 0), apply_geometry=False)

    def setGeometry(self, rect: QRect) -> None:
        super().setGeometry(rect)
        self._do_layout(rect, apply_geometry=True)

    def sizeHint(self) -> QSize:
        return self.minimumSize()

    def minimumSize(self) -> QSize:
        m = self.contentsMargins()
        # Minimum is at least one item plus margins
        return self._item_size + QSize(m.left() + m.right(), m.top() + m.bottom())
