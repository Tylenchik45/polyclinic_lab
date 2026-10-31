"""
В этом файле прописана работа со всеми классами.
Использованы встроенные модули json и xml.etree.ElementTree
Также имеется обработка исключений из exceptions, однако я забыл прописать исключение для уже существующего id,
пока оставлю ValueError, потом поменяю.
Импортировал пока все классы и работу с файлами, позже пропишу их
"""

import xml.etree.ElementTree as Et
from structure.classes import Patient, Doctor, MedicalCard, Diagnosis, Prescription
from storage.file_handler import save_to_json, load_from_json, save_to_xml, load_from_xml
from exceptions.custom_errors import PatientNotFoundError, DoctorNotFoundError


class PolyclinicSystem:
    def __init__(self):
        self.patients = {}
        self.doctors = {}
        self.departments = {}

    def add_patient(self, patient):
        if patient.id in self.patients:
            # Забыл прописать свою ошибку для уже существующего id, пока оставлю ValueError, мб так и оставлю
            raise ValueError("Пациент с ID " + patient.id + " уже существует.")
        self.patients[patient.id] = patient

    def get_patient(self, patient_id):
        if patient_id not in self.patients:
            raise PatientNotFoundError("Пациент с ID " + patient_id + " не найден.")
        return self.patients[patient_id]

    def update_patient_phone(self, patient_id, new_phone):
        patient = self.get_patient(patient_id)
        patient.phone = new_phone

    def delete_patient(self, patient_id):
        if patient_id not in self.patients:
            raise PatientNotFoundError("Невозможно удалить: пациент с ID " + patient_id + " не найден.")
        del self.patients[patient_id]

    def add_doctor(self, doctor):
        if doctor.id in self.doctors:
            # Забыл прописать свою ошибку для уже существующего id, пока оставлю ValueError, мб так и оставлю
            raise ValueError("Врач с ID " + doctor.id + " уже существует.")
        self.doctors[doctor.id] = doctor

    def get_doctor(self, doctor_id):
        if doctor_id not in self.doctors:
            raise DoctorNotFoundError("Врач с ID " + doctor_id + " не найден.")
        return self.doctors[doctor_id]

    def add_department(self, department):
        self.departments[department.dept_id] = department

