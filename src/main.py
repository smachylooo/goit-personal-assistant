from colorama import init
from typing import Dict, Callable
from handlers.contacts import birthdays_next_days, search_contacts
from storage import save_data, load_data
from utils import parse_input
from handlers import (
    add_contact, change_contact, show_phones, 
    add_birthday, show_birthday, birthdays_next_week, add_email, change_email, show_email,
    add_contact_note, add_general_note, show_notes, 
    find_note_by_tag, edit_note, delete_note, clear_notes, birthdays, birthday_week
)


def main() -> None:
    init(autoreset=True)
    book, notes = load_data()    
    
    print("Welcome to the assistant bot!")
    commands: Dict[str, Callable] = {
        "hello": lambda args, b: "How can I help you?",
        "add": add_contact,
        "change": change_contact,
        "phone": show_phones,
        "add-email": add_email,
        "change-email": change_email,
        "email": show_email,
        "add-birthday": add_birthday,
        "show-birthday": show_birthday,
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
                print(handler(args, book))
            else:
                print("Invalid command.")
    finally:
        save_data(book, notes)

if __name__ == "__main__":
    main()