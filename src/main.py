from typing import Dict, Callable
from storage import save_data, load_data
from utils import parse_input
from models import AddressBook
from handlers import (
    add_contact, change_contact, show_phone, 
    show_all, add_birthday, show_birthday, birthdays_next_week
)

def main() -> None:
    book: AddressBook = load_data()
    print("Welcome to the assistant bot!")
    
    commands: Dict[str, Callable] = {
        "hello": lambda args, book: "How can I help you?",
        "add": add_contact,
        "change": change_contact,
        "phone": show_phones,
        "all": show_all,
        "add-email": add_email,
        "change-email": change_email,
        "email": show_email,
        "add-birthday": add_birthday,
        "show-birthday": show_birthday,
        "birthdays": birthdays_next_week,
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
                print(handler(args, book))
            else:
                print("Invalid command.")
    finally:
        save_data(book)

if __name__ == "__main__":
    main()