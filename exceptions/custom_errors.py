class PolyclinicBaseError(Exception):
    """Базовый класс исключений для поликлиники."""
    pass


class PatientNotFoundError(PolyclinicBaseError):
    """Исключение, возникающее при попытке найти несуществующего пациента."""
    pass


class DoctorNotFoundError(PolyclinicBaseError):
    """Исключение, возникающее при попытке найти несуществующего врача."""
    pass


class DataStorageError(PolyclinicBaseError):
    """Исключение, возникающее при ошибках чтения/записи файлов."""
    pass
