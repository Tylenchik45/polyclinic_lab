"""
В этом файле прописаны все классы для области поликлиники.
Не все из них полноценно используются, но, надеюсь, этого достаточно для задания.
Наиболее важно было создать связь между классами, что сделано с помощью того,
что почти у всех объектов есть свой уникальный идентификатор.
Сама структура классов описана в UML диаграмме.
"""


# Абстрактный класс, общий для пациентов и сотрудников
class Person:
    def __init__(self, person_id, full_name, birth_date, phone):
        self.id = person_id
        self.full_name = full_name
        self.birth_date = birth_date
        self.phone = phone

    def get_info(self):
        # Получаем общую информацию о человеке
        return self.full_name + " (ID: " + self.id + ", Тел: " + self.phone + ")"


# Класс диагноза (icd_code - то же самое, что код МКБ)
class Diagnosis:
    def __init__(self, icd_code, description, date):
        self.icd_code = icd_code
        self.description = description
        self.date = date


# Класс для рецепта от врача
class Prescription:
    def __init__(self, medication, dosage, duration_days):
        self.medication = medication
        self.dosage = dosage
        self.duration_days = duration_days


# Класс для медицинской карты
class MedicalCard:
    def __init__(self, card_id, patient_id):
        self.card_id = card_id
        self.patient_id = patient_id
        self.diagnoses = []
        self.prescriptions = []


# Класс для работы с пациентом
class Patient(Person):
    def __init__(self, person_id, full_name, birth_date, phone, policy_number, address):
        # super - для корректного наследования от родителя (Person) (вызываем конструкторы родителя)
        super(Patient, self).__init__(person_id, full_name, birth_date, phone)
        self.policy_number = policy_number
        self.address = address
        self.medical_card = MedicalCard(card_id="MR" + person_id, patient_id=person_id)

    def add_diagnosis(self, diagnosis):
        # Можем добавить диагноз в медицинскую карту
        self.medical_card.diagnoses.append(diagnosis)


# Абстрактный класс для сотрудников (врач, администратор)
# Удобно на будущее для добавления позиций уборщиков, охранников и т. д.
class Employee(Person):
    def __init__(self, person_id, full_name, birth_date, phone, employee_id, position, salary):
        super(Employee, self).__init__(person_id, full_name, birth_date, phone)
        self.employee_id = employee_id
        self.position = position
        self.salary = salary


# Класс расписания врача
class Schedule:
    def __init__(self, doctor_id):
        self.doctor_id = doctor_id
        self.available_slots = []

    def add_slot(self, slot):
        # Добавляем доступное время
        if slot not in self.available_slots:
            self.available_slots.append(slot)


# Класс для врача
class Doctor(Employee):
    def __init__(self, person_id, full_name, birth_date, phone, employee_id, position, salary, specialization,
                 office_number):
        super(Doctor, self).__init__(person_id, full_name, birth_date, phone, employee_id, position, salary)
        self.specialization = specialization
        self.office_number = office_number
        self.schedule = Schedule(doctor_id=person_id)


# Клас для администратора
class Administrator(Employee):
    def __init__(self, person_id, full_name, birth_date, phone, employee_id, position, salary, access_level):
        super(Administrator, self).__init__(person_id, full_name, birth_date, phone, employee_id, position, salary)
        self.access_level = access_level


# Класс для отделения
class Department:
    def __init__(self, dept_id, name, head_doctor):
        self.dept_id = dept_id
        self.name = name
        self.head_doctor = head_doctor
        self.doctors = []

    def add_doctor(self, doctor):
        # Можем приписать врача к отделению
        self.doctors.append(doctor)


# Класс записи к врачу
class Appointment:
    def __init__(self, appointment_id, date, time, status, patient, doctor):
        self.appointment_id = appointment_id
        self.date = date
        self.time = time
        self.status = status
        self.patient = patient
        self.doctor = doctor
