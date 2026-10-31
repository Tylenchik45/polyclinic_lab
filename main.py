"""
Основной файл программы. Этот файл нужно запустить для проведения тестов и проверки работоспособности
"""

from structure.classes import Patient, Doctor, Diagnosis, Prescription, Department
from structure.class_manager import PolyclinicSystem
from exceptions.custom_errors import PolyclinicBaseError, DataStorageError


def main():
    system = PolyclinicSystem()

    print("### 1. Добавление данных из шаблонов (CRUD: Create) ###")
    # Проверяем возможность создания объектов вручную

    # Пациент из шаблона
    patient1 = Patient(
        person_id="P001", full_name="Иванов Иван Иванович", birth_date="2006-08-16",
        phone="+78005553535", policy_number="1234567890123456",
        address="г. Москва, ул. Нагорная, д. 1"
    )
    patient1.add_diagnosis(Diagnosis(
        icd_code="T02.2",
        description="Переломы, захватывающие несколько областей одной верхней конечности",
        date="2026-02-01"
    ))
    patient1.medical_card.prescriptions.append(Prescription(
        medication="Парацетамол", dosage="500мг", duration_days=5
    ))
    system.add_patient(patient1)
    print("Пациент добавлен: " + patient1.get_info())

    # Врач из шаблона
    doctor1 = Doctor(
        person_id="D001", full_name="Двачевская Алиса Семеновна", birth_date="1975-10-29",
        phone="+79774375311", employee_id="EMP001", position="Врач", salary=85000.0,
        specialization="Терапевт", office_number="101"
    )
    system.add_doctor(doctor1)
    print("Врач добавлен: " + doctor1.get_info())

    # Отделение
    dept1 = Department(dept_id="DEP001", name="Терапевтическое отделение", head_doctor=doctor1)
    dept1.add_doctor(doctor1)
    system.add_department(dept1)
    print("Отделение добавлено: " + dept1.name)

    print("\n### 2. Чтение данных (CRUD: Read) ###")
    try:
        found_patient = system.get_patient("P001")
        print("Найден пациент: " + found_patient.full_name + ", дата рождения: " + found_patient.birth_date)

        found_doctor = system.get_doctor("D001")
        print("Найден врач: " + found_doctor.full_name + ", дата рождения: " + found_doctor.birth_date)
    except TypeError as e:
        print("[Ошибка типа данных] Неверный формат ID: " + str(e))
    except PolyclinicBaseError as e:
        print("[Ошибка системы] " + str(e))

    print("\n### 3. Обработка пользовательского исключения (Пациент не найден) ###")
    try:
        system.get_patient("P999")
    except PolyclinicBaseError as e:
        print("Успешно поймано исключение: " + str(e))
        print("Программа продолжает работу без вылета.")

    print("\n### 4. Обновление данных (CRUD: Update) ###")
    try:
        system.update_patient_phone("P001", "+73141592653")
        print("Новый телефон пациента: " + system.get_patient("P001").phone)
    except PolyclinicBaseError as e:
        print("[Ошибка] " + str(e))

    print("\n#### 5. Сохранение и загрузка (JSON) ###")
    try:
        system.export_to_json("data_export.json")
        print("Данные успешно сохранены в data_export.json")

        # Чистим имеющиеся данные, для проверки правильности импорта
        system.patients.clear()
        system.doctors.clear()
        system.import_from_json("data_export.json")
        print("Данные загружены из JSON. Пациентов: " + str(len(system.patients)) + ", Врачей: " +
              str(len(system.doctors)))
        print("Пациент после загрузки: " + system.get_patient("P001").full_name)
        print("Врач после загрузки: " + system.get_doctor("D001").full_name + ", Кабинет: " +
              system.get_doctor("D001").office_number)
    except DataStorageError as e:
        print("[Ошибка хранилища] " + str(e))

    print("\n### 6. Сохранение и загрузка (XML) ###")
    try:
        system.export_to_xml("data_export.xml")
        print("Данные успешно сохранены в data_export.xml")

        # Чистим имеющиеся данные, для проверки правильности импорта
        system.patients.clear()
        system.doctors.clear()
        system.import_from_xml("data_export.xml")
        print("Данные загружены из XML. Пациентов: " + str(len(system.patients)) + ", Врачей: "
              + str(len(system.doctors)))
        print("Пациент после загрузки: " + system.get_patient("P001").full_name)
        print("Врач после загрузки: " + system.get_doctor("D001").full_name + ", Кабинет: " +
              system.get_doctor("D001").office_number)
    except DataStorageError as e:
        print("[Ошибка хранилища] " + str(e))

    print("\n### 7. Демонстрация защиты от некорректного файла ###")
    try:
        system.import_from_json("non_existent_file.json")
    except DataStorageError as e:
        print("Успешно поймали: " + str(e))

    print("\n### 8. Чтение из исходных шаблонов ###")
    try:
        # Чистим имеющиеся данные, для проверки правильности импорта
        system.patients.clear()
        system.doctors.clear()
        system.import_from_json("docs/data_structure_template.json")
        print("Загружено из шаблона JSON. Пациентов: " + str(len(system.patients)) + ", Врачей: " +
              str(len(system.doctors)))
    except DataStorageError as e:
        print("[Ошибка] " + str(e))

    try:
        # Чистим имеющиеся данные, для проверки правильности импорта
        system.patients.clear()
        system.doctors.clear()
        system.import_from_xml("docs/data_structure_template.xml")
        print("Загружено из шаблона XML. Пациентов: " + str(len(system.patients)) + ", Врачей: " +
              str(len(system.doctors)))
    except DataStorageError as e:
        print("[Ошибка] " + str(e))


if __name__ == "__main__":
    main()
