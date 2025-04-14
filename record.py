from datetime import datetime as dtdt
from datetime import timedelta
from collections import UserDict

from utils import input_error
from models import Name, Phone, Birthday, Address, Email, NoteText, Title


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None
        self.address = None
        self.email = None

    def __str__(self):
        birthday_str = ""
        address_str = ""
        email_str = ""
        if self.birthday:
            birthday_str = f", birthday: {self.birthday.value.strftime('%d.%m.%Y')}"
        if self.address:
            address_str = f", address: {self.address}"
        if self.email:
            email_str = f", email: {self.email}"
        return (f"Contact name: {self.name.value}, phones: {'; '.join(str(p.value) for p in self.phones)}"
                + birthday_str + email_str + address_str)

    @input_error
    def add_phone(self, phone: str) -> tuple:
        """
        Add a phone to the record

        Args:
            phone (str): phone number

        Returns:
            tuple: message
        """
        phone = Phone(phone)
        if phone.value is None:
            return "Please enter a valid phone number.", "warning"
        elif phone.value not in [i.value for i in self.phones]:
            self.phones.append(phone)
            return "Phone added.", "success"
        else:
            return "⚠️  Phone already exists.", "warning"

    @input_error
    def remove_phone(self, phone_rm: str) -> tuple:
        """
        Remove a phone from the record

        Args:
            phone_rm (str): phone number to remove

        Returns:
            tuple: message
        """
        for phone in self.phones:
            if phone_rm == phone.value:
                self.phones.remove(phone)
                return f"Phone {phone_rm} removed.", "success"

        return "⚠️  No such phone exists.", "warning"

    @input_error
    def edit_phone(self, old_phone: str, new_phone: str) -> tuple:
        """
        Edit a phone in the record

        Args:
            old_phone (str): phone number to edit
            new_phone (str): new phone number

        Returns:
            tuple: message
        """
        new_phone = Phone(new_phone)

        if new_phone.value is None:
            return "⚠️  Please enter a valid phone number.", "warning"

        for phone in self.phones:
            if old_phone == phone.value and new_phone.value:
                phone.value = new_phone.value
                return f"Phone {old_phone} changed to {new_phone}.", "success"

        return "⚠️  No such phone exists.", "warning"

    @input_error
    def find_phone(self, phone_to_find: str) -> tuple:
        """
        Find a phone in the record

        Args:
             phone_to_find (str): phone number to find

        Returns:
            tuple: message
        """
        for phone in self.phones:
            if phone_to_find == phone.value:
                return phone

    @input_error
    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)
        if self.birthday.value is None:
            self.birthday = None
            return "⚠️  Invalid date format. Try DD.MM.YYYY.", "warning"
        return "Birthday added.", "success"

    @input_error
    def show_birthday(self):
        if self.birthday is None:
            return "⚠️  No birthday found.", "warning"
        return f"{self.name.value.capitalize()}'s birthday: {dtdt.strftime(self.birthday.value, '%d.%m.%Y')}"

    @input_error
    def add_address(self, *args) -> tuple:
        address = " ".join(args)
        address = Address(address)
        if address.value is None:
            return "Please enter a valid address.", "warning"
        elif self.address is not None:
            return "⚠️  Address already exists.", "warning"
        else:
            self.address = address
            return "Address added.", "success"

    @input_error
    def show_address(self, *args) -> tuple:
        if self.address is None:
            return "⚠️  No address found.", "warning"
        return self.address.value, "common"

    @input_error
    def edit_address(self, address: str, *args) -> tuple:
        address = Address(address)
        if self.address is None:
            return "⚠️  No address found.", "warning"
        elif address.value is None:
            return "⚠️  Please enter a valid address.", "warning"
        else:
            self.address = address
            return "Address changed.", "success"

    @input_error
    def delete_address(self, *args) -> tuple:
        self.address = None
        return "Address deleted.", "success"

    @input_error
    def add_email(self, email):
        if hasattr(self, "email") and self.email is not None:
            return "⚠️  This contact already has an email.", "warning"

        email_obj = Email(email)
        if email_obj.value is None:
            return "⚠️  Please enter a valid email address.", "warning"

        self.email = email_obj
        return "Email added.", "success"

    @input_error
    def edit_email(self, new_email):
        email = Email(new_email)
        if email.value is None:
            return "⚠️  Please enter a valid email address (only Latin letters and must include @).", "warning"
        if self.email is None:
            return "⚠️  No email found.", "warning"
        self.email = email
        return "Email changed.", "success"

    @input_error
    def delete_email(self):
        if self.email is None or self.email.value is None:
            return "⚠️  No email found to delete.", "warning"
        self.email = None
        return "Email deleted.", "success"

    @input_error
    def show_email(self):
        if self.email is None or self.email.value is None:
            return "⚠️  No email found.", "warning"
        return f"{self.name.value.capitalize()}'s email: {self.email.value}", "common"

    @input_error
    def get_contact_keywords(self):
        keywords = [self.name.value]
        [keywords.append(p.value) for p in self.phones]
        if self.birthday:
            keywords.append(self.birthday.value.strftime("%d.%m.%Y"))
        if self.email:
            keywords.append(self.email.value)
        return keywords


class Note:
    def __init__(self):
        self.title = None
        self.text = None
        self.tags = []
        self.created_date = dtdt.now().replace(microsecond=0)
        self.updated_date = dtdt.now().replace(microsecond=0)
    
    def format_for_display(self):
        tag_line = f"Tags: {', '.join(self.tags)}\n" if self.tags else "Tags: "
        return (
            f"{'='*35}\n"
            f"📌 Title: {self.title.value}\n"
            f"📝 Content: {self.text.value}\n"
            f"🏷️  {tag_line}\n"
            f"🕒 Created: {self.created_date}\n"
            f"🕒 Updated: {self.updated_date}\n"
            f"{'='*35}"
        )
    
    def add_title(self, title_str):
        title = Title(title_str)
        if title.value is None:
            return "⚠️  Note cannot be empty.", "warning"
        self.title = title
        return None
        
    def add_text(self, text_str):
        text = NoteText(text_str)
        if text.value is None:
            return "⚠️  Text cannot be empty.", "warning"
        self.text = text
        return None

    def add_tag(self, tag: str) -> tuple:
        """
        Add a tag to the note.

        Args:
            tag (str): The tag to be added.

        Returns:
            tuple: Message indicating success or warning.
        """
        if not tag.strip():
            return "⚠️  Tag cannot be empty.", "warning"
        elif tag in self.tags:
            return "⚠️  Tag already exists or invalid.", "warning"
        self.tags.append(tag)
        return f"Tag '{tag}' added to the note.", "success"

    def remove_tag(self, tag: str) -> tuple:
        """
        Remove a tag from the note.

        Args:
            tag (str): The tag to be removed.

        Returns:
            tuple: Success message or warning if tag not found.
        """
        if tag in self.tags:
            self.tags.remove(tag)
            return f"Tag '{tag}' removed from the note.", "success"
        return f"⚠️  Tag '{tag}' not found in this note.", "warning"


class NoteBook:
    def __init__(self):
        super().__init__()
        self.notes = []
    
    @input_error
    def add_note(self, note: Note) -> tuple:
        """
        Add a new note to the notebook.

        Args:
            note (Note): Note object containing title and content.

        Returns:
            tuple: Message and message type indicating success or validation warning.
        """
        if self.find_note(note.title.value):
            return "⚠️  Note with this title already exists. Change the title", "warning"
        elif note.title.value is None:
            return "⚠️  Title must be 15 characters or less.", "warning"
        self.notes.append(note)
        return "Note added.", "success"
    
    @input_error
    def find_note(self, title: str) -> Note | None:
        """
        Search for a note by its title.

        Args:
            title (str): Title of the note to search for.

        Returns:
            Note | None: Note object if found, otherwise None.
        """
        for note in self.notes:
            if note.title.value.lower() == title.lower():
                return note
    
    @input_error
    def delete_note(self, title: str) -> tuple | None:
        """
        Delete a note by its title.

        Args:
            title (str): Title of the note to delete.

        Returns:
            tuple | None: Message indicating success or None if not found.
        """
        for note in self.notes:
            if note.title.value.lower() == title.lower():
                self.notes.remove(note)
                return "Note deleted.", "success"
            
    @input_error
    def edit_note(self, title: str, new_text: str) -> tuple:
        """
        Edit the content of a note by its title.

        Args:
            title (str): Title of the note to edit.
            new_text (str): New text to update the note content.

        Returns:
            tuple: Message indicating success or warning if validation fails.
        """
        for note in self.notes:
            if note.title.value.lower() == title.lower():
                txt = NoteText(new_text)
                if txt.value is None:
                    return "⚠️  Note cannot be empty.", "warning"
                else:
                    note.text = txt
                    note.updated_date = dtdt.now().replace(microsecond=0)
                    return "Note edited.", "success"
    
    @input_error
    def search_notes(self, keyword: str) -> list:
        """
        Search for notes that contain the keyword in their title or content.

        Args:
            keyword (str): Keyword to search for in notes.

        Returns:
            list: List of string representations of matching notes.
        """
        notes = []
        for note in self.notes:
            if keyword.lower() in note.title.value.lower() or keyword.lower() in note.text.value.lower():
                notes.append(note)
        return [note.format_for_display() for note in notes]

    @input_error
    def show_all_notes(self) -> list:
        """
        Get a list of all notes in the notebook.

        Returns:
            list: List of string representations of all notes.
        """
        note_list = [note.format_for_display() for note in self.notes]
        return note_list
    
    @input_error
    def clear_all_notes(self) -> tuple:
        """
        Delete all notes from the notebook.

        Returns:
            tuple: Message confirming that all notes were deleted.
        """
        self.notes.clear()
        return "All the notes have been deleted.", "success"
    
    @input_error
    def search_by_tag(self, tag: str) -> list:
        """
        Search for notes by tag.

        Args:
            tag (str): Tag to search for in notes.

        Returns:
            list: List of string representations of notes containing the tag.
        """
        results = [note for note in self.notes if tag in note.tags]
        return [note.format_for_display() for note in results]
    
    @input_error
    def sort_by_tag(self) -> list:
        """
        Sort notes by the number of tags (ascending) and alphabetically by title.

        Returns:
            list: List of string representations of sorted notes.
        """
        tagged_notes = [note for note in self.notes if note.tags]
        untagged_notes = [note for note in self.notes if not note.tags]

        tagged_sorted = sorted(tagged_notes, key=lambda n: (-len(n.tags), n.title.value.lower()))
        untagged_sorted = sorted(untagged_notes, key=lambda n: n.title.value.lower())

        sorted_notes = tagged_sorted + untagged_sorted
        return [note.format_for_display() for note in sorted_notes]
    
    @input_error
    def list_all_tags(self) -> list:
        """
        Return a list of all unique tags in the notebook.

        Returns:
            list: List of tag strings.
        """
        tags = set()
        for note in self.notes:
            tags.update(note.tags)
        return sorted(tags)
    
    @input_error
    def clear_all_tags(self) -> tuple:
        """
        Remove all tags from every note in the notebook.

        Returns:
            tuple: Message indicating success.
        """
        for note in self.notes:
            note.tags.clear()
        return "All tags have been removed from all notes.", "success"
    
    @input_error
    def remove_tag_from_all(self, tag: str) -> tuple:
        """
        Remove a specific tag from all notes where it appears.

        Args:
            tag (str): The tag to remove.

        Returns:
            tuple: Message indicating how many notes were affected.
        """
        count = 0
        for note in self.notes:
            if tag in note.tags:
                note.tags.remove(tag)
                count += 1
        if count == 0:
            return f"⚠️  Tag 'tag' not found in any note.", "warning"
        return f"Tag '{tag}' remove from {count} note(s).", "success"


class AddressBook(UserDict):
    @input_error
    def add_record(self, record):
        self.data[record.name.value] = record
        return "Record added.", "success"

    @input_error
    def find(self, name):
        return self.data[name.lower()]

    @input_error
    def find_by_keyword(self, keyword):
        contacts = []
        for contact in self.data.values():
            contact_keywords = contact.get_contact_keywords()
            if keyword.lower() in contact_keywords:
                name = contact.name.value.capitalize()
                phones = "; ".join(p.value for p in contact.phones)
                birthday = contact.birthday.value.strftime('%d.%m.%Y') if contact.birthday else "-"
                email = contact.email.value if contact.email else "-"
                address = contact.address.value if contact.address else "-"
                contacts.append([name, phones, birthday, email, address])

        if contacts:
            return contacts, "table"
        return "No contact found.", "warning"

    @input_error
    def delete(self, name):
        self.data.pop(name.lower())
        return "Record deleted.", "success"

    @input_error
    def get_upcoming_birthdays(self, days: int = 7) -> (list, str):
        today = dtdt.now().date()
        d7 = today + timedelta(days=days)
        lst = [f"Next {days} days You need to congratulate:"]
        for user in self.data.values():
            if user.birthday is None:
                continue
            bday = user.birthday.value.replace(year=today.year)
            if bday <= today:
                bday = bday.replace(year=today.year + 1)
            if today <= bday <= d7:
                if bday.weekday() == 5:
                    bday = bday + timedelta(days=2)
                if bday.weekday() == 6:
                    bday = bday + timedelta(days=1)
                user_bday = f"{user.name.value.capitalize()}: {dtdt.strftime(bday, '%d.%m.%Y')}"
                lst.append(user_bday)
        return lst, "common list"

    @input_error
    def clear_all_contacts(self) -> tuple:
        """
        Delete all contacts from the addressbook.

        Returns:
            tuple: Message confirming that all notes were deleted.
        """
        self.data.clear()
        return "All the contacts have been deleted.", "success"
