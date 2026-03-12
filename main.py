from collections import UserDict
from datetime import date, datetime
from get_upcoming_bd_func import *
from input_wrapper import input_error
import pickle

# --- Класи полів ---
class Field:
    def __init__(self, value):
        self.value = value
    def __str__(self) -> str:
        return str(self.value)

class Name(Field):
    def __init__(self, name):
        super().__init__(name)

class Phone(Field):
    def __init__(self, phone):
        if len(str(phone)) != 10 or not phone.isdigit():
            raise ValueError("Phone must be 10 digits.")
        super().__init__(phone)

class Birthday(Field):
    def __init__(self, value):
        try:
            # Зберігаємо як об'єкт date для внутрішньої логіки
            self.value = datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
    
    def __str__(self):
        return self.value.strftime("%d.%m.%Y")

# --- Клас Record ---
class Record:
    def __init__(self, name: str):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone_number):
        self.phones.append(Phone(phone_number))

    def remove_phone(self, phone_number):
        self.phones = [p for p in self.phones if p.value != phone_number]

    def edit_phone(self, old_phone, new_phone):
        phone_for_editing = self.find_phone(old_phone)

        if phone_for_editing:
            self.add_phone(new_phone)
            self.remove_phone(old_phone)
            return f"Phone {old_phone} updated to {new_phone}."
    
    def find_phone(self, phone_number):
        for p in self.phones:
            if p.value == phone_number:
                return p
        return None

    def add_birthday(self, birthday_string):
        #Now store the birthday as a date object for easier handling in get_upcoming_birthdays
        self.birthday = Birthday(birthday_string)

    def __str__(self) -> str:
        bd_str = str(self.birthday) if self.birthday else "None"
        phones_str = "; ".join(p.value for p in self.phones)
        return f"Contact name: {self.name.value}, phones: {phones_str}, birthday: {bd_str}"

class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

@input_error
def add_contact(args, book: AddressBook):
    name, phone = args
    record = book.find(name)
    if record is None:
        record = Record(name)
        book.add_record(record)
    record.add_phone(phone)
    return "Contact added."

@input_error
def change_contact(args, book: AddressBook):
    name, old_phone, new_phone = args
    record = book.find(name)
    if record:
        record.edit_phone(old_phone, new_phone)
        return "Contact updated."
    return "Contact not found."

@input_error
def show_phone(args, book: AddressBook):
    name = args[0]
    record = book.find(name)
    return str(record) if record else "Contact not found."

@input_error
def add_birthday(args, book: AddressBook):
    name, bd = args
    record = book.find(name)
    if record:
        record.add_birthday(bd)
        return "Birthday added."
    return "Contact not found."

@input_error
def show_birthday(args, book: AddressBook):
    name = args[0]
    record = book.find(name)
    if record and record.birthday:
        return f"{name}'s birthday: {record.birthday}"
    return "Birthday not found."

@input_error
def birthdays(args, book: AddressBook):
    #Prepare user list of upcoming bd's
    users = []
    for record in book.data.values():
        if record.birthday:
            #Convert birthday to string for easier handling in prepare_user_list
            users.append({
                "name": record.name.value, 
                "birthday": record.birthday.value.strftime("%Y.%m.%d")
            })
    
    if not users:
        return "No upcoming birthdays found."
    
    prepared = prepare_user_list(users)
    upcoming = get_upcoming_birthdays(prepared)
    
    if not upcoming:
        return "No upcoming birthdays found."
    
    return "List of upcoming birthdays: \n" + "\n".join([f"{u['name']}: {u['congratulation_date']}" for u in upcoming])

def parse_input(user_input):
    cmd, *args = user_input.split()
    return cmd.strip().lower(), args

def save_data(book, filename="addressbook.pkl"):
    with open(filename, 'wb') as f:
        pickle.dump(book, f)

def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()

def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)

        if command in ["close", "exit","finish"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, book))
        elif command == "change":
            print(change_contact(args, book))
        elif command == "phone":
            print(show_phone(args, book))
        elif command == "all":
            for record in book.data.values():
                print(record)
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == "show-birthday":
            print(show_birthday(args, book))
        elif command == "birthdays":
            print(birthdays(args, book))
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()