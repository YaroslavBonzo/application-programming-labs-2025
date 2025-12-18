import os
import pandas as pd


class ImageIterator:
    """Универсальный итератор для изображений и CSV аннотаций"""

    def __init__(self, source: str):
        """Конструктор принимает путь к папке или CSV файлу"""
        self.paths = []
        self.counter = 0
        self.labels = []  # Для хранения меток из CSV
        self.source_type = None

        if not source:
            raise RuntimeError("Пустой путь к источнику")

        # Определяем тип источника
        if source.endswith('.csv'):
            self.source_type = 'csv'
            self.load_from_csv(source)
        elif os.path.isdir(source):
            self.source_type = 'folder'
            self.load_from_folder(source)
        else:
            raise RuntimeError(f"Неподдерживаемый источник: {source}")

        if not self.paths:
            raise RuntimeError("Не найдено ни одного изображения")

    def load_from_csv(self, csv_path: str):
        """Загрузка путей из CSV файла"""
        try:
            df = pd.read_csv(csv_path)

            # Ищем столбцы с путями к изображениям
            possible_columns = ['path', 'file', 'image', 'filename', 'abs_path']
            path_column = None

            for col in possible_columns:
                if col in df.columns:
                    path_column = col
                    break

            if path_column is None:
                # Если не нашли стандартные названия, берем первый столбец
                path_column = df.columns[0]

            # Берем столбец с метками если есть
            if 'label' in df.columns:
                self.labels = df['label'].tolist()
            elif 'class' in df.columns:
                self.labels = df['class'].tolist()
            else:
                self.labels = [""] * len(df)

            self.paths = df[path_column].tolist()
            print(f"Загружено {len(self.paths)} изображений из CSV")

        except Exception as e:
            raise RuntimeError(f"Ошибка чтения CSV: {e}")

    def load_from_folder(self, folder_path: str):
        """Загрузка путей из папки"""
        supported_formats = ('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.webp')

        for file_name in os.listdir(folder_path):
            if file_name.lower().endswith(supported_formats):
                full_path = os.path.join(folder_path, file_name)
                self.paths.append(full_path)
                self.labels.append("")  # Пустая метка для папок

        self.paths.sort()  # Сортируем для порядка
        print(f"Загружено {len(self.paths)} изображений из папки")

    def __iter__(self):
        self.counter = 0
        return self

    def __next__(self):
        """Получить следующее изображение"""
        if not self.paths:
            raise StopIteration("Нет изображений")

        if self.counter >= len(self.paths):
            self.counter = 0  # Циклический переход

        path = self.paths[self.counter]
        label = self.labels[self.counter] if self.counter < len(self.labels) else ""
        self.counter += 1

        return path, label

    def prev(self):
        """Получить предыдущее изображение"""
        if not self.paths:
            raise StopIteration("Нет изображений")

        if self.counter <= 0:
            self.counter = len(self.paths)  # Переходим к последнему

        self.counter -= 1
        path = self.paths[self.counter]
        label = self.labels[self.counter] if self.counter < len(self.labels) else ""

        return path, label

    def get_current_info(self):
        """Получить информацию о текущем изображении"""
        if not self.paths or self.counter == 0:
            return None, ""

        idx = self.counter - 1 if self.counter > 0 else len(self.paths) - 1
        if 0 <= idx < len(self.paths):
            return self.paths[idx], self.labels[idx] if idx < len(self.labels) else ""
        return None, ""

    def get_total(self):
        """Получить общее количество изображений"""
        return len(self.paths)