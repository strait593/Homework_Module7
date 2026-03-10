from main import *

# Test
address_book = AddressBook()

# Add first contact
record1 = Record('john')
record1.add_phone('1234567890')
record1.add_birthday('15.03.2000')
address_book.add_record(record1)

# Add second contact  
record2 = Record('jane')
record2.add_phone('9876543210')
record2.add_birthday('10.03.2000')
address_book.add_record(record2)

# Test get_upcoming_birthdays
result = address_book.get_upcoming_birthdays()
print('Result:', result)
print('Length:', len(result))
for item in result:
    print(f"{item['name']} - {item['congratulation_date']}")
