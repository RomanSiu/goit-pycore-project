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

def ask_yes_no(question: str) -> bool:
    answer = input(f"{Fore.CYAN}{question} (y/n): {Style.RESET_ALL}").strip().lower()
    return answer in ["y", "yes"]

def extend_contact_interactive(record, book):
    from assistant import add_birthday, add_email, address  # уникнути циклічного імпорту

    name = record.name.value

    if ask_yes_no("Would you like to add a birthday?"):
        bday = user_input("Enter birthday (DD.MM.YYYY): ")
        add_birthday([name, bday], book)

    if ask_yes_no("Would you like to add an email?"):
        email = user_input("Enter email: ")
        add_email([name, email], book)

    if ask_yes_no("Would you like to add an address?"):
        addr = user_input("Enter address: ")
        address([name, addr], book, "add_address")
