import pickle
from pathlib import Path
from assistant.models import AddressBook, NoteBook

FILE_PATH = Path(__file__).resolve().parent.parent
BOOK_FILE = FILE_PATH / "addressbook.pkl"
NOTES_FILE = FILE_PATH / "notes.pkl"

def save_data(book: AddressBook, notes: NoteBook):
    with open(BOOK_FILE, "wb") as f:
        pickle.dump(book, f)
        
    with open(NOTES_FILE, "wb") as f:
        pickle.dump(notes, f)

def load_data():
    if BOOK_FILE.exists():
        with open(BOOK_FILE, "rb") as f:
            book = pickle.load(f)
    else:
        book = AddressBook()

    if NOTES_FILE.exists():
        with open(NOTES_FILE, "rb") as f:
            notes = pickle.load(f)
    else:
        notes = NoteBook()

    return book, notes


