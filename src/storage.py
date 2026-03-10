import pickle
from pathlib import Path
from typing import Any
from models import AddressBook, NoteBook

# Визначаємо шлях до папки користувача, щоб дані не губилися
SAVE_PATH = Path.home() / "assistant_bot_data"
SAVE_PATH.mkdir(exist_ok=True)

def save_data(data: Any, filename: str) -> None:
    """Універсальна функція для збереження будь-якого об'єкта (книги або нотаток)."""
    file_path = SAVE_PATH / filename
    with open(file_path, "wb") as f:
        pickle.dump(data, f)

def load_data(filename: str, default_type: Any) -> Any:
    """Універсальна функція для завантаження даних."""
    file_path = SAVE_PATH / filename
    try:
        with open(file_path, "rb") as f:
            return pickle.load(f)
    except (FileNotFoundError, EOFError):
        # Якщо файлу немає, створюємо новий об'єкт вказаного типу (AddressBook або NoteBook)
        return default_type()