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

        # Store the original value via Field initializer
        super().__init__(birthday)
            
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
        else:
            raise ValueError(f"Phone number {old_phone} does not exist.")
        
    @input_error
    def find_phone(self,value):
        for phone in self.phones:
            if phone.value == value:
                return phone
        return None
    
    @input_error
    def add_birthday(self,value):
        self.birthday = value

        return f"{self.birthday} added."
    
    @input_error
    def show_birthday(self, value):
        if value == self.name.value:
            return f"{self.name.value}'s birthday is {self.birthday}"
        else:
            raise IndexError(f"{value} birthday was not found.")
        
    @input_error
    def birthdays(self):
        #Return upcoming birthday(s) for this record within 7 days since present date.
        if not getattr(self, "birthday", None):
            return []

        users_raw = [{"name": self.name.value, "birthday": self.birthday}]
        prepared = prepare_user_list(users_raw)

        return get_upcoming_birthdays(prepared)

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

        if not getattr(self, "birthday", None):
            return []

        users_raw = [{"name": self.name.value, "birthday": self.birthday}]
        prepared = prepare_user_list(users_raw)

        return get_upcoming_birthdays(prepared)
    
@input_error
def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, args

def main():
    address_book = AddressBook()
    record = Record()
    while True:
            user_input = input("Enter command: ")
            if not user_input:
                print("Please enter a command.")
                continue
            command, args = parse_input(user_input)

            if command == "hello":
                print("Hi there . How can i assist you today?")
            
            elif command == "add":
                if len(args) < 2:
                    print("Usage: add <name> <phone>")
                    continue
                name, phone = args[0], args[1]
                record = Record(name)
                try:
                    record.add_phone(phone)
                    address_book.add_record(record)
                    print(f"Added contact: {record}")
                except (InsufficientCharactersError, InvalidCharacter) as e:
                    print(e)
            
            
            elif command == "add_birthday":
                if len(args) < 2:
                    print("Usage: add_birthday <name> <birthday>")
                    continue
                name, birthday = args[0], args[1]
                record = address_book.find(name)
                if record:
                    try:
                        print(record.add_birthday(birthday))
                    except ValueError as e:
                        print(e)
                else:
                    print(f"Contact {name} not found.")
            
            elif command == "show-birthday":
                if len(args) < 1:
                    print("Use case: show-birthday <name>")
                    continue
                name = args[0]
                record = address_book.find(name)
                if record:
                    try:
                        print(record.show_birthday(name))
                    except IndexError as e:
                        print(e)
                else:
                    print(f"Contact {name} not found.")
            
            elif command == "birthdays":
                upcoming = address_book.get_upcoming_birthdays()
                if upcoming:
                    print("Upcoming birthdays within 7 days:")
                    for user in upcoming:
                        print(f"{user['name']} - {user['birthday']}")
                else:
                    print("No upcoming birthdays within 7 days.")
    
            elif command == "phone":
                if len(args) < 1:
                    print("Usage: phone <name>")
                    continue
                name = args[0]
                record = address_book.find(name)
                if record:
                    print(f"{name}'s phone numbers: {[str(phone) for phone in record.phones]}")
                else:
                    print(f"Contact {name} not found.")

            elif command == "all":
                print(address_book.display_records())
            
            elif command == "edit":
                if len(args) < 3:
                    print("Usage: edit <name> <old_phone> <new_phone>")
                    continue
                name, old_phone, new_phone = args[0], args[1], args[2]
                record = address_book.find(name)
                if record:
                    try:
                        record.edit_phone(old_phone, new_phone)
                        print(f"Updated contact: {record}")
                    except ValueError as e:
                        print(e)
                else:
                    print(f"Contact {name} not found.")
            
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