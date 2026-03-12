import pickle
from main import AddressBook

def save_data(book,filename="addressbook.pkl"):
    with open(filename, 'wb', encoding='utf-8') as pickled:
        pickle.dump(pickled, book)

def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as addressbook:
            return pickle.load(addressbook)
    except FileNotFoundError:
        return AddressBook()