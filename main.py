from collections import UserDict
from datetime import date,datetime
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
            raise InsufficientCharactersError("The phone number is too short.")
        super().__init__(phone)

        if not phone.isdigit():
            raise InvalidCharacter("Invalid character entered.")

class Birthday(Field):
    def __init__(self, birthday):
        bd = None
        # Try multiple common formats; stop on first successful parse
        for fmt in ("%Y-%m-%d", "%Y.%m.%d", "%d.%m.%Y"):
            try:
                bd = datetime.strptime(birthday, fmt)
                break
            except ValueError:
                continue

        if bd is None:
            raise ValueError(f"Date {birthday} is not a supported date format.")

        # Store the birthday in normalized format (Y.m.d) for compatibility with prepare_user_list
        normalized_birthday = bd.strftime("%Y.%m.%d")
        super().__init__(normalized_birthday)
            
class Record:
    # Handles the addition, removal and editing of phone numbers
    def __init__(self, name: str):
        self.name = Name(name)
        self.phones: list[Phone] = []
        self.birthday = None

    @input_error
    def add_phone(self, value: str):
        self.phones.append(Phone(value))
        
    @input_error
    def remove_phone(self, value: str):
        for phone in self.phones:
            if phone.value == value:
                self.phones.remove(phone)
                break
            
    @input_error
    def edit_phone(self, old_phone:str,updated_phone:str):
        phone_for_editing = self.find_phone(old_phone)

        if phone_for_editing:
            self.add_phone(updated_phone)
            self.remove_phone(old_phone)
        
    @input_error
    def find_phone(self,value):
        for phone in self.phones:
            if phone.value == value:
                return phone
        return None
    
    @input_error
    def add_birthday(self,value):
        bd = Birthday(value)
        self.birthday = bd.value
        return f"{self.birthday} added."
    
    @input_error
    def show_birthday(self, value):
        if value == self.name.value:
            return f"{self.name.value}'s birthday is {self.birthday}"

    def __str__(self) -> str:
        phones_str = "; ".join(p.value for p in self.phones)
        return f"Contact name: {self.name.value}, phones: {phones_str}, birthday: {self.birthday}"
    
class AddressBook(UserDict):
    # Handles the addition of contacts, searches based on name and removal of records
    def add_record(self, record: "Record"):
        self.data[record.name.value] = record
    
    @input_error
    def find(self, name: str):
        return self.data.get(name)
    @input_error
    def delete(self, name: str):
        if name in self.data:
            del self.data[name]
    
    def display_records(self) -> str:
        return "\n".join(str(record) for record in self.data.values())
    
    def __str__(self):
        return str(self.display_records())
    
    @input_error
    def get_upcoming_birthdays(self):
        users_raw = []
        for record in self.data.values():
            if record.birthday:
                users_raw.append({"name": record.name.value, "birthday": record.birthday})
        
        if not users_raw:
            return []
        
        prepared = prepare_user_list(users_raw)
        return get_upcoming_birthdays(prepared)
    
@input_error
def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, args

def main():
    address_book = AddressBook()
    while True:
            user_input = input("Enter command: ")
            if not user_input:
                print("Please enter a command.")
                continue
            command, args = parse_input(user_input)

            if command == "hello":
                print("Hi there . How can i assist you today?")
            
            elif command == "add":
                @input_error
                def add_contact(args, book: AddressBook):
                    name, phone, *_ = args
                    record = book.find(name)
                    message = "Contact updated."
                    if record is None:
                        record = Record(name)
                        book.add_record(record)
                        message = "Contact added."
                    if phone:
                        record.add_phone(phone)
                    return message
                print(add_contact(args, address_book))
            
            elif command == "add-birthday":
                @input_error
                def add_birthday(args, book: AddressBook):
                    name, birthday, *_ = args
                    record = book.find(name)
                    if record is None:
                        raise ValueError(f"Contact {name} not found.")
                    return record.add_birthday(birthday)
                print("Added birthday:", add_birthday(args, address_book))
            
            elif command == "show-birthday":
                @input_error
                def show_birthday(args, book: AddressBook):
                    name, *_ = args
                    record = book.find(name)
                    if record is None:
                        raise ValueError(f"Contact {name} not found.")
                    return record.show_birthday(name)
                print(show_birthday(args, address_book))
            
            elif command == "birthdays":
                @input_error
                def show_upcoming_birthdays(book: AddressBook):
                    upcoming = book.get_upcoming_birthdays()
                    if not upcoming:
                        return "No upcoming birthdays found."
                    return "Upcoming birthdays:\n" + "\n".join(f"{item['name']} - {item['congratulation_date']}" for item in upcoming)
                print(show_upcoming_birthdays(address_book))

            elif command == "phone":
                @input_error
                def show_phone(args, book: AddressBook):
                    name, *_ = args
                    record = book.find(name)
                    if record is None:
                        raise ValueError(f"Contact {name} not found.")
                    return f"{name}'s phone numbers: {[str(phone) for phone in record.phones]}"
                
                print(show_phone(args, address_book))

            elif command == "all":
                @input_error
                def show_all_contacts(book: AddressBook):
                    if not book.data:
                        return "No contacts found."
                    return book.display_records()
                print(show_all_contacts(address_book))
            
            elif command == "change":
                @input_error
                def change_phone(args, book: AddressBook):
                    name, old_phone, new_phone, *_ = args
                    record = book.find(name)
                    if record is None:
                        raise ValueError(f"Contact {name} not found.")
                    record.edit_phone(old_phone, new_phone)
                    return f"{name}'s phone number updated from {old_phone} to {new_phone}."
                print(change_phone(args, address_book))
            
            elif command == "remove":
                if len(args) < 2:
                    print("Usage: remove <name> <phone>")
                    continue
                name, phone = args[0], args[1]
                record = address_book.find(name)
                if record:
                    record.remove_phone(phone)
                    print(f"{phone} removed from {name}'s contact.")
                else:
                    raise ValueError(f"Contact {name} not found.")

            elif command in ["exit", "close", "finish"]:
                print("Have a great day!")
                break
            else:
                print("Unknown command. Please try again.")
                continue

if __name__ == "__main__":
    main()