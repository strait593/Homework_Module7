from collections import UserDict
from datetime import date, datetime
from get_upcoming_bd_func import *
from input_wrapper import input_error

class InsufficientCharactersError(Exception):
    pass
class InvalidCharacter(Exception):
    pass

class Field:
    def __init__(self, value):
        self.value = value

    # handles the conversion to str datatype
    def __str__(self) -> str:
        return str(self.value)

class Name(Field):
    def __init__(self, name):
        super().__init__(name)

class Phone(Field):
    def __init__(self, phone):
        if len(str(phone)) != 10:
            raise InsufficientCharactersError("The phone number should be exactly 10 digits long.")
        super().__init__(phone)
        if not phone.isdigit():
                raise ValueError("Phone number cannnot contain letters or special symbols")

class Birthday(Field):
    def __init__(self, value):
        try:
            datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid date format. Supported date format: DD.MM.YYYY")
        super().__init__(value)

class Record:
    # Handles the addition, removal and editing of phone numbers
    def __init__(self, name: str):
        self.name = Name(name)
        self.phones: list[Phone] = []
        self.birthday = None

    def add_phone(self, value: str):
        self.phones.append(Phone(value))

    def remove_phone(self, value: str):
        for phone in self.phones:
            if phone.value == value:
                self.phones.remove(phone)
                break
    
    def edit_phone(self, old_phone:str,updated_phone:str):
        phone_for_editing = self.find_phone(old_phone)

        if phone_for_editing:
            self.add_phone(updated_phone)
            self.remove_phone(old_phone)
        else:
            raise ValueError(f"Phone number {old_phone} does not exist.")
    
    def find_phone(self,value):
        for phone in self.phones:
            if phone.value == value:
                return phone
            
        return None
    
    def add_birthday(self, birthday_str):
        self.birthday = Birthday(birthday_str)

        return f"{self.name}'s birthday updated to {self.birthday}"

    def __str__(self) -> str:
        phones_str = "; ".join(p.value for p in self.phones)
        return f"Contact name: {self.name.value}, phones: {phones_str}"
    
class AddressBook(UserDict):
    # Handles the addition of contacts, searches based on name and removal of records
    def add_record(self, record: "Record"):
        self.data[record.name.value] = record

    def find(self, name: str):
        return self.data.get(name)

    def delete(self, name: str):
        if name in self.data:
            del self.data[name]

    def display_records(self) -> str:
        return "\n".join(str(record) for record in self.data.values())
    
    def __str__(self):
        return str(self.display_records())

    def get_upcoming_birthdays(self, days=7) -> list:
        users = []
        for record in self.data.values():
            if record.birthday:
                try:
                    birthday_date = datetime.strptime(record.birthday.value, "%d.%m.%Y").date()
                    users.append({"name": record.name.value, "birthday": birthday_date.strftime("%Y.%m.%d")})
                except ValueError:
                    continue
        return users

@input_error
def add_contact(args, book: AddressBook):
    name, phone = args
    record = book.find(name)
    if record is None:
        record = Record(name)
        book.add_record(record)
        print(f"Contact {name} created.")

    record.add_phone(phone)

@input_error
def change_contact(args, book:AddressBook):
    name, old_phone, new_phone = args
    record = book.find(name)
    record.edit_phone(old_phone, new_phone)
    return f"Phone number {old_phone} for contact {name} has been updated to {new_phone}."

@input_error
def show_phone(args, book: AddressBook):
    name = args[0]
    record = book.find(name)
    return f"{name}'s phone(s):{';'.join(p.value for p in record.phones)}"

@input_error
def add_birthday(args, book:AddressBook):
    name,birthday = args
    record = book.find(name)

    return record.add_birthday(birthday)

@input_error
def show_birthday(args, book:AddressBook):
    name = args[0]
    record = book.find(name)
    if record.birthday:
        return f"{name}'s birthday is on {record.birthday.value}"

@input_error
def show_upcoming_birthdays(book:AddressBook, days=7):
    upcoming_birthdays = book.get_upcoming_birthdays(days)

    return "Upcoming birthdays:\n" + "\n".join(f"{user['name']} - {user['birthday']}" for user in upcoming_birthdays)

def parse_input(user_input):
    cmd, *args = user_input.split()
    return cmd.strip().lower(), args

def main():
    book = AddressBook()
    while True:
            user_input = input("Enter the command: ")
            command, args = parse_input(user_input)

            if not user_input:
                continue
            
            elif command in ['end', 'exit', 'close']:
                print("Goodbye")
                break
            
            elif command == 'add':
                print(add_contact(args, book))
            elif command == "change":
                print(change_contact(args, book))
            elif command == "phone":
                print(show_phone(args, book))
            elif command == "all":
                print(book)
            elif command == "add-birthday":
                print(add_birthday(args, book))
            elif command == "show-birthday":
                print(show_birthday(args, book))
            elif command == "birthdays":
                print(show_upcoming_birthdays(book))
            else:
                print("Unknown command. Please try again.")

if __name__ == "__main__":
    main()