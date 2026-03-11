import re
import phonenumbers

EMAIL_REGEX = r'^[\w\.-]+@[\w\.-]+\.\w+$'
def is_valid_email(email: str) -> bool:
    return re.match(EMAIL_REGEX, email) is not None

def normalize_phone(phone_number: str) -> str:
    parsed = phonenumbers.parse(phone_number, "UA")
    if not phonenumbers.is_valid_number(parsed):
        raise ValueError("Error: Invalid phone number")
    
    return phonenumbers.format_number(
        parsed,
        phonenumbers.PhoneNumberFormat.E164
    )
