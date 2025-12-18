import sys
import os
from PyQt5 import QtWidgets, QtCore
from main_window import MainWindow


def main() -> None:
    """Основная функция. Вход в программу"""
    # Устанавливаем высокое DPI для современных мониторов
    if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

    # Создаем приложение
    app = QtWidgets.QApplication(sys.argv)

    # Устанавливаем стиль Fusion (современный кроссплатформенный)
    app.setStyle('Fusion')

    # Создаем и показываем главное окно
    window = MainWindow()
    window.show()

    # Запускаем главный цикл
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()