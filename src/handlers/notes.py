import random
from typing import List

from rich.table import Table
from rich.console import Console
from rich.text import Text

from models import Note, AddressBook, NoteBook
from utils import input_error

console = Console()

NOTE_COLORS = [
    "cyan",
    "green",
    "yellow",
    "magenta",
    "blue",
    "white",
]


def _build_notes_table() -> Table:
    table = Table(
        title="📚 Notes",
        header_style="bold white",
        border_style="bright_blue",
        expand=True
    )

    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("Owner", style="green")
    table.add_column("Content", style="white")
    table.add_column("Tags", style="yellow")

    return table


def _format_tags(tags: List[str]):
    if not tags:
        return "-"

    text = Text()

    for i, tag in enumerate(tags):
        color = random.choice(NOTE_COLORS)
        text.append(f"#{tag}", style=color)

        if i < len(tags) - 1:
            text.append(", ")

    return text


@input_error
def add_contact_note(args: List[str], book: AddressBook, notes: NoteBook) -> str:
    if len(args) < 2:
        return "[red]❌ Error: Enter name and note text[/red]"

    name = args[0]
    text = " ".join(args[1:])
    record = book.find(name)

    if not record:
        return f"[red]❌ Contact '{name}' not found[/red]"

    new_note = record.add_note(text)
    note_id = notes.add_note(new_note, name)

    return f"[green]📎 Note added to '{name}' (ID: {note_id})[/green]"


@input_error
def add_general_note(args: List[str], notes: NoteBook) -> str:
    if not args:
        return "[red]❌ Error: Enter note text[/red]"

    text = " ".join(args)
    new_note = Note(text)
    note_id = notes.add_note(new_note)

    return f"[green]📝 Note saved (ID: {note_id})[/green]"


def show_notes(args: List[str], notes: NoteBook):
    if not notes.data:
        console.print("[yellow]📚 Notebook is empty[/yellow]")
        return

    table = _build_notes_table()

    for note_id, data in notes.data.items():
        note = data["note"]
        owner = data["owner"] if data["owner"] else "---"

        table.add_row(
            str(note_id),
            owner,
            note.text,
            _format_tags(note.tags),
        )

    console.print(table)


@input_error
def edit_note(args: List[str], notes: NoteBook) -> str:
    if len(args) < 2:
        return "[red]❌ Error: Enter ID and additional text[/red]"

    note_id = int(args[0])
    text = " ".join(args[1:])

    if note_id in notes.data:
        notes.data[note_id]["note"].add_to_end(text)
        return f"[yellow]✏ Note {note_id} updated[/yellow]"

    return "[red]❌ Note not found[/red]"


@input_error
def find_note_by_tag(args: List[str], notes: NoteBook):
    if not args:
        console.print("[red]❌ Error: Provide a tag (e.g., 'find-tag work')[/red]")
        return

    tag_to_find = args[0].lower().replace("#", "")
    table = _build_notes_table()

    found = False

    for note_id, data in notes.data.items():
        note = data["note"]
        owner = data["owner"] if data["owner"] else "---"

        if tag_to_find in note.tags:
            table.add_row(
                str(note_id),
                owner,
                note.text,
                _format_tags(note.tags),
            )
            found = True

    if found:
        console.print(table)
    else:
        console.print(f"[yellow]🔎 No notes found with tag #{tag_to_find}[/yellow]")


@input_error
def delete_note(args: List[str], notes: NoteBook) -> str:
    note_id = int(args[0])

    if notes.delete_note(note_id):
        return f"[red]🗑 Note {note_id} deleted[/red]"

    return "[red]❌ Note not found[/red]"


def clear_notes(args: List[str], notes: NoteBook) -> str:
    confirm = input("Delete ALL notes? (y/n): ").lower()

    if confirm == "y":
        notes.data.clear()
        return "[red]🗑 All notes deleted[/red]"

    return "[yellow]⚠ Operation cancelled[/yellow]"