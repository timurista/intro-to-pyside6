# token_calculator.py

from PySide6.QtCore import QObject, Signal


class TokenCalculator(QObject):
    progress_signal = Signal(int)

    def calculate_and_emit(self, tokens):
        self.progress_signal.emit(tokens / 7500 * 100)
