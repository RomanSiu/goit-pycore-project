# __Bot assistant__
This is the __CLI Address Book__ - an application that will simplify your work with contact information and save your time for more interesting cases.


# __Installation instructions__ :
```sh
1. Create a new folder on the local computer, and sqitch to it
2. git clone https://github.com/RomanSiu/goit-pycore-project.git
3. pip install -r requirements.txt
4. py assistant.py
```

# __User manual__

## 1. _Commands to work with address book:_
| Instruction name     | Arguments     | Explanations                                               |
|----------------------|---------------|------------------------------------------------------------|
| "hello" or "hi"      | -             | greeting                                                   |
| "help"               | -             | calling for help                                           |
| "show-all"           | -             | display all the contents of the address book               |
| "add-contact"        | (name and phone) | add phone number to the contact                            |
| "change-contact"     | (name, old phone, new phone) | edit contact's phone                                       |
| "show-phone"         | (name)        | show contact's phones                                      |
| "delete-contact"     | (name)        | delete contact                                             |
| "add-address"        | (name and address) | add address to the contact                                 |
| "show-address"       | (name)        | show contact's address                                     |
| "change-address"     | (name and new address) | change contact's address                                   |
| "delete-address"     | (name)        | delete contact's address                                   |
| "add-email"          | (name and email) | add email to the contact                                   |
| "show-email"         | (name)        | show contact's email                                       |
| "change-email"       | (name and new email) | change contact's email                                     |
| "delete-email"       | (name)        | delete contact's email                                     |
| "add-birthday"       | (name and birthday(DD.MM.YYYY)) | add birthday to the contact                                |
| "show-birthday"      | (name)        | show contact's birthday                                    |
| "upcoming-birthdays" | (number of days(optional)) | show the contacts that have a birthday in the next XX days |
| "exit" or "close"    |               | Turn off the bot                                           |

## 2. _Commands to work with notes:_
| Instruction name | Arguments              | Explanations                          |
|------------------|------------------------|---------------------------------------|
| "add-note"       | -                      | add the note                          |
| "find-note"      | -                      | find note by title                    |
| "edit-note"      | -                      | edit the note                         |
| "delete-note"    | -                      | delete the note                       |
| "show-all-notes" | -                      | show all notes                        |
| "search-notes"    | -                      | find note by keyword in title or text |
| "import-note"         | -                      | import notes from text file           |
| "clear-all-notes"    | -                      | clear all notebook                    |
| "search-by-tag"  | -                      | search note by the tag                     |
| "sort-by-tag"    | -                      | sort notes by the tag                     |
| "remove-tag"     | -                      | remove tag from the note                     |
| "show-tags"      | -                      | show the list of tags in nootbook             |
| "clear-all-tags" | -                      | clear all the tags from all of the notes     |
| "remove-tag-from-all"  | -                | remove one tag from all notes               |

# _Good luck!_