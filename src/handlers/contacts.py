from typing import List
from models import Record, AddressBook
from utils import input_error
from datetime import date, timedelta
import calendar

@input_error
def add_contact(args: List[str], book: AddressBook) -> str:
    name, phone = args
    record = book.find(name)

    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    else:
        message = "Phone added."

    record.add_phone(phone)
    return message


@input_error
def change_contact(args: List[str], book: AddressBook) -> str:
    name, old_p, new_p = args
    record = book.find(name)
    if not record:
        raise KeyError

    record.edit_phone(old_p, new_p)
    return f"{name}'s phone updated."


@input_error
def show_phones(args: List[str], book: AddressBook) -> str:
    name = args[0]
    record = book.find(name)
    if not record:
        raise KeyError

    return f"{name}: {', '.join(p.value for p in record.phones)}"


@input_error
def add_email(args: List[str], book: AddressBook) -> str:
    name, email = args
    record = book.find(name)

    if record is None:
        raise KeyError

    record.add_email(email)
    return "Email added."


@input_error
def show_email(args: List[str], book: AddressBook) -> str:
    name = args[0]
    record = book.find(name)

    if not record:
        raise KeyError

    if not record.emails:
        return "No emails found."

    return f"{name}: {', '.join(e.value for e in record.emails)}"


@input_error
def change_email(args: List[str], book: AddressBook) -> str:
    name, old_e, new_e = args
    record = book.find(name)
    if not record:
        raise KeyError

    record.edit_email(old_e, new_e)
    return f"{name}'s email updated."


@input_error
def add_birthday(args: List[str], book: AddressBook) -> str:
    name, bday = args
    record = book.find(name)
    if not record:
        raise KeyError

    record.add_birthday(bday)
    return "Birthday added."


@input_error
def show_birthday(args: List[str], book: AddressBook) -> str:
    name = args[0]
    record = book.find(name)

    if not record or not record.birthday:
        return "Error: Birthday not found."

    return f"{name}'s birthday: {record.birthday}"

def birthdays_next_week(args: List[str], book: AddressBook) -> str:
    upcoming = book.get_upcoming_birthdays()

    if not upcoming:
        return "No upcoming birthdays."

    return "\n".join(
        f"{item['name']}: {item['congratulation_date']}"
        for item in upcoming
    )

@input_error
def birthdays(args: List[str], book: AddressBook) -> str:
    lines = []

    for record in book.data.values():
        if record.birthday:
            lines.append(f"{record.name.value} - {record.birthday}")

    if not lines:
        return "No birthdays found."

    return "\n".join(lines)

def _parse_month(month_str: str) -> int:
    month_str = month_str.strip().lower()

    # Спроба повної назви місяця (March)
    for m in range(1, 13):
        full = calendar.month_name[m].lower()
        short = calendar.month_abbr[m].lower()
        if month_str == full or month_str == short:
            return m

    raise ValueError("Error: Invalid month name. Use e.g. 'March' or 'Mar'.")


def _get_week_range(year: int, month: int, week: int) -> tuple[int, int]:
    if week < 1 or week > 5:
        raise ValueError("Error: Week number must be between 1 and 5.")

    _, last_day = calendar.monthrange(year, month)
    start_day = 1 + (week - 1) * 7
    if start_day > last_day:
        raise ValueError("Error: This week does not exist in given month.")

    end_day = min(start_day + 6, last_day)
    return start_day, end_day


@input_error
def birthday_week(args: List[str], book: AddressBook) -> str:
    
    if len(args) != 2:
        return "Error: Use 'birthday-week <month> <week_number>'."

    month_str, week_str = args
    month = _parse_month(month_str)

    try:
        week = int(week_str)
    except ValueError:
        return "Error: Week number must be an integer."

    today = date.today()
    start_day, end_day = _get_week_range(today.year, month, week)

    results = []
    for record in book.data.values():
        if not record.birthday:
            continue

        bday = record.birthday.value
        try:
            birthday_this_year = date(today.year, bday.month, bday.day)
        except ValueError:
            continue

        if birthday_this_year.month != month:
            continue

        if not (start_day <= birthday_this_year.day <= end_day):
            continue

        delta_days = (birthday_this_year - today).days
        date_str = birthday_this_year.strftime("%d %B")

        if 0 <= delta_days < 30:
            results.append(
                f"{record.name.value} - {date_str} (after {delta_days} days)"
            )
        else:
            results.append(f"{record.name.value} - {date_str}")

    month_name = calendar.month_name[month]
    header = f"The following birthdays will be celebrated in the {week} week of {month_name}:"

    if not results:
        return header + "\nNo birthdays in this week."

    return header + "\n" + "\n".join(results)

@input_error
def birthdays_next_days(args: List[str], book: AddressBook) -> str:
    
    if len(args) != 1:
        return "Error: Use 'birthdays-next <days>'."

    try:
        days_limit = int(args[0])
    except ValueError:
        return "Error: <days> must be an integer."

    if days_limit < 0:
        return "Error: <days> must be non-negative."

    today = date.today()
    results = []

    for record in book.data.values():
        if not record.birthday:
            continue

        bday = record.birthday.value

        try:
            birthday_this_year = date(today.year, bday.month, bday.day)
        except ValueError:
            continue

        if birthday_this_year < today:
            birthday_this_year = date(today.year + 1, bday.month, bday.day)

        delta_days = (birthday_this_year - today).days

        if 0 <= delta_days <= days_limit:
            date_str = birthday_this_year.strftime("%d %B")
            results.append(
                f"{record.name.value} – {date_str} (after {delta_days} days)"
            )

    header = f"Birthdays in the next {days_limit} days:"

    if not results:
        return header + "\nNo birthdays found."

    return header + "\n" + "\n".join(results)

@input_error
def search_contacts(args: List[str], book: AddressBook) -> str:
    query = " ".join(args)
    results = book.search(query)

    if not results:
        return "No matching contacts found."

    return "\n".join(str(r) for r in results)
