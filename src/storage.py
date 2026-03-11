import pickle
from pathlib import Path
from models import AddressBook, NoteBook

# Визначаємо шлях до папки в домашній директорії користувача
SAVE_DIR = Path.home() / "assistant_bot_data"
BOOK_FILE = SAVE_DIR / "addressbook.pkl"
NOTES_FILE = SAVE_DIR / "notes.pkl"

def save_data(book: AddressBook, notes: NoteBook):
    # Створюємо папку, якщо її ще немає
    SAVE_DIR.mkdir(parents=True, exist_ok=True)
    
    # Зберігаємо книгу контактів
    with open(BOOK_FILE, "wb") as f:
        pickle.dump(book, f)
        
    # Зберігаємо блокнот
    with open(NOTES_FILE, "wb") as f:
        pickle.dump(notes, f)

def load_data():
    # Завантажуємо книгу контактів (або створюємо нову)
    if BOOK_FILE.exists():
        with open(BOOK_FILE, "rb") as f:
            book = pickle.load(f)
    else:
        book = AddressBook()

    # Завантажуємо нотатки (або створюємо нові)
    if NOTES_FILE.exists():
        with open(NOTES_FILE, "rb") as f:
            notes = pickle.load(f)
    else:
        notes = NoteBook()

    return book, notes