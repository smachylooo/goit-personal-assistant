from datetime import datetime
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
            raise ValueError("Error: email address is wrong.")
        self._value = new_value.strip()


class Birthday(Field):
    @Field.value.setter
    def value(self, new_value: str) -> None :
        if isinstance(new_value, str):
            try:
                new_value = datetime.strptime(new_value, "%d.%m.%Y").date()
            except ValueError:
                raise ValueError("Invalid birthday format. Use DD.MM.YYYY")
        self._value = new_value