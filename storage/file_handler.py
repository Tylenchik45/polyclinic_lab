"""
В этом файле прописана работа с файлами .json и .xml.
Использованы встроенные модули json и xml.etree.ElementTree
Тут уже появляется обработка исключений из exceptions
"""

import json
import xml.etree.ElementTree as Et
from exceptions.custom_errors import DataStorageError


def save_to_json(data, filepath):
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)  # ensure_ascii для корректного отображения кириллицы
    except (IOError, TypeError) as e:
        raise DataStorageError("Ошибка записи в JSON: " + str(e))


def load_from_json(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        raise DataStorageError("Файл JSON не найден: " + filepath)
    except json.JSONDecodeError as e:
        raise DataStorageError("Ошибка декодирования JSON: " + str(e))


def save_to_xml(root_element, filepath):
    try:
        tree = Et.ElementTree(root_element)
        tree.write(filepath, encoding='utf-8', xml_declaration=True)
    except (IOError, TypeError) as e:
        raise DataStorageError("Ошибка записи в XML: " + str(e))


def load_from_xml(filepath):
    try:
        tree = Et.parse(filepath)
        return tree.getroot()
    except FileNotFoundError:
        raise DataStorageError("Файл XML не найден: " + filepath)
    except Et.ParseError as e:
        raise DataStorageError("Ошибка парсинга XML: " + str(e))
