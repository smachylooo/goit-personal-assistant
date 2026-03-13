import re
import phonenumbers
from rich.console import Console
from rich.table import Table
from rich.markup import escape
console = Console()

EMAIL_REGEX = r'^[\w\.-]+@[\w\.-]+\.\w+$'
def is_valid_email(email: str) -> bool:
    return re.match(EMAIL_REGEX, email) is not None

def normalize_phone(phone_number: str) -> str:
    parsed = phonenumbers.parse(phone_number, "UA")
    if not phonenumbers.is_valid_number(parsed):
        raise ValueError("Error: Invalid phone number")
    
    return phonenumbers.format_number(
        parsed,
        phonenumbers.PhoneNumberFormat.E164
    )



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

    table.add_row("add", escape("[name] [phone]"), "Add new contact or add phone")
    table.add_row("change", escape("[name] [old_phone] [new_phone]"), "Change phone number")
    table.add_row("phone", escape("[name]"), "Show contact phone numbers")

    table.add_row("add-email", escape("[name] [email]"), "Add email to contact")
    table.add_row("change-email", escape("[name] [old_email] [new_email]"), "Change contact email")
    table.add_row("email", escape("[name]"), "Show contact emails")

    table.add_row("add-birthday", escape("[name] [DD.MM.YYYY]"), "Add birthday to contact")
    table.add_row("show-birthday", escape("[name]"), "Show contact birthday")

    table.add_row("birthdays-next-week", "-", "Show upcoming birthdays in next week")
    table.add_row("birthdays", "-", "Show all contacts with birthdays")
    table.add_row("birthday-week", escape("[month] [week]"), "Birthdays in specific week of month")
    table.add_row("birthdays-next", escape("[days]"), "Birthdays within next N days")

    table.add_row("search", escape("[query]"), "Search contacts by name or phone")

    table.add_row("add-note", escape("[name] [text]"), "Add note to contact")
    table.add_row("note", escape("[text]"), "Add general note")
    table.add_row("notes", "-", "Show all notes")
    table.add_row("find-tag", escape("[tag]"), "Find notes by tag")
    table.add_row("edit-note", escape("[note_id] [new_text]"), "Edit existing note")
    table.add_row("delete-note", escape("[note_id]"), "Delete note")
    table.add_row("clear-notes", "-", "Delete all notes")

    table.add_row("help", "-", "Show this help message")
    table.add_row("exit / close", "-", "Exit the program")

    console.print(table)