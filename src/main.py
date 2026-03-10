from typing import Dict, Callable
from colorama import init
from storage import save_data, load_data
from utils import parse_input
from models import AddressBook, NoteBook
from handlers import (
    add_contact, change_contact, show_phone, 
    show_all, add_birthday, show_birthday, birthdays_next_week,
    add_note, show_notes, edit_note, delete_note, find_note_by_tag # Нотатки
)

def main() -> None:
    # Ініціалізація colorama для кольорових тегів у нотатках
    init(autoreset=True)
    
    # Завантажуємо обидві бази даних
    book: AddressBook = load_data("addressbook.pkl", AddressBook)
    notes: NoteBook = load_data("notes.pkl", NoteBook)
    
    print("Welcome to the assistant bot!")
    
    # Словник команд тепер підтримує різні типи об'єктів
    # Використовуємо lambda, щоб передати правильний об'єкт (book або notes)
    commands: Dict[str, Callable] = {
        "hello": lambda args, b: "How can I help you?",
        "add": add_contact,
        "change": change_contact,
        "phone": show_phone,
        "all": show_all,
        "add-birthday": add_birthday,
        "show-birthday": show_birthday,
        "birthdays": birthdays_next_week,
        # Команди для нотаток (передаємо об'єкт notes)
        "add-note": lambda args, b: add_note(args, notes),
        "notes": lambda args, b: show_notes(args, notes),
        "edit-note": lambda args, b: edit_note(args, notes),
        "find-tag": lambda args, b: find_note_by_tag(args, notes),
        "delete-note": lambda args, b: delete_note(args, notes),
    }

    try:
        while True:
            user_input: str = input("Enter a command: ").strip()
            command, args = parse_input(user_input)

            if not command:
                continue

            if command in ["close", "exit"]:
                print("Good bye!")
                break

            handler = commands.get(command)
            if handler:
                # Викликаємо обробник. Об'єкт 'book' передається за замовчуванням, 
                # а lambda для нотаток перенаправить виклик на об'єкт 'notes'.
                print(handler(args, book))
            else:
                print("Invalid command.")
    finally:
        # Зберігаємо обидві бази даних при виході
        save_data(book, "addressbook.pkl")
        save_data(notes, "notes.pkl")

if __name__ == "__main__":
    main()