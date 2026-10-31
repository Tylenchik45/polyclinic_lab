"""
В этом файле прописаны все классы исключений для области поликлиники.
Я не уверен, как нужно было отразить исключения в диаграмме, поэтому они там вынесены отдельно.
Сама структура классов исключений описана в UML диаграмме.
"""


class PolyclinicBaseError(Exception):
    """Базовый класс исключений для поликлиники."""
    pass


class PersonBaseError(PolyclinicBaseError):
    """Базовый класс исключений для человека"""
    pass


class PatientNotFoundError(PersonBaseError):
    """Исключение, возникающее при попытке найти несуществующего пациента."""
    pass


class DoctorNotFoundError(PersonBaseError):
    """Исключение, возникающее при попытке найти несуществующего врача."""
    pass


class DataStorageError(PolyclinicBaseError):
    """Исключение, возникающее при ошибках чтения/записи файлов."""
    pass
