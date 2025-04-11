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