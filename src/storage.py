import pickle
from pathlib import Path
from models import AddressBook

DATA_FILE = Path(__file__).resolve().parent.parent / "addressbook.pkl"

def save_data(book: AddressBook, filename: Path = DATA_FILE) -> None:
    with open(filename, "wb") as f:
        pickle.dump(book, f)

def load_data(filename: Path = DATA_FILE) -> AddressBook:
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()