from typing import Dict, Callable
from storage import save_data, load_data
from utils import parse_input
from models import AddressBook
from handlers import (
    add_contact, change_contact, show_phone, 
    show_all, add_birthday, show_birthday, birthdays_next_week, show_help
)

from rich.panel import Panel
from rich.console import Console

console = Console()
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
)

def main() -> None:
    book: AddressBook = load_data()
   # print("Welcome to the assistant bot!")
   #print("Type 'help' to see available commands.")

    commands: Dict[str, Callable] = {
        #"hello": lambda args, book: "How can I help you?",
        "add": add_contact,
        "change": change_contact,
        "phone": show_phone,
        "all": show_all,
        "add-birthday": add_birthday,
        "show-birthday": show_birthday,
        "birthdays": birthdays_next_week,
        "help": show_help
    }

    try:
        while True:
            user_input: str = input("Enter a command: ").strip()
            command, args = parse_input(user_input)

            if command in ["close", "exit"]:
                print("Good bye!")
                break

            handler = commands.get(command)

            if handler:
                result = handler(args, book)
                if result:
                    console.print(result)
            else:
                console.print("[red]Invalid command[/red]")
    finally:
        save_data(book)

if __name__ == "__main__":
    main()