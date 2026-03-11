from collections import UserDict
from datetime import datetime, timedelta
from typing import List, Optional

from .fields import Name, Phone, Email, Birthday
from .notes import Note


class Record:
    def __init__(self, name: str) -> None:
        self.name: Name = Name(name)
        self.phones: List[Phone] = []
        self.birthday: Optional[Birthday] = None
        self.emails: List[Email] = []
        self.notes: List[Note] = []

    def find_phone(self, phone_number: str) -> Optional[Phone]:
        for phone in self.phones:
            if phone.value == Phone(phone_number).value:
                return phone
        return None

    def add_phone(self, phone_number: str) -> None:
        if self.find_phone(phone_number):
            raise ValueError(f"Error: Phone {phone_number} already exists.")
        self.phones.append(Phone(phone_number))

    def edit_phone(self, old_number: str, new_number: str) -> None:
        phone_obj = self.find_phone(old_number)
        if not phone_obj:
            raise ValueError(f"Error: Phone {old_number} not found.")

        existing_phone = self.find_phone(new_number)
        if existing_phone and existing_phone is not phone_obj:
            raise ValueError(f"Error: Phone {new_number} already exists.")

        phone_obj.value = new_number

    def find_email(self, email: str) -> Optional[Email]:
        email = email.strip()
        for item in self.emails:
            if item.value == email:
                return item
        return None

    def add_email(self, email: str) -> None:
        if self.find_email(email):
            raise ValueError(f"Error: Email {email} already exist.")
        self.emails.append(Email(email))

    def edit_email(self, old_email: str, new_email: str) -> None:
        old_email = old_email.strip()
        new_email = new_email.strip()

        email_obj = self.find_email(old_email)
        if not email_obj:
            raise ValueError(f"Error: Email {old_email} not found.")

        existing = self.find_email(new_email)
        if existing and existing is not email_obj:
            raise ValueError("Email already exists.")

        email_obj.value = new_email

    def add_birthday(self, birthday_string: str) -> None:
        self.birthday = Birthday(birthday_string)

    def add_note(self, text: str) -> Note:
        new_note = Note(text)
        self.notes.append(new_note)
        return new_note

    def __str__(self) -> str:
        phones_str = "; ".join(phone.value for phone in self.phones)
        emails_str = "; ".join(email.value for email in self.emails)
        birthday_str = str(self.birthday) if self.birthday else "-"
        notes_str = str(len(self.notes))

        return (
            f"{self.name.value:20} | "
            f"{phones_str:20} | "
            f"{emails_str:25} | "
            f"{birthday_str:12} | "
            f"notes: {notes_str}"
        )


class AddressBook(UserDict):
    def add_record(self, record: Record) -> None:
        self.data[record.name.value] = record

    def find(self, name: str) -> Optional[Record]:
        return self.data.get(name)

    def get_upcoming_birthdays(self) -> List[dict]:
        upcoming: List[dict] = []
        today = datetime.today().date()

        for record in self.data.values():
            if not record.birthday:
                continue

            birthday_this_year = record.birthday.value.replace(year=today.year)

            if birthday_this_year < today:
                birthday_this_year = birthday_this_year.replace(year=today.year + 1)

            if 0 <= (birthday_this_year - today).days <= 7:
                congratulation_date = birthday_this_year

                if birthday_this_year.weekday() == 5:
                    congratulation_date += timedelta(days=2)
                elif birthday_this_year.weekday() == 6:
                    congratulation_date += timedelta(days=1)

                upcoming.append({
                    "name": record.name.value,
                    "congratulation_date": congratulation_date.strftime("%d.%m.%Y"),
                })

        return upcoming