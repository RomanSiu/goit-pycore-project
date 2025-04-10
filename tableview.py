from prettytable import PrettyTable
from colorama import Fore, Style

def output(message: str, mtype=None):
    def is_name_phone_format(line):
        return isinstance(line, str) and ':' in line

    if mtype == 'success':
        print(Fore.GREEN + message + Style.RESET_ALL)
    elif mtype == 'warning':
        print(Fore.YELLOW + message + Style.RESET_ALL)
    elif mtype == 'error':
        print(Fore.RED + message + Style.RESET_ALL)
    elif mtype == 'common':
        print(Fore.BLUE + message + Style.RESET_ALL)
    elif isinstance(message, list) and all(is_name_phone_format(m) for m in message):
        table = PrettyTable()
        table.field_names = [f"{Fore.CYAN}Name{Style.RESET_ALL}", f"{Fore.CYAN}Phone(s){Style.RESET_ALL}"]
        for m in message:
            name, phones = m.split(":", 1)
            table.add_row([
                f"{Fore.GREEN}{name.strip()}{Style.RESET_ALL}",
                f"{Fore.YELLOW}{phones.strip()}{Style.RESET_ALL}"
            ])
        print(table)
    elif isinstance(message, list):
        for m in message:
            print(Fore.BLUE + m + Style.RESET_ALL)
    else:
        print(message)

