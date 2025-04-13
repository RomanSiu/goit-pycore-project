from prettytable import PrettyTable
from colorama import Fore, Style


def show_table(message, mtype=None):
    if mtype == 'success':
        print(Fore.GREEN + message + Style.RESET_ALL)
    elif mtype == 'warning':
        print(Fore.YELLOW + message + Style.RESET_ALL)
    elif mtype == 'error':
        print(Fore.RED + message + Style.RESET_ALL)
    elif mtype == 'common':
        print(Fore.BLUE + message + Style.RESET_ALL)
    elif mtype == 'table' and isinstance(message, list):
        table = PrettyTable()
        table.field_names = [
            f"{Fore.CYAN}👤 Name{Style.RESET_ALL}", 
            f"{Fore.CYAN}📞 Phone(s){Style.RESET_ALL}",
            f"{Fore.CYAN}🎂 Birthday{Style.RESET_ALL}",
            f"{Fore.CYAN}📧 Email{Style.RESET_ALL}",
            f"{Fore.CYAN}🏠 Address{Style.RESET_ALL}"
        ]

        for row in message:
            if isinstance(row, list) and len(row) == 5:
                name, phones, birthday, email, address = row
            else:
                name, phones, birthday, email, address = "-", "-", "-", "-", "-"
            table.add_row([
                f"{Fore.GREEN}{name}{Style.RESET_ALL}",
                f"{Fore.YELLOW}{phones}{Style.RESET_ALL}",
                f"{Fore.MAGENTA}{birthday}{Style.RESET_ALL}",
                f"{Fore.BLUE}{email}{Style.RESET_ALL}",
                f"{Fore.WHITE}{address}{Style.RESET_ALL}"
            ])
        print(table)
    elif mtype == 'birthdays' and isinstance(message, list):
        table = PrettyTable()
        table.field_names = [
            f"{Fore.CYAN}👤 Name{Style.RESET_ALL}",
            f"{Fore.CYAN}🎉 Congratulation Date{Style.RESET_ALL}"
        ]
        for row in message:
            if isinstance(row, list) and len(row) == 2:
                name, bday = row
            else:
                name, bday = "-", "-"
            table.add_row([
                f"{Fore.GREEN}{name}{Style.RESET_ALL}",
                f"{Fore.MAGENTA}{bday}{Style.RESET_ALL}"
            ])
        print(table)


def show_help_table():
    help_sections = {
        "🤖 GENERAL": [
            ("hello", "Greet the assistant"),
            ("help", "Show all available commands"),
            ("exit / close", "Exit the assistant")
        ],
        "📞 CONTACTS": [
            ("add-contact", "Add a new contact"),
            ("change-contact", "Change a contact's phone number"),
            ("show-phone", "Show phone numbers of a contact"),
            ("delete", "Delete a contact"),
            ("show-all", "Display all contacts"),
            ("clear-all-contacts", "Clear all contacts")
        ],
        "🏠 ADDRESS": [
            ("add-address", "Add an address to a contact"),
            ("show-address", "Show a contact's address"),
            ("change-address", "Edit a contact's address"),
            ("delete-address", "Delete a contact's address")
        ],
        "✉️   EMAIL": [
            ("add-email", "Add an email to a contact"),
            ("change-email", "Change a contact's email"),
            ("show-email", "Show a contact's email"),
            ("delete-email", "Delete a contact's email")
        ],
        "🎂 BIRTHDAY": [
            ("add-birthday", "Add a birthday to a contact"),
            ("show-birthday", "Show a contact's birthday"),
            ("birthdays", "Show upcoming birthdays")
        ],
        "📝 NOTES": [
            ("add-note", "Add a new note"),
            ("find-note", "Find a note by title"),
            ("edit-note", "Edit the text of a note"),
            ("delete-note", "Delete a note"),
            ("show-all-notes", "Show all notes"),
            ("search-notes", "Search notes by keyword"),
            ("import-note", "Import a note from file"),
            ("clear-all-notes", "Delete all notes"),
            ("remove-tag", "Remove tag from note"),
            ("sort-by-tag", "Sort notes by tags"),
            ("search-by-tag", "Search notes by tag"),
            ("show-tags", "Display all unique tags used in notes"),
            ("clear-all-tags", "Remove all tags from every note"),
            ("remove-tag-from-all", "Remove a specific tag from all notes")
        ]
    }

    for section, commands in help_sections.items():
        print(f"\n{Fore.CYAN}{section}{Style.RESET_ALL}")
        table = PrettyTable()
        table.field_names = [
            f"{Fore.YELLOW}Command{Style.RESET_ALL}",
            f"{Fore.GREEN}Description{Style.RESET_ALL}"
        ]
        for cmd, desc in commands:
            table.add_row([
                f"{Fore.WHITE}{cmd}{Style.RESET_ALL}",
                f"{Fore.MAGENTA}{desc}{Style.RESET_ALL}"
            ])
        print(table)
