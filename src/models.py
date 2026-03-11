import phonenumbers
from collections import UserDict
from datetime import datetime, timedelta
from typing import List, Optional
from .helper import normalize_phone

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
        self._value = normalize_phone(new_value)

class Birthday(Field):
    @Field.value.setter
    def value(self, new_value: str) -> None:
        try:
            self._value = datetime.strptime(new_value, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Error: Invalid date format. Use DD.MM.YYYY")

    def __str__(self) -> str:
        return self._value.strftime("%d.%m.%Y")

class Record:
    def __init__(self, name: str) -> None:
        self.name: Name = Name(name)
        self.phones: List[Phone] = []
        self.birthday: Optional[Birthday] = None

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

    def add_birthday(self, birthday_string: str) -> None:
        self.birthday = Birthday(birthday_string)

    def __str__(self) -> str:
        phones_str = "; ".join(p.value for p in self.phones)
        birthday_str = f", birthday: {self.birthday}" if self.birthday else ""
        return f"{self.name.value:10} | {phones_str:20} {birthday_str}"

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