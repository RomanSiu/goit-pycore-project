from colorama import init, Fore, Style
from prompt_toolkit import prompt
from prompt_toolkit.completion import Completer, Completion

init(autoreset=True)


commands = ["hello", "help", "exit", "close", "add-contact", "change-contact", "show-phone", "delete",
            "show-all", "add-address", "show-address", "change-address", "delete-address", "add-email",
            "change-email", "show-email", "delete-email", "add-birthday", "show-birthday", "birthdays", "add-note",
            "find-note", "edit-note", "delete-note", "show-all-notes", "search-notes", "import-note",
            "clear-all-notes", "remove-tag", "sort-by-tag", "search-by-tag", "show-tags", "clear-all-tags",
            "remove-tag-from-all", "clear-all-contacts"]


class FirstWordCompleter(Completer):
    def get_completions(self, document, complete_event):
        text_before_cursor = document.text_before_cursor.lstrip()
        words = text_before_cursor.split()

        if len(words) == 0 or (len(words) == 1 and not text_before_cursor.endswith(' ')):
            for cmd in commands:
                if cmd.startswith(words[0] if words else ''):
                    yield Completion(cmd, start_position=-len(words[0]) if words else 0)


def main_user_input():
    user_prompt = prompt("Write a command: ", completer=FirstWordCompleter())
    return user_prompt.split(" ")


def user_input(prompt_str: str) -> str:
    return input(f"{Fore.MAGENTA}{prompt_str}{Style.RESET_ALL}")


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
