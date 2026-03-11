from typing import Callable, List, Tuple, Any

def input_error(func: Callable) -> Callable:
    def inner(*args: Any, **kwargs: Any) -> Any:
        try:
            return func(*args, **kwargs)
        except ValueError as e: return str(e)
        except KeyError: return "Error: Contact or note not found."
        except IndexError: return "Error: Arguments missing."
        except Exception as e: return f"Unexpected error: {e}"
    return inner

def parse_input(user_input: str) -> Tuple[str, List[str]]:
    parts = user_input.split()
    if not parts:
        return "", []
    cmd = parts[0].strip().lower()
    args = parts[1:]
    return cmd, args