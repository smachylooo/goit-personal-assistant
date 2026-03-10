from typing import List, Union
from prettytable import PrettyTable
from colorama import Fore, Style
from models import Record, AddressBook, Note, NoteBook
from utils import input_error

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

# --- NOTES HANDLERS (with PrettyTable + Colorama) ---

@input_error
def add_note(args: List[str], notes: NoteBook) -> str:
    text = " ".join(args)
    note_id = notes.add_note(Note(text))
    return f"Note added with ID: {note_id}"

def show_notes(args: List[str], notes: NoteBook):
    if not notes.data: return "Notebook is empty."
    table = PrettyTable()
    table.field_names = ["ID", "Content", "Tags"]
    table.align["Content"] = "l"
    table._max_width = {"Content": 50}
    
    for nid, note in notes.data.items():
        # Тільки тут використовуємо кольори для тегів
        colored_tags = [f"{Fore.CYAN}#{t}{Style.RESET_ALL}" for t in note.tags]
        table.add_row([nid, note.text, ", ".join(colored_tags) or "-"])
    return table

@input_error
def edit_note(args: List[str], notes: NoteBook) -> str:
    note_id, text = int(args[0]), " ".join(args[1:])
    if note_id in notes.data:
        notes.data[note_id].add_to_end(text)
        return f"Note {note_id} updated."
    return "Note not found."

@input_error
def find_note_by_tag(args: List[str], notes: NoteBook) -> Union[PrettyTable, str]:
    if not args:
        return "Error: Please provide a tag to search for (e.g., 'find-tag work')."
    
    tag_to_find = args[0].lower().replace("#", "") # Видаляємо #, якщо користувач його ввів
    
    # Створюємо таблицю для результатів
    table = PrettyTable()
    table.field_names = ["ID", "Content", "Tags"]
    table.align["Content"] = "l"
    table._max_width = {"Content": 50}
    
    found = False
    for nid, note in notes.data.items():
        if tag_to_find in note.tags:
            colored_tags = [f"{Fore.CYAN}#{t}{Style.RESET_ALL}" for t in note.tags]
            table.add_row([nid, note.text, ", ".join(colored_tags)])
            found = True
            
    if not found:
        return f"No notes found with tag #{tag_to_find}."
    
    return table

@input_error
def delete_note(args: List[str], notes: NoteBook) -> str:
    note_id = int(args[0])
    if notes.delete_note(note_id): return f"Note {note_id} deleted."
    return "Note not found."

def clear_notes(args: List[str], notes: NoteBook) -> str:
    confirm = input("Delete ALL notes? (y/n): ").lower()
    if confirm == 'y':
        notes.data.clear()
        return "All notes deleted."
    return "Cancelled."