from colorama import init, Fore, Style

init(autoreset=True)


def user_input(prompt: str) -> str:
    return input(f"{Fore.MAGENTA}{prompt}{Style.RESET_ALL}")


def user_output(message: str, status: str = "info") -> None:
    color = {
        "info": Fore.GREEN,
        "error": Fore.RED,
        "warning": Fore.YELLOW
    }.get(status, Fore.WHITE)

    print(f"{color}{message}{Style.RESET_ALL}")

    # ui_helpers.py


def ask_and_get_value(question: str) -> str | None:
    print(f"{Fore.CYAN}{question} (Press Enter to skip):{Style.RESET_ALL}")
    answer = input("> ").strip()
    return answer if answer else None


def extend_contact_interactive(record, book):
    from assistant import add_birthday, add_email, address  # уникнути циклічного імпорту

    name = record.name.value

    bday = ask_and_get_value("Would you like to add a birthday?")
    if bday:
        add_birthday([name, bday], book)

    email = ask_and_get_value("Would you like to add an email?")
    if email:
        add_email([name, email], book)

    addr = ask_and_get_value("Would you like to add an address?")
    if addr:
        address([name, addr], book, "add_address")
