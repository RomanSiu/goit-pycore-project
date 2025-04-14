import pickle
import os

from colorama import Fore, Style

from utils import input_error
from models import Name, Phone, Birthday, Address, Email, NoteText, Title
from record import AddressBook, Record, NoteBook, Note
from ui_helpers import user_input, user_output, extend_contact_interactive, main_user_input
from tableview import show_table, show_help_table
from prompt_variants import (get_prompts, title_prompts, text_prompt, edit_note_prompt, edit_text_prompt,
                             title_search_prompt, delete_note_prompt)


def output(message: str, mtype: str):
    if mtype == 'success':
        user_output(Fore.GREEN + message + Style.RESET_ALL)
    elif mtype == 'warning':
        user_output(Fore.YELLOW + message + Style.RESET_ALL)
    elif mtype == 'error':
        user_output(Fore.RED + message + Style.RESET_ALL)
    elif mtype == 'common list':
        for m in message:
            user_output(Fore.BLUE + m + Style.RESET_ALL)
    elif mtype == 'common':
        user_output(Fore.BLUE + message + Style.RESET_ALL)
    else:
        user_output(message)


@input_error
def add_contact(args: list, book: AddressBook) -> tuple:
    """
    Add a contact to the book.

    Args:
        args (list): Argument list from command line.
        book (AddressBook): Address book to save records.

    Returns:
        tuple: Message.
    """
    name, phone, *_ = args
    record = book.find(name)
    if type(record) is tuple:
        record = Record(name)
        message = record.add_phone(phone)
        if message[1] in ["warrning", "error"]:
            return message
        book.add_record(record)
        extend_contact_interactive(record, book)
    else:
        message = record.add_phone(phone)
    return message


@input_error
def change_contact(args: list, book: AddressBook) -> tuple:
    """
    Change phone number to the contact.

    Args:
        args (list): Argument list from command line.
        book (AddressBook): Address book to save records.

    Returns:
        tuple: Message.
    """
    name, old_phone, new_phone, *_ = args
    record = book.find(name)
    if type(record) is not tuple:
        message = record.edit_phone(old_phone, new_phone)
        return message
    else:
        return record


@input_error
def find_contact(args: list, book: AddressBook) -> tuple:
    """
    Find a contact in the address book.

    Args:
        args (list): Argument list from command line.
        book (AddressBook): Address book to save records.

    Returns:
        tuple: tuple with list of contacts of message.
    """
    keyword, *_ = args
    records = book.find_by_keyword(keyword)
    return records


@input_error
def delete_contact(args: list, book: AddressBook) -> tuple:
    """
    Delete a contact from the book.

    Args:
        args (list): Argument list from command line.
        book (AddressBook): Address book to save records.

    Returns:
        tuple: Message.
    """
    name, *_ = args
    record = book.find(name)
    if type(record) is not tuple:
        message = book.delete(name)
        return message
    else:
        return record


@input_error
def clear_all_contacts(book: AddressBook):
    """
    Clear all contacts from the AdressBook.

    Args:
        book (AddressBook): AddressBook to clear.

    Returns:
        tuple: Success or warning message if no notes exist.
    """
    return book.clear_all_contacts()


@input_error
def show_phone(args: list, book: AddressBook) -> tuple:
    """
    Return list of phone numbers for a contact.

    Args:
        args (list): Argument list from command line.
        book (AddressBook): Address book to save records.

    Returns:
        tuple: Tuple with list of phones or with message.
    """
    name, *_ = args
    record = book.find(name)
    if type(record) is not tuple:
        phones = [i.value for i in record.phones]
        return phones, "common list"
    else:
        return record


@input_error
def show_all(book: AddressBook) -> tuple:
    """
    Return list of all contacts.

    Args:
        book (AddressBook): Address book to save records.

    Returns:
        tuple: Tuple with list of contacts or with message.
    """
    rows = []
    for rec in book.values():
        name = rec.name.value.capitalize()
        phones = "; ".join(p.value for p in rec.phones)
        birthday = rec.birthday.value.strftime('%d.%m.%Y') if rec.birthday else "-"
        email = rec.email.value if rec.email else "-"
        address = rec.address.value if rec.address else "-"
        rows.append([name, phones, birthday, email, address])
    return rows, "table"


@input_error
def add_birthday(args: list, book: AddressBook) -> tuple:
    """
    Add birthday to contact.

    Args:
        args (list): Argument list from command line.
        book (AddressBook): Address book to save records.

    Returns:
        tuple: Message.
    """
    name, birthday, *_ = args
    record = book.find(name)
    if type(record) is not tuple:
        message = record.add_birthday(birthday)
        return message
    else:
        return record


@input_error
def show_birthday(args: list, book: AddressBook) -> tuple:
    """
    Show birthday of a contact.

    Args:
        args (list): Argument list from command line.
        book (AddressBook): Address book to save records.

    Returns:
        tuple: Tuple with contacts birthday or with message.
    """
    name, *_ = args
    record = book.find(name)
    if type(record) is not tuple:
        message = record.show_birthday()
        return message if type(message) is tuple else (message, "common")
    else:
        return record


@input_error
def birthdays_table(book: AddressBook, days: int = 7) -> tuple:
    data, _ = book.get_upcoming_birthdays(days)

    if len(data) <= 1:
        return f"⚠️  No birthdays in the next {days} days.", "warning"

    rows = []
    for line in data[1:]:  # пропускаємо заголовок
        try:
            name, bday = line.split(": ")
            rows.append([name.strip(), bday.strip()])
        except ValueError:
            continue

    return rows, "birthdays"


@input_error
def add_note(book: NoteBook):
    """
    Add a new note with title and text.

    Args:
        book (NoteBook): NoteBook object to store the note.

    Returns:
        tuple: Success or warning message.
    """
    title = user_input(get_prompts(title_prompts))

    note = Note()
    message = note.add_title(title)
    if message:
        return message
    
    if book.find_note(title):
        return "⚠️  Note with this title already exists. Change the title", "warning"
    
    text = user_input(get_prompts(text_prompt))
    message = note.add_text(text)
    if message:
        return message
    
    add_tag_answer = user_input("Would you like to add a 🏷️  tag? (Y/N):\n>  ").strip().lower()
    if add_tag_answer == "y":
        tag = user_input("Enter a tag:\n>  ").strip()
        tag_msg = note.add_tag(tag)
        if tag_msg:
            output(*tag_msg)

    return book.add_note(note)


@input_error
def find_note(book: NoteBook):
    """
    Find a note by title.

    Args:
        book (NoteBook): NoteBook to search in.

    Returns:
        tuple: Note content if found, otherwise warning message.
    """
    title = user_input(get_prompts(title_search_prompt))
    note = book.find_note(title)
    if isinstance(note, Note):
        return note.format_for_display(), "common"
    return "⚠️  Note with this title doesn't exist.", "warning"


@input_error
def edit_note(book: NoteBook):
    """
    Edit an existing note.

    Args:
        book (NoteBook): NoteBook object containing notes.

    Returns:
        tuple: Success message or warning if not found or empty.
    """
    title = user_input(get_prompts(edit_note_prompt))
    note = book.find_note(title)
    if not note:
        return "⚠️  Note with this title doesn't exist.", "warning"

    new_text = user_input(get_prompts(edit_text_prompt))
    message = note.add_text(new_text)
    if message:
        return message
    
    add_tag_answer = user_input("Would you like to add a 🏷️  tag to this note? (Y/N):\n>  ").strip().lower()
    if add_tag_answer == "y":
        tag = user_input("Enter a tag:\n>  ").strip()
        tag_msg = note.add_tag(tag)
        if tag_msg:
            output(*tag_msg)
    return book.edit_note(title, new_text)


@input_error
def delete_note(book: NoteBook):
    """
    Delete a note by title.

    Args:
        book (NoteBook): NoteBook containing the note.

    Returns:
        tuple: Success message or warning if not found.
    """
    title = user_input(get_prompts(delete_note_prompt))
    if not title.strip():
        return "⚠️  Note title cannot be empty.", "warning"

    message = book.delete_note(title)
    if message is None:
        return "⚠️  Note not found.", "warning"

    return message


@input_error
def show_all_notes(book: NoteBook):
    """
    Display all notes in the NoteBook.

    Args:
        book (NoteBook): NoteBook containing the notes.

    Returns:
        tuple: List of all notes or a warning if none exist.
    """
    notes = book.show_all_notes()
    if not notes:
        return "⚠️  No notes found.", "warning"

    return notes, "common list"


@input_error
def search_notes(book: NoteBook):
    """
    Search notes by keyword in title or text.

    Args:
        book (NoteBook): NoteBook to search in.

    Returns:
        tuple: List of matched notes or warning if nothing found.
    """
    keyword = user_input("Enter keyword to search in notes 🔍 :\n>  ").strip()
    if not keyword.strip():
        return "⚠️  Please, enter a keyword.", "warning"

    result = book.search_notes(keyword)
    if not result:
        return "⚠️  No matches found.", "warning"

    results = ["The results of the search:"] + result
    output(results, "common list")

    add_as_tag = user_input(f"Would you like to add '{keyword}' as a 🏷️  tag to all matching notes? (Y/N):\n>  ").strip().lower()
    if add_as_tag == "y":
        count = 0
        for note_str in result:
            for note in book.notes:
                if str(note) == note_str:
                    message = note.add_tag(keyword)
                    if message and message[1] == "success":
                        count +=1
        return f"Keyword '{keyword}' added as tag to {count} note(s).", "success"
    return None


@input_error
def import_note(book: NoteBook):
    """
    Import a note from a text file.

    Args:
        book (NoteBook): NoteBook to add the imported note to.

    Returns:
        tuple: Success message or error if the file is invalid.
    """
    file_path = user_input("Enter file name (with .txt) to import note:\n>  ")
    if not os.path.exists(file_path):
        return "File not found.", "error"

    title, _ = os.path.splitext(os.path.basename(file_path))
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    note = Note()
    note.add_title(title)
    note.add_text(text)
    return book.add_note(note)


@input_error
def clear_all_notes(book: NoteBook):
    """
    Clear all notes from the NoteBook.

    Args:
        book (NoteBook): NoteBook to clear.

    Returns:
        tuple: Success or warning message if no notes exist.
    """
    if not book.notes:
        return "⚠️  There are no notes to delete.", "warning"

    return book.clear_all_notes()

  
@input_error
def search_notes_by_tag(book: NoteBook):
    """
    Search notes by tag entered by the user.

    Args:
        book (NoteBook): The notebook to search in.

    Returns:
        tuple: List of matching notes or a warning message.
    """
    tag = user_input("Enter the 🏷️  tag to search:\n>  ")
    if not tag.strip():
        return "⚠️  Tag cannot be empty.", "warning"
    result = book.search_by_tag(tag)
    if not result:
        return f"⚠️  No notes found with this tag '{tag}'.", "warning"
    return [f"Notes with tag '{tag}':"] + result, "common list"


@input_error
def sort_notes_by_tag(book: NoteBook):
    """
    Sort notes by the number of tags and display them.

    Args:
        book (NoteBook): The notebook to sort.

    Returns:
        tuple: Sorted notes list or a warning.
    """
    sorted_notes = book.sort_by_tag()
    if not sorted_notes:
        return "⚠️  No notes to sort.", "warning"
    return sorted_notes, "common list"


@input_error
def remove_tag(book: NoteBook):
    """
    Remove a tag from a specific note.

    Args:
        book (NoteBook): The notebook containing the note.

    Returns:
        tuple: Success or warning message.
    """
    title = user_input(get_prompts(title_search_prompt))
    note = book.find_note(title)
    if not note:
        return "⚠️  Note not found.", "warning"
    
    tag = user_input("Enter the 🏷️  tag to remove:\n>  ").strip()
    return note.remove_tag(tag)


@input_error
def show_all_tags(book: NoteBook):
    """
    Display a list of all unique tags across notes.

    Args:
        book (NoteBook): The notebook containing the notes.

    Returns:
        tuple: List of tags or a warning if none exist.
    """
    tags = book.list_all_tags()
    if not tags:
        return "⚠️  There are no tags in your notes.", "warning"
    return ["📌 Tags in your notes:"] + tags, "common list"


@input_error
def clear_all_tags(book:NoteBook):
    """
    Clear all tags from all notes in the notebook.

    Args:
        book (NoteBook): The notebook to clear tags from.

    Returns:
        tuple: Success message.
    """
    return book.clear_all_tags()


@input_error
def remove_tag_from_all(book: NoteBook):
    """
    Remove a specific tag from all notes in the notebook.

    Args:
        book (NoteBook): The notebook to update.

    Returns:
        tuple: Success or warning message.
    """
    tag = user_input("Enter the 🏷️  tag to remove from all notes:\n>  ").strip()
    if not tag:
        return "⚠️  Tag cannot be empty.", "warning"
    return book.remove_tag_from_all(tag)


@input_error
def address(args: list, book: AddressBook, func: str) -> tuple:
    """
    Call func to interact with an address of a contact.

    Args:
        args (list): Argument list from command line.
        book (AddressBook): Address book to save records.
        func (str): Function to call to interact with an address.

    Returns:
        tuple: Tuple with address or with message.
    """
    record = book.find(args[0])
    if type(record) is not tuple:
        address_func = getattr(record, func)
        return address_func(*args[1:])
    else:
        return record
    

@input_error
def add_email(args, book):
    name, email = args
    record = book.find(name)
    if type(record) is not tuple:
        return record.add_email(email)
    return "⚠️  Contact not found.", "warning"


@input_error
def edit_email(args, book):
    name, new_email = args
    record = book.find(name)
    if record:
        return record.edit_email(new_email)
    return "⚠️  Contact not found.", "warning"


@input_error
def show_email(args, book):
    name = args[0]
    record = book.find(name)
    if record:
        return record.show_email()
    return "⚠️  Contact not found.", "warning"


@input_error
def delete_email(args, book):
    name = args[0]
    record = book.find(name)
    if record:
        return record.delete_email()
    return "⚠️  Contact not found.", "warning"


# Серіалізація даних в окремий файл з обох книг
def save_data(books, filename="data/addressbook_and_notebook.pkl"):
    # створює директорію, якщо вона не існує
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "wb") as f:
        pickle.dump(books, f)


# Завантаження даних з файлу з кортежами обох книг та повернення у разі провало також обох з них
def load_data(filename="data/addressbook_and_notebook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook(), NoteBook()


def main():
    addressbook, notebook = load_data()
    user_output("Welcome to the assistant bot!")
    while True:
        command = main_user_input()
        if not command:
            continue
        command[0] = command[0].lower()

        match command[0]:
            case 'exit' | 'close':
                user_output("Good bye!")
                break
            case 'hello':
                user_output("How can I help you?")
            case 'add-contact':
                output(*add_contact(command[1:], addressbook))
            case 'change-contact':
                output(*change_contact(command[1:], addressbook))
            case 'find-contact':
                show_table(*find_contact(command[1:], addressbook))
            case 'show-phone':
                output(*show_phone(command[1:], addressbook))
            case 'delete-contact':
                output(*delete_contact(command[1:], addressbook))
            case 'add-address':
                output(*address(command[1:], addressbook, "add_address"))
            case 'show-address':
                output(*address(command[1:], addressbook, "show_address"))
            case 'change-address':
                output(*address(command[1:], addressbook, "edit_address"))
            case 'delete-address':
                output(*address(command[1:], addressbook, "delete_address"))
            case 'add-email':
                output(*add_email(command[1:], addressbook))
            case 'change-email':
                output(*edit_email(command[1:], addressbook))
            case 'show-email':
                output(*show_email(command[1:], addressbook))
            case 'delete-email':
                output(*delete_email(command[1:], addressbook))
            case 'add-birthday':
                output(*add_birthday(command[1:], addressbook))
            case 'show-birthday':
                output(*show_birthday(command[1:], addressbook))
            case 'birthdays':
                try:
                    days = int(command[1])
                except IndexError:
                    days = 7
                show_table(*birthdays_table(addressbook, days))
            case 'clear-all-contacts':
                output(*clear_all_contacts(addressbook))
            case 'add-note':
                output(*add_note(notebook))
            case 'find-note':
                output(*find_note(notebook))
            case 'edit-note':
                output(*edit_note(notebook))
            case 'delete-note':
                output(*delete_note(notebook))
            case 'show-all-notes':
                output(*show_all_notes(notebook))
            case 'search-notes':
                output(*search_notes(notebook))
            case 'import-note':
                output(*import_note(notebook))
            case 'clear-all-notes':
                output(*clear_all_notes(notebook))
            case 'search-by-tag':
                output(*search_notes_by_tag(notebook))
            case 'sort-by-tag':
                output(*sort_notes_by_tag(notebook))
            case 'remove-tag':
                output(*remove_tag(notebook))
            case 'show-tags':
                output(*show_all_tags(notebook))
            case 'clear-all-tags':
                output(*clear_all_tags(notebook))
            case 'remove-tag-from-all':
                output(*remove_tag_from_all(notebook))
            case 'help':
                show_help_table()
            case 'show-all':
                show_table(*show_all(addressbook))
            case _:
                output("Invalid command.", "error")
    save_data((addressbook, notebook))


if __name__ == '__main__':
    main()
