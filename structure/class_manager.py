"""
В этом файле прописана работа со всеми классами.
Использованы встроенные модули json и xml.etree.ElementTree
Также имеется обработка исключений из exceptions.
Импортировал пока все классы и работу с файлами.
"""

import xml.etree.ElementTree as Et
from structure.classes import Patient, Doctor, MedicalCard, Diagnosis, Prescription
from storage.file_handler import save_to_json, load_from_json, save_to_xml, load_from_xml
from exceptions.custom_errors import (PatientNotFoundError, PatientAlreadyExistError, DoctorNotFoundError,
                                      DoctorAlreadyExistError)


class PolyclinicSystem:
    def __init__(self):
        self.patients = {}
        self.doctors = {}
        self.departments = {}

    def add_patient(self, patient):
        if patient.id in self.patients:
            raise PatientAlreadyExistError("Пациент с ID " + patient.id + " уже существует.")
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
            raise DoctorAlreadyExistError("Врач с ID " + doctor.id + " уже существует.")
        self.doctors[doctor.id] = doctor

    def get_doctor(self, doctor_id):
        if doctor_id not in self.doctors:
            raise DoctorNotFoundError("Врач с ID " + doctor_id + " не найден.")
        return self.doctors[doctor_id]

    def add_department(self, department):
        self.departments[department.dept_id] = department

    # Экспорт в JSON
    def export_to_json(self, filepath):
        # Основной блок
        data = {"polyclinic": {"patients": [], "doctors": []}}

        # Блок о пациенте
        for p in self.patients.values():
            patient_dict = {
                "id": p.id,
                "full_name": p.full_name,
                "birth_date": p.birth_date,
                "phone": p.phone,
                "policy_number": p.policy_number,
                "address": p.address,
                "medical_card": {
                    "record_id": p.medical_card.card_id,
                    # Подблок о диагнозе
                    "diagnoses": [
                        {"icd_code": d.icd_code, "description": d.description, "date": d.date}
                        for d in p.medical_card.diagnoses
                    ],
                    # Подблок о рецепте
                    "prescriptions": [
                        {"medication": pr.medication, "dosage": pr.dosage, "duration_days": pr.duration_days}
                        for pr in p.medical_card.prescriptions
                    ]
                }
            }
            data["polyclinic"]["patients"].append(patient_dict)

        # Блок о врачах
        for d in self.doctors.values():
            doctor_dict = {
                "id": d.id,
                "full_name": d.full_name,
                "birth_date": d.birth_date,
                "phone": d.phone,
                "employee_id": d.employee_id,
                "position": d.position,
                "salary": d.salary,
                "specialization": d.specialization,
                "office_number": d.office_number
            }
            data["polyclinic"]["doctors"].append(doctor_dict)

        save_to_json(data, filepath)

    # Импорт из JSON
    def import_from_json(self, filepath):
        data = load_from_json(filepath)
        # Основной блок
        polyclinic_data = data.get("polyclinic", {})

        # Блок о пациенте
        for p_data in polyclinic_data.get("patients", []):
            mc_data = p_data.get("medical_card", {})
            mc = MedicalCard(card_id=mc_data.get("card_id", ""), patient_id=p_data["id"])

            # Подблок о диагнозе
            for d in mc_data.get("diagnoses", []):
                mc.diagnoses.append(Diagnosis(icd_code=d["icd_code"], description=d["description"], date=d["date"]))

            # Подблок о рецепте
            for pr in mc_data.get("prescriptions", []):
                mc.prescriptions.append(Prescription(
                    medication=pr["medication"], dosage=pr["dosage"], duration_days=pr["duration_days"]
                ))

            patient = Patient(
                person_id=p_data["id"], full_name=p_data["full_name"], birth_date=p_data["birth_date"],
                phone=p_data["phone"], policy_number=p_data["policy_number"], address=p_data["address"]
            )
            patient.medical_record = mc
            self.patients[patient.id] = patient

        # Блок о врачах
        for d_data in polyclinic_data.get("doctors", []):
            doctor = Doctor(
                person_id=d_data["id"], full_name=d_data["full_name"], birth_date=d_data["birth_date"],
                phone=d_data["phone"], employee_id=d_data["employee_id"], position=d_data["position"],
                salary=d_data["salary"], specialization=d_data["specialization"],
                office_number=d_data["office_number"]
            )
            self.doctors[doctor.id] = doctor

    # Экспорт в XML
    def export_to_xml(self, filepath):
        # Основной блок
        root = Et.Element("polyclinic")

        # Блок о пациенте
        patients_elem = Et.SubElement(root, "patients")
        for p in self.patients.values():
            p_elem = Et.SubElement(patients_elem, "patient", id=p.id)
            Et.SubElement(p_elem, "full_name").text = p.full_name
            Et.SubElement(p_elem, "birth_date").text = p.birth_date
            Et.SubElement(p_elem, "phone").text = p.phone
            Et.SubElement(p_elem, "policy_number").text = p.policy_number
            Et.SubElement(p_elem, "address").text = p.address

            mc_elem = Et.SubElement(p_elem, "medical_card", card_id=p.medical_card.card_id)

            # Подблок о диагнозе
            diagnoses_elem = Et.SubElement(mc_elem, "diagnoses")
            for d in p.medical_card.diagnoses:
                d_elem = Et.SubElement(diagnoses_elem, "diagnosis", icd_code=d.icd_code, date=d.date)
                d_elem.text = d.description

            # Подблок о рецепте
            prescriptions_elem = Et.SubElement(mc_elem, "prescriptions")
            for pr in p.medical_card.prescriptions:
                pr_elem = Et.SubElement(prescriptions_elem, "prescription", duration_days=str(pr.duration_days))
                Et.SubElement(pr_elem, "medication").text = pr.medication
                Et.SubElement(pr_elem, "dosage").text = pr.dosage

        # Блок о врачах
        doctors_elem = Et.SubElement(root, "doctors")
        for d in self.doctors.values():
            d_elem = Et.SubElement(doctors_elem, "doctor", id=d.id)
            Et.SubElement(d_elem, "full_name").text = d.full_name
            Et.SubElement(d_elem, "birth_date").text = d.birth_date
            Et.SubElement(d_elem, "phone").text = d.phone
            Et.SubElement(d_elem, "employee_id").text = d.employee_id
            Et.SubElement(d_elem, "position").text = d.position
            Et.SubElement(d_elem, "salary").text = str(d.salary)
            Et.SubElement(d_elem, "specialization").text = d.specialization
            Et.SubElement(d_elem, "office_number").text = d.office_number

        save_to_xml(root, filepath)

    # Импорт из XML
    def import_from_xml(self, filepath):
        root = load_from_xml(filepath)

        # Импорт пациентов
        for p_elem in root.findall(".//patient"):
            patient_id = p_elem.get("id")
            full_name = p_elem.find("full_name").text
            birth_date = p_elem.find("birth_date").text
            phone = p_elem.find("phone").text
            policy_number = p_elem.find("policy_number").text
            address = p_elem.find("address").text

            patient = Patient(
                person_id=patient_id, full_name=full_name, birth_date=birth_date,
                phone=phone, policy_number=policy_number, address=address
            )

            mc_elem = p_elem.find("medical_record")
            if mc_elem is not None:
                mr = MedicalCard(card_id=mc_elem.get("card_id", ""), patient_id=patient_id)
                for d_elem in mc_elem.findall(".//diagnosis"):
                    mr.diagnoses.append(Diagnosis(
                        icd_code=d_elem.get("icd_code"), description=d_elem.text, date=d_elem.get("date")
                    ))
                for pr_elem in mc_elem.findall(".//prescription"):
                    mr.prescriptions.append(Prescription(
                        medication=pr_elem.find("medication").text,
                        dosage=pr_elem.find("dosage").text,
                        duration_days=int(pr_elem.get("duration_days"))
                    ))
                patient.medical_record = mr

            self.patients[patient.id] = patient

        # Импорт врачей
        for d_elem in root.findall(".//doctor"):
            doctor = Doctor(
                person_id=d_elem.get("id"),
                full_name=d_elem.find("full_name").text,
                birth_date=d_elem.find("birth_date").text,
                phone=d_elem.find("phone").text,
                employee_id=d_elem.find("employee_id").text,
                position=d_elem.find("position").text,
                salary=float(d_elem.find("salary").text),
                specialization=d_elem.find("specialization").text,
                office_number=d_elem.find("office_number").text
            )
            self.doctors[doctor.id] = doctor
