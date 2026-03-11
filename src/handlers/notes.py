import random
from typing import List, Union

from prettytable import PrettyTable
from colorama import Fore, Style

from models import Note, AddressBook, NoteBook
from utils import input_error

NOTE_COLORS = [Fore.CYAN, Fore.GREEN, Fore.YELLOW, Fore.MAGENTA, Fore.BLUE, Fore.LIGHTWHITE_EX]


def _build_notes_table() -> PrettyTable:
    table = PrettyTable()
    table.field_names = ["ID", "Owner", "Content", "Tags"]
    table.align["Content"] = "l"
    table.align["Owner"] = "l"

    if hasattr(table, "max_widths"):
        table.max_widths = {"Content": 50}
    elif hasattr(table, "max_width"):
        table.max_width = 50

    return table


def _format_tags(tags: List[str]) -> str:
    if not tags:
        return "-"

    colored_tags = [
        f"{random.choice(NOTE_COLORS)}#{tag}{Style.RESET_ALL}"
        for tag in tags
    ]
    return ", ".join(colored_tags)


@input_error
def add_contact_note(args: List[str], book: AddressBook, notes: NoteBook) -> str:
    if len(args) < 2:
        return "Error: Enter name and note text."

    name = args[0]
    text = " ".join(args[1:])
    record = book.find(name)

    if not record:
        return f"Contact {name} not found."

    new_note = record.add_note(text)
    note_id = notes.add_note(new_note, name)
    return f"Note added to {name} (ID: {note_id})."


@input_error
def add_general_note(args: List[str], notes: NoteBook) -> str:
    if not args:
        return "Error: Enter note text."

    text = " ".join(args)
    new_note = Note(text)
    note_id = notes.add_note(new_note)
    return f"General note saved (ID: {note_id})."


def show_notes(args: List[str], notes: NoteBook) -> Union[PrettyTable, str]:
    if not notes.data:
        return "Notebook is empty."

    table = _build_notes_table()

    for note_id, data in notes.data.items():
        note = data["note"]
        owner = data["owner"] if data["owner"] else "---"

        table.add_row([
            note_id,
            owner,
            note.text,
            _format_tags(note.tags),
        ])

    return table


@input_error
def edit_note(args: List[str], notes: NoteBook) -> str:
    if len(args) < 2:
        return "Error: Enter ID and additional text."

    note_id = int(args[0])
    text = " ".join(args[1:])

    if note_id in notes.data:
        notes.data[note_id]["note"].add_to_end(text)
        return f"Note {note_id} updated."

    return "Note not found."


@input_error
def find_note_by_tag(args: List[str], notes: NoteBook) -> Union[PrettyTable, str]:
    if not args:
        return "Error: Please provide a tag (e.g., 'find-tag work')."

    tag_to_find = args[0].lower().replace("#", "")
    table = _build_notes_table()
    found = False

    for note_id, data in notes.data.items():
        note = data["note"]
        owner = data["owner"] if data["owner"] else "---"

        if tag_to_find in note.tags:
            table.add_row([
                note_id,
                owner,
                note.text,
                _format_tags(note.tags),
            ])
            found = True

    return table if found else f"No notes found with tag #{tag_to_find}."


@input_error
def delete_note(args: List[str], notes: NoteBook) -> str:
    note_id = int(args[0])

    if notes.delete_note(note_id):
        return f"Note {note_id} deleted."

    return "Note not found."


def clear_notes(args: List[str], notes: NoteBook) -> str:
    confirm = input("Delete ALL notes? (y/n): ").lower()

    if confirm == "y":
        notes.data.clear()
        return "All notes deleted."

    return "Cancelled."