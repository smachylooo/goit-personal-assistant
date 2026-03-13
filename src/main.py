from colorama import init
from typing import Dict, Callable
from handlers.contacts import *
from storage import save_data, load_data
from utils import parse_input
<<<<<<< HEAD
# from handlers import (
#     add_contact, change_contact, show_phones, 
#     add_birthday, show_birthday, birthdays_next_week, add_email, change_email, show_email,
#     add_contact_note, add_general_note, show_notes, 
#     find_note_by_tag, edit_note, delete_note, clear_notes, birthdays, birthday_week, show_help
# )

=======
from models import AddressBook
from handlers import (
    add_contact, change_contact, show_phone, 
    show_all, add_birthday, show_birthday, birthdays_next_week, show_help
)
>>>>>>> d24a03487176ccfb58619fe74dd08ee7f631d6d9

from rich.panel import Panel
from rich.console import Console

console = Console()
<<<<<<< HEAD

console.print(
    Panel(
        "Welcome to the Project_7 Assistant Bot!",
        style="bold yellow",
        expand=False
    )
=======
#console.print(Panel("Welcome to the Assistant Bot!", style="bold green"))
#console.print(Panel("Type 'help' to see available commands.", style="bold green"))
console.print(
    Panel(
        "Welcome to the Assistant Bot!",
        style="bold yellow",
        expand=False
    )
)

console.print(
    Panel(
        "Type 'help' to see available commands.",
        style="bold magenta",
        expand=False
    )
>>>>>>> d24a03487176ccfb58619fe74dd08ee7f631d6d9
)

console.print(
    Panel(
        "Type 'help' to see available commands.",
        style="bright_blue",
        expand=False
    )
)
def main() -> None:
<<<<<<< HEAD
    init(autoreset=True)
    book, notes = load_data()    

    commands: Dict[str, Callable] = {
        "help": show_help,
=======
    book: AddressBook = load_data()
   # print("Welcome to the assistant bot!")
   #print("Type 'help' to see available commands.")

    commands: Dict[str, Callable] = {
        #"hello": lambda args, book: "How can I help you?",
>>>>>>> d24a03487176ccfb58619fe74dd08ee7f631d6d9
        "add": add_contact,
        "change": change_contact,
        "phone": show_phones,
        "add-email": add_email,
        "change-email": change_email,
        "email": show_email,
        "add-birthday": add_birthday,
        "show-birthday": show_birthday,
<<<<<<< HEAD
        "birthdays-next-week": birthdays_next_week,
        "birthdays": birthdays,
        "birthday-week": birthday_week,
        "birthdays-next": birthdays_next_days,
        "search": search_contacts,
        "add-note": lambda args, book: add_contact_note(args, book, notes),
        "note": lambda args, book: add_general_note(args, notes),
        "notes": lambda args, book: show_notes(args, notes),
        "find-tag": lambda args, book: find_note_by_tag(args, notes),
        "edit-note": lambda args, book: edit_note(args, notes),
        "delete-note": lambda args, book: delete_note(args, notes),
        "clear-notes": lambda args, book: clear_notes(args, notes),
=======
        "birthdays": birthdays_next_week,
        "help": show_help
>>>>>>> d24a03487176ccfb58619fe74dd08ee7f631d6d9
    }

    try:
        while True:
            user_input: str = input("Enter a command: ").strip()
            if not user_input: continue

            command, args = parse_input(user_input)

            if command in ["close", "exit"]:
                print("Good bye!")
                break

            handler = commands.get(command)

            if handler:
<<<<<<< HEAD
                console.print(handler(args, book))
=======
                result = handler(args, book)
                if result:
                    console.print(result)
>>>>>>> d24a03487176ccfb58619fe74dd08ee7f631d6d9
            else:
                console.print("[red]Invalid command[/red]")
    finally:
        save_data(book, notes)

if __name__ == "__main__":
    main()