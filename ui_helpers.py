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