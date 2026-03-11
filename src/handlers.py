import random
from typing import List, Union
from prettytable import PrettyTable
from colorama import Fore, Style
from models import Record, AddressBook, Note, NoteBook
from utils import input_error

NOTE_COLORS = [Fore.CYAN, Fore.GREEN, Fore.YELLOW, Fore.MAGENTA, Fore.BLUE, Fore.LIGHTWHITE_EX]

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

# 1. Додавання нотатки КОНКРЕТНОМУ контакту
@input_error
def add_contact_note(args, book: AddressBook, notes: NoteBook):
    if len(args) < 2:
        return "Error: Enter name and note text."
    name, text = args[0], " ".join(args[1:])
    record = book.find(name)
    if not record:
        return f"Contact {name} not found."
    
    new_note = record.add_note(text) # Додали в контакт
    note_id = notes.add_note(new_note, contact_name=name) # Синхронізували в блокнот
    return f"Note added to {name} (ID: {note_id})."

@input_error
def add_general_note(args, notes: NoteBook):
    if not args:
        return "Error: Enter note text."
    text = " ".join(args)
    new_note = Note(text)
    note_id = notes.add_note(new_note) # owner буде None
    return f"General note saved (ID: {note_id})."

def show_notes(args: List[str], notes: NoteBook):
    if not notes.data: return "Notebook is empty."
    table = PrettyTable()
    table.field_names = ["ID", "Owner", "Content", "Tags"] # Додано Owner
    table.align["Content"] = "l"
    # Use PrettyTable public API for column widths instead of private _max_width
    if hasattr(table, "max_widths"):
        table.max_widths = {"Content": 50}
    elif hasattr(table, "max_width"):
        table.max_width = 50
    
    for nid, data in notes.data.items():
        note = data["note"] # Дістаємо нотатку зі словника
        owner = data["owner"] if data["owner"] else "---"
        colored_tags = [f"{random.choice(NOTE_COLORS)}#{t}{Style.RESET_ALL}" for t in note.tags]
        table.add_row([nid, owner, note.text, ", ".join(colored_tags) or "-"])
    return table

@input_error
def edit_note(args: List[str], notes: NoteBook) -> str:
    if len(args) < 2:
        return "Error: Enter ID and additional text."
    note_id, text = int(args[0]), " ".join(args[1:])
    if note_id in notes.data:
        # Дістаємо об'єкт нотатки зі словника для редагування
        notes.data[note_id]["note"].add_to_end(text)
        return f"Note {note_id} updated."
    return "Note not found."

@input_error
def find_note_by_tag(args: List[str], notes: NoteBook) -> Union[PrettyTable, str]:
    if not args:
        return "Error: Please provide a tag (e.g., 'find-tag work')."
    
    tag_to_find = args[0].lower().replace("#", "")
    colors = [Fore.CYAN, Fore.GREEN, Fore.YELLOW, Fore.MAGENTA, Fore.BLUE, Fore.LIGHTWHITE_EX]
    
    table = PrettyTable()
    table.field_names = ["ID", "Owner", "Content", "Tags"]
    table.align["Content"] = "l"
    table.align["Owner"] = "l"
    table._max_width = {"Content": 50}
    
    found = False
    for nid, data in notes.data.items():
        note = data["note"]
        owner = data["owner"] if data["owner"] else "---"
        if tag_to_find in note.tags:
            # Магія випадкових кольорів для тегів
            colored_tags = [f"{random.choice(colors)}#{t}{Style.RESET_ALL}" for t in note.tags]
            table.add_row([nid, owner, note.text, ", ".join(colored_tags)])
            found = True
            
    return table if found else f"No notes found with tag #{tag_to_find}."
    

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