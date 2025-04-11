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
| Instruction name  | Arguments     | Explanations                                               |
|-------------------|---------------|------------------------------------------------------------|
| "hello" or "hi"   | -             | greeting                                                   |
| "help" or "?"     | -             | calling for help                                           |
| "all"             | -             | display all the contents of the address book               |
| "add"             | (name and phone) | add phone number to the contact                            |
| "change"          | (name, old phone, new phone) | edit contact's phone                                       |
| "phone"           | (name)        | show contact's phones                                      |
| "delete"          | (name)        | delete contact                                             |
| "add-address"     | (name and address) | add address to the contact                                 |
| "show-address"    | (name)        | show contact's address                                     |
| "change-address"  | (name and new address) | change contact's address                                   |
| "delete-address"  | (name)        | delete contact's address                                   |
| "add-email"       | (name and email) | add email to the contact                                   |
| "show-email"      | (name)        | show contact's email                                       |
| "change-email"    | (name and new email) | change contact's email                                     |
| "delete-email"    | (name)        | delete contact's email                                     |
| "add-birthday"    | (name and birthday(DD.MM.YYYY)) | add birthday to the contact                                |
| "show-birthday"   | (name)        | show contact's birthday                                    |
| "birthdays"       | (number of days(optional)) | show the contacts that have a birthday in the next XX days |
| "exit" or "close" |               | Turn off the bot                                           |

## 2. _Commands to work with notes:_
| Instruction name | Arguments              | Explanations                          |
|------------------|------------------------|---------------------------------------|
| "add-note"       | -                      | add the note                          |
| "find-note"      | -                      | find note by title                    |
| "edit-note"      | -                      | edit the note                         |
| "delete-note"    | -                      | delete the note                       |
| "show-all-notes" | -                      | show all notes                        |
| "search-note"    | -                      | find note by keyword in title or text |
| "import-note"         | -                      | import notes from text file           |
| "clear-all-notes"    | -                      | clear all notebook                    |

# _Good luck!_