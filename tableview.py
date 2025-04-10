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
            f"{Fore.CYAN}🎂 Birthday{Style.RESET_ALL}"
        ]

        for row in message:
            if isinstance(row, list) and len(row) == 3:
                name, phones, birthday = row
            else:
                name, phones, birthday = "-", "-", "-"
            table.add_row([
                f"{Fore.GREEN}{name}{Style.RESET_ALL}",
                f"{Fore.YELLOW}{phones}{Style.RESET_ALL}",
                f"{Fore.MAGENTA}{birthday}{Style.RESET_ALL}"
            ])
    print(table)