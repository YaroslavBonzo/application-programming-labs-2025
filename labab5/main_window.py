from PyQt5 import QtCore, QtGui, QtWidgets
from Iterator import ImageIterator
import os

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(900, 700)
        MainWindow.setMinimumSize(600, 500)

        # Устанавливаем темную тему
        MainWindow.setStyleSheet("""
            QMainWindow {
                background-color: #1e1e1e;
            }
            QLabel {
                color: #e0e0e0;
            }
        """)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Главный вертикальный layout
        self.main_layout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(15)

        # Панель информации
        self.info_panel = QtWidgets.QFrame()
        self.info_panel.setStyleSheet("""
            QFrame {
                background-color: #2d2d30;
                border-radius: 10px;
                border: 1px solid #3e3e42;
            }
        """)
        self.info_panel.setMaximumHeight(80)

        self.info_layout = QtWidgets.QHBoxLayout(self.info_panel)

        # Статус
        self.status_label = QtWidgets.QLabel("Выберите датасет для просмотра")
        self.status_label.setStyleSheet("""
            QLabel {
                color: #cccccc;
                font-size: 14px;
                font-weight: bold;
            }
        """)
        self.info_layout.addWidget(self.status_label)

        # Счетчик
        self.counter_label = QtWidgets.QLabel("")
        self.counter_label.setStyleSheet("""
            QLabel {
                color: #569cd6;
                font-size: 14px;
                font-weight: bold;
            }
        """)
        self.counter_label.setAlignment(QtCore.Qt.AlignRight)
        self.info_layout.addWidget(self.counter_label)

        self.main_layout.addWidget(self.info_panel)

        # Область для изображения
        self.image_frame = QtWidgets.QFrame()
        self.image_frame.setStyleSheet("""
            QFrame {
                background-color: #252526;
                border-radius: 10px;
                border: 2px solid #3e3e42;
            }
        """)

        self.image_layout = QtWidgets.QVBoxLayout(self.image_frame)
        self.image_layout.setContentsMargins(10, 10, 10, 10)

        # Метка для изображения
        self.picture = QtWidgets.QLabel()
        self.picture.setAlignment(QtCore.Qt.AlignCenter)
        self.picture.setMinimumSize(400, 300)
        self.picture.setStyleSheet("""
            QLabel {
                background-color: transparent;
            }
        """)
        self.image_layout.addWidget(self.picture)

        # Метка для названия файла
        self.filename_label = QtWidgets.QLabel()
        self.filename_label.setAlignment(QtCore.Qt.AlignCenter)
        self.filename_label.setStyleSheet("""
            QLabel {
                color: #d7ba7d;
                font-size: 12px;
                margin-top: 10px;
            }
        """)
        self.image_layout.addWidget(self.filename_label)

        # Метка для метки/класса
        self.class_label = QtWidgets.QLabel()
        self.class_label.setAlignment(QtCore.Qt.AlignCenter)
        self.class_label.setStyleSheet("""
            QLabel {
                color: #4ec9b0;
                font-size: 13px;
                font-weight: bold;
                margin-top: 5px;
            }
        """)
        self.image_layout.addWidget(self.class_label)

        self.main_layout.addWidget(self.image_frame, 1)  # 1 для растяжения

        # Панель управления
        self.control_panel = QtWidgets.QFrame()
        self.control_panel.setStyleSheet("""
            QFrame {
                background-color: #2d2d30;
                border-radius: 10px;
                border: 1px solid #3e3e42;
            }
        """)

        self.control_layout = QtWidgets.QVBoxLayout(self.control_panel)

        # Горизонтальная панель кнопок
        self.button_layout = QtWidgets.QHBoxLayout()

        # Кнопка выбора папки
        self.select_folder_button = self.create_button("📁 Выбрать папку", "#007acc")
        self.button_layout.addWidget(self.select_folder_button)

        # Кнопка выбора CSV
        self.select_csv_button = self.create_button("📄 Выбрать CSV", "#68217a")
        self.button_layout.addWidget(self.select_csv_button)

        self.control_layout.addLayout(self.button_layout)

        # Панель навигации
        self.nav_layout = QtWidgets.QHBoxLayout()

        # Кнопка Предыдущий
        self.prev_button = self.create_button("◀ Предыдущий", "#569cd6", 40)
        self.prev_button.setEnabled(False)
        self.nav_layout.addWidget(self.prev_button)

        # Кнопка Следующий
        self.next_button = self.create_button("Следующий ▶", "#569cd6", 40)
        self.next_button.setEnabled(False)
        self.nav_layout.addWidget(self.next_button)

        self.control_layout.addLayout(self.nav_layout)
        self.main_layout.addWidget(self.control_panel)

        MainWindow.setCentralWidget(self.centralwidget)

        # Подключение сигналов
        self.select_folder_button.clicked.connect(self.open_folder)
        self.select_csv_button.clicked.connect(self.open_csv)
        self.prev_button.clicked.connect(self.show_prev)
        self.next_button.clicked.connect(self.show_next)

        self.main_window = MainWindow
        self.current_image_path = None
        self.image_iterator = None

    def create_button(self, text, color, height=35):
        """Создает стилизованную кнопку"""
        button = QtWidgets.QPushButton(text)
        button.setMinimumHeight(height)
        button.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 14px;
                font-weight: bold;
                padding: 8px 15px;
            }}
            QPushButton:hover {{
                background-color: {self.lighten_color(color)};
            }}
            QPushButton:pressed {{
                background-color: {self.darken_color(color)};
            }}
            QPushButton:disabled {{
                background-color: #3e3e42;
                color: #7e7e7e;
            }}
        """)
        return button

    def lighten_color(self, hex_color):
        """Осветляет цвет на 20%"""
        r = int(hex_color[1:3], 16)
        g = int(hex_color[3:5], 16)
        b = int(hex_color[5:7], 16)
        r = min(255, int(r * 1.2))
        g = min(255, int(g * 1.2))
        b = min(255, int(b * 1.2))
        return f"#{r:02x}{g:02x}{b:02x}"

    def darken_color(self, hex_color):
        """Затемняет цвет на 20%"""
        r = int(hex_color[1:3], 16)
        g = int(hex_color[3:5], 16)
        b = int(hex_color[5:7], 16)
        r = int(r * 0.8)
        g = int(g * 0.8)
        b = int(b * 0.8)
        return f"#{r:02x}{g:02x}{b:02x}"

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle("Просмотрщик датасетов - Лабораторная работа 5")

    def open_folder(self):
        """Открытие папки с изображениями"""
        folder = QtWidgets.QFileDialog.getExistingDirectory(
            self.main_window,
            "Выберите папку с изображениями",
            "",
            QtWidgets.QFileDialog.ShowDirsOnly
        )

        if folder:
            try:
                self.image_iterator = ImageIterator(folder)
                self.update_status(f"Загружено {self.image_iterator.get_total()} изображений из папки", "#4ec9b0")
                self.update_controls(True)
                self.show_next()
            except Exception as e:
                self.show_error(f"Ошибка загрузки папки: {str(e)}")

    def open_csv(self):
        """Открытие CSV файла с аннотациями"""
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self.main_window,
            "Выберите CSV файл с аннотациями",
            "",
            "CSV Files (*.csv);;All Files (*)"
        )

        if file_path:
            try:
                self.image_iterator = ImageIterator(file_path)
                self.update_status(f"Загружено {self.image_iterator.get_total()} изображений из CSV", "#4ec9b0")
                self.update_controls(True)
                self.show_next()
            except Exception as e:
                self.show_error(f"Ошибка загрузки CSV: {str(e)}")

    def show_next(self):
        """Показать следующее изображение"""
        if not self.image_iterator:
            return

        try:
            image_path, label = next(self.image_iterator)
            self.display_image(image_path, label)
        except StopIteration:
            self.image_iterator.counter = 0
            if self.image_iterator.paths:
                self.show_next()

    def show_prev(self):
        """Показать предыдущее изображение"""
        if not self.image_iterator:
            return

        try:
            image_path, label = self.image_iterator.prev()
            self.display_image(image_path, label)
        except StopIteration:
            pass

    def display_image(self, image_path, label=""):
        """Отобразить изображение с информацией"""
        if not image_path:
            return

        # Загружаем изображение
        pixmap = QtGui.QPixmap(image_path)
        if pixmap.isNull():
            self.show_error(f"Не удалось загрузить изображение:\n{image_path}")
            return

        # Масштабируем с сохранением пропорций
        label_size = self.picture.size()
        scaled_pixmap = pixmap.scaled(
            label_size,
            QtCore.Qt.KeepAspectRatio,
            QtCore.Qt.SmoothTransformation
        )

        self.picture.setPixmap(scaled_pixmap)
        self.current_image_path = image_path

        # Обновляем информацию
        filename = os.path.basename(image_path)
        current_idx = self.image_iterator.counter if self.image_iterator.counter > 0 else self.image_iterator.get_total()
        total = self.image_iterator.get_total()

        self.filename_label.setText(f"📄 {filename}")
        self.counter_label.setText(f"{current_idx}/{total}")

        if label:
            self.class_label.setText(f"🏷️  Класс: {label}")
        else:
            self.class_label.setText("")

        # Центрируем изображение
        self.picture.setAlignment(QtCore.Qt.AlignCenter)

    def update_status(self, message, color="#cccccc"):
        """Обновить статус"""
        self.status_label.setText(message)
        self.status_label.setStyleSheet(f"color: {color}; font-size: 14px; font-weight: bold;")

    def update_controls(self, enabled):
        """Обновить состояние кнопок навигации"""
        self.prev_button.setEnabled(enabled)
        self.next_button.setEnabled(enabled)

    def show_error(self, message):
        """Показать сообщение об ошибке"""
        QtWidgets.QMessageBox.critical(
            self.main_window,
            "Ошибка",
            message
        )
        self.update_status("Произошла ошибка", "#f44747")

    def resizeEvent(self, event):
        """Обработчик изменения размера окна"""
        if self.current_image_path and self.image_iterator:
            # Получаем текущее изображение и метку
            current_path, current_label = self.image_iterator.get_current_info()
            if current_path:
                pixmap = QtGui.QPixmap(current_path)
                if not pixmap.isNull():
                    label_size = self.picture.size()
                    scaled_pixmap = pixmap.scaled(
                        label_size,
                        QtCore.Qt.KeepAspectRatio,
                        QtCore.Qt.SmoothTransformation
                    )
                    self.picture.setPixmap(scaled_pixmap)
        super(type(self.main_window), self.main_window).resizeEvent(event)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.retranslateUi(self)

        # Устанавливаем иконку окна
        self.setWindowIcon(QtGui.QIcon())

        # Показываем дефолтное изображение если есть fon.jpg
        default_image = "fon.jpg"
        if os.path.exists(default_image):
            pixmap = QtGui.QPixmap(default_image)
            if not pixmap.isNull():
                self.ui.picture.setPixmap(pixmap.scaled(
                    self.ui.picture.size(),
                    QtCore.Qt.KeepAspectRatio,
                    QtCore.Qt.SmoothTransformation
                ))

    def resizeEvent(self, event):
        """Передаем событие изменения размера в UI"""
        self.ui.resizeEvent(event)
        super().resizeEvent(event)