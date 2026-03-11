import phonenumbers

def normalize_phone(phone_number: str) -> str:
    parsed = phonenumbers.parse(phone_number, "UA")
    if not phonenumbers.is_valid_number(parsed):
        raise ValueError("Error: Invalid phone number")
    
    return phonenumbers.format_number(
        parsed,
        phonenumbers.PhoneNumberFormat.E164
    )
