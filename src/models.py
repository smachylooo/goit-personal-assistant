import re
import phonenumbers
from collections import UserDict
from datetime import datetime, timedelta
from typing import List, Optional
from helper import is_valid_email, normalize_phone

class Field:
    def __init__(self, value: str) -> None:
        self.value = value

    @property
    def value(self) -> str:
        return self._value

    @value.setter
    def value(self, new_value: str) -> None:
        self._value = new_value

    def __str__(self) -> str:
        return str(self._value)

class Name(Field):
    @Field.value.setter
    def value(self, new_value: str) -> None:
        if not new_value.strip():
            raise ValueError("Error: Name cannot be empty.")
        self._value = new_value.strip()

class Phone(Field):
    @Field.value.setter
    def value(self, new_value: str) -> None:
        self._value = normalize_phone(new_value)

class Email(Field):
    @Field.value.setter
    def value(self, new_value: str) -> None:
        if not new_value.strip():
            raise ValueError("Error: Email cannot be empty.")
        if not is_valid_email(new_value):
            raise ValueError('Error: email address is wrong.')
        self._value = new_value

class Birthday(Field):
    @Field.value.setter
    def value(self, new_value: str) -> None:
        try:
            self._value = datetime.strptime(new_value, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Error: Invalid date format. Use DD.MM.YYYY")

    def __str__(self) -> str:
        return self._value.strftime("%d.%m.%Y")

class Note:
    def __init__(self, text: str) -> None:
        if len(text) > 500:
            raise ValueError("Error: Note too long (max 500 chars).")
        self.text: str = text
        self.tags: List[str] = [t.lower() for t in re.findall(r'#(\w+)', text)]

    def add_to_end(self, additional_text: str) -> None:
        new_text = self.text + " " + additional_text
        if len(new_text) > 500:
            raise ValueError("Error: Note would exceed 500 chars.")
        self.text = new_text
        new_tags = re.findall(r'#(\w+)', additional_text)
        for tag in new_tags:
            t_l = tag.lower()
            if t_l not in self.tags: self.tags.append(t_l)

class Record:
    def __init__(self, name: str) -> None:
        self.name: Name = Name(name)
        self.phones: List[Phone] = []
        self.birthday: Optional[Birthday] = None
        self.emails: List[Email] = []
        self.notes: List[Note] = []

    def find_phone(self, phone_number: str) -> Optional[Phone]:
        normalized = normalize_phone(phone_number)
        for phone in self.phones:
            if phone.value == normalized:
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

    def find_email(self, email: str):
        for e in self.emails:
            if e.value == email:
                return e
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
        phones_str = "; ".join(p.value for p in self.phones)
        emails_str = "; ".join(e.value for e in self.emails)
        birthday_str = f", birthday: {self.birthday}" if self.birthday else ""
        notes_str = f"notes: {len(self.notes)}" if self.notes else ""
        return f"{self.name.value:20} | {phones_str:20} | {emails_str:20} | {birthday_str:10} | {notes_str}"

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
            bday = record.birthday.value.replace(year=today.year)
            if bday < today:
                bday = bday.replace(year=today.year + 1)
            if 0 <= (bday - today).days <= 7:
                congr_date = bday
                if bday.weekday() == 5: congr_date += timedelta(days=2)
                elif bday.weekday() == 6: congr_date += timedelta(days=1)
                upcoming.append({"name": record.name.value, "congratulation_date": congr_date.strftime("%d.%m.%Y")})
        return upcoming


class NoteBook(UserDict):
    def add_note(self, note: Note, contact_name: Optional[str] = None) -> int:
        note_id = max(self.data.keys(), default=0) + 1
        # Зберігаємо і саму нотатку, і ім'я контакту (якщо воно є)
        self.data[note_id] = {
            "note": note,
            "owner": contact_name # Може бути None для загальних нотаток
        }
        return note_id

    def delete_note(self, note_id: int) -> bool:
        if note_id in self.data:
            del self.data[note_id]
            return True
        return False