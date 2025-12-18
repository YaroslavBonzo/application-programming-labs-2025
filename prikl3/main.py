import argparse  # Импорт модуля для обработки аргументов командной строки

import cv2  # Импорт OpenCV для работы с изображениями

import image  # Импорт нашего собственного модуля image.py


def get_args() -> list[str]:
    """Parse cmd arguments"""  # Документация функции: парсинг аргументов командной строки
    parser = argparse.ArgumentParser()  # Создание парсера аргументов
    parser.add_argument(
        '-s', '--source', help='Path to source image file'  # Добавление аргумента для пути к исходному изображению
    )
    parser.add_argument(
        '-o', '--output', help='Path to output image file'  # Добавление аргумента для пути к выходному изображению
    )
    parser.add_argument(
        '-v', '--is_vertical', help='Do vertical reverse need?'  # Добавление флага для вертикального отражения
    )
    args = parser.parse_args()  # Парсинг аргументов из командной строки
    if args.source is None or args.output is None:  # Проверка обязательных аргументов
        return None  # Возврат None, если обязательные аргументы не указаны
    return [args.source, args.output, bool(args.is_vertical)]  # Возврат списка с аргументами


def main() -> None:
    """Main function"""  # Документация главной функции
    try:
        source, output, vertical = get_args()  # Получение аргументов из командной строки
        img = cv2.imread(source)  # Загрузка изображения с помощью OpenCV
    except TypeError:  # Обработка исключения, если get_args() вернул None
        print("Usage: python main.py -s source.jpg -o out.jpg")  # Вывод инструкции по использованию
        return  # Завершение выполнения функции
    except Exception as e:  # Обработка любых других исключений
        print(f"Something went wrong {e}")  # Вывод сообщения об ошибке
        return  # Завершение выполнения функции

    print(f"Image size: {img.shape[1]}*{img.shape[0]}")  # Вывод размера изображения (ширина*высота)
    rev_img = image.reverse_img(img.copy(), vertical)  # Создание отраженной копии изображения (используется наш модуль image)
    image.show(img, rev_img)  # Отображение исходного и отраженного изображений

    try:
        cv2.imwrite(output, rev_img)  # Сохранение отраженного изображения в файл
    except Exception as e:  # Обработка исключений при сохранении
        print(f"Something went wrong {e}")  # Вывод сообщения об ошибке
        return  # Завершение выполнения функции


if __name__ == "__main__":  # Проверка, запущен ли скрипт напрямую
    main()  # Вызов главной функции