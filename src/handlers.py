from typing import List
from .models import Record, AddressBook
from .utils import input_error

@input_error
def add_contact(args: List[str], book: AddressBook) -> str:
    name, phone = args
    record = book.find(name)
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    else:
        message = "Phone added."
    record.add_phone(phone)
    return message

@input_error
def change_contact(args: List[str], book: AddressBook) -> str:
    name, old_p, new_p = args
    record = book.find(name)
    if not record: raise KeyError
    record.edit_phone(old_p, new_p)
    return "Contact updated."

@input_error
def show_phone(args: List[str], book: AddressBook) -> str:
    name = args[0]
    record = book.find(name)
    if not record: raise KeyError
    return f"{name}: {', '.join(p.value for p in record.phones)}"

@input_error
def add_birthday(args: List[str], book: AddressBook) -> str:
    name, bday = args
    record = book.find(name)
    if not record: raise KeyError
    record.add_birthday(bday)
    return "Birthday added."

@input_error
def show_birthday(args: List[str], book: AddressBook) -> str:
    name = args[0]
    record = book.find(name)
    if not record or not record.birthday: return "Error: Birthday not found."
    return f"{name}'s birthday: {record.birthday}"

def show_all(args: List[str], book: AddressBook) -> str:
    if not book.data: return "Book is empty."
    return "\n".join([str(record) for record in book.data.values()])

def birthdays_next_week(args: List[str], book: AddressBook) -> str:
    upcoming = book.get_upcoming_birthdays()
    if not upcoming: return "No upcoming birthdays."
    return "\n".join([f"{u['name']}: {u['congratulation_date']}" for u in upcoming])