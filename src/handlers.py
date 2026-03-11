from typing import List
from models import Record, AddressBook
from utils import input_error

from rich.console import Console
from rich.table import Table

console = Console()


@input_error
def add_contact(args: List[str], book: AddressBook) -> str:
    name, phone = args
    record = book.find(name)

    if record is None:
        record = Record(name)
        book.add_record(record)
        record.add_phone(phone)
        return f"[green]✔ Contact '{name}' added with phone {phone}[/green]"

    record.add_phone(phone)
    return f"[cyan]📞 Phone {phone} added to contact '{name}'[/cyan]"


@input_error
def change_contact(args: List[str], book: AddressBook) -> str:
    name, old_p, new_p = args
    record = book.find(name)

    if not record:
        raise KeyError

    record.edit_phone(old_p, new_p)

    return f"[yellow]✏ Phone for '{name}' updated: {old_p} → {new_p}[/yellow]"


@input_error
def show_phone(args: List[str], book: AddressBook) -> str:
    name = args[0]
    record = book.find(name)

    if not record:
        raise KeyError

    phones = ", ".join(p.value for p in record.phones)

    return f"[cyan]📞 {name}: {phones}[/cyan]"


@input_error
def add_birthday(args: List[str], book: AddressBook) -> str:
    name, bday = args
    record = book.find(name)

    if not record:
        raise KeyError

    record.add_birthday(bday)

    return f"[magenta]🎂 Birthday for '{name}' set to {bday}[/magenta]"


@input_error
def show_birthday(args: List[str], book: AddressBook) -> str:
    name = args[0]
    record = book.find(name)

    if not record or not record.birthday:
        return "[red]Birthday not found[/red]"

    return f"[magenta]🎂 {name}'s birthday: {record.birthday}[/magenta]"


def show_all(args: List[str], book: AddressBook) -> str:
    if not book.data:
        return "[yellow]Address book is empty[/yellow]"

    return "\n".join(str(record) for record in book.data.values())


def birthdays_next_week(args: List[str], book: AddressBook) -> str:
    upcoming = book.get_upcoming_birthdays()

    if not upcoming:
        return "[yellow]No upcoming birthdays[/yellow]"

    result = "\n".join(
        f"[magenta]🎉 {u['name']} → {u['congratulation_date']}[/magenta]"
        for u in upcoming
    )

    return result


def show_help(args, book):

    table = Table(
        title="Assistant Bot Commands",
        header_style="bold white",
        border_style="bright_blue",
        expand=True
    )

    table.add_column("Command", style="cyan", no_wrap=True)
    table.add_column("Arguments", style="yellow", no_wrap=True)
    table.add_column("Description", style="green")

    table.add_row("add", r"\[name] \[phone]", "Add a new contact")
    table.add_row("change", r"\[name] \[old_phone] \[new_phone]", "Change phone number")
    table.add_row("phone", r"\[name]", "Show phone numbers for contact")
    table.add_row("all", "no arguments needed", "Show all contacts")
    table.add_row("add-birthday", r"\[name] \[DD.MM.YYYY]", "Add birthday to contact")
    table.add_row("show-birthday", r"\[name]", "Show contact birthday")
    table.add_row("birthdays", "no arguments needed", "Show upcoming birthdays within a week")
    table.add_row("help", "no arguments needed", "Show this help message")
    table.add_row("exit / close", "no arguments needed", "Exit the program")

    console.print(table)

    return ""