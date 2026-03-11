import re
from collections import UserDict
from datetime import datetime, timedelta
from typing import List, Optional

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
        if not new_value or not new_value.strip():
            raise ValueError("Error: Name cannot be empty.")
        self._value = new_value.strip()

class Phone(Field):
    @Field.value.setter
    def value(self, new_value: str) -> None:
        if not (new_value.isdigit() and len(new_value) == 10):
            raise ValueError("Error: Phone number must contain 10 digits.")
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
        self.address: Optional[str] = None
        self.notes: List[Note] = []

    def add_phone(self, phone_number: str) -> None:
        self.phones.append(Phone(phone_number))

    def find_phone(self, phone_number: str) -> Optional[Phone]:
        for phone in self.phones:
            if phone.value == phone_number:
                return phone
        return None

    def edit_phone(self, old_number: str, new_number: str) -> None:
        phone_obj = self.find_phone(old_number)
        if not phone_obj:
            raise ValueError(f"Error: Phone {old_number} not found.")
        phone_obj.value = new_number

    def add_birthday(self, birthday_string: str) -> None:
        self.birthday = Birthday(birthday_string)

    def add_note(self, text: str) -> Note:
        new_note = Note(text)
        self.notes.append(new_note)
        return new_note

    def __str__(self) -> str:
        phones_str = "; ".join(p.value for p in self.phones)
        birthday_str = f", birthday: {self.birthday}" if self.birthday else ""
        notes_str = f", notes: {len(self.notes)}" if self.notes else ""
        return f"{self.name.value:10} | {phones_str:20} {birthday_str}{notes_str}"
    
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