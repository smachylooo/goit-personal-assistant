import re
from collections import UserDict
from typing import List, Optional


class Note:
    def __init__(self, text: str) -> None:
        if len(text) > 500:
            raise ValueError("Error: Note too long (max 500 chars).")
        self.text: str = text
        self.tags: List[str] = [t.lower() for t in re.findall(r"#(\w+)", text)]

    def add_to_end(self, additional_text: str) -> None:
        new_text = self.text + " " + additional_text
        if len(new_text) > 500:
            raise ValueError("Error: Note would exceed 500 chars.")

        self.text = new_text
        new_tags = re.findall(r"#(\w+)", additional_text)

        for tag in new_tags:
            tag_lower = tag.lower()
            if tag_lower not in self.tags:
                self.tags.append(tag_lower)


class NoteBook(UserDict):
    def add_note(self, note: Note, contact_name: Optional[str] = None) -> int:
        note_id = max(self.data.keys(), default=0) + 1
        self.data[note_id] = {
            "note": note,
            "owner": contact_name,
        }
        return note_id

    def delete_note(self, note_id: int) -> bool:
        if note_id in self.data:
            del self.data[note_id]
            return True
        return False