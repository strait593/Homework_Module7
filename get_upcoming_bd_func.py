from datetime import datetime, date, timedelta

def string_to_date(date_string):
    return datetime.strptime(date_string, "%Y.%m.%d").date()

def date_to_string(date_obj):
    return date_obj.strftime("%Y.%m.%d")

def prepare_user_list(user_data):
    prepared_list = []
    for user in user_data:
        prepared_list.append({"name": user["name"], "birthday": string_to_date(user["birthday"])})
    return prepared_list

def find_next_weekday(start_date, weekday):
    days_ahead = weekday - start_date.weekday()
    if days_ahead <= 0:
        days_ahead += 7
    return start_date + timedelta(days=days_ahead)

def adjust_for_weekend(birthday):
    # Check if Saturday (5) or Sunday (6)
    if birthday.weekday() >= 5:
        return find_next_weekday(birthday, 0)  # 0 is Monday
    return birthday

def get_upcoming_birthdays(users, days=7):
    upcoming_birthdays = []
    today = date.today()

    for user in users:
        # 1. Set birthday to current year
        birthday_this_year = user["birthday"].replace(year=today.year)

        # 2. Check if birthday has already passed this year
        if birthday_this_year < today:
            birthday_this_year = birthday_this_year.replace(year=today.year + 1)

        # 3. Calculate distance to birthday
        delta_days = (birthday_this_year - today).days

        # 4. If within the next 'days' (e.g., 7 days)
        if 0 <= delta_days <= days:
            # Adjust date if it falls on a weekend
            congratulation_date = adjust_for_weekend(birthday_this_year)
            
            # Convert back to string and add to the final list
            upcoming_birthdays.append({
                "name": user["name"], 
                "congratulation_date": date_to_string(congratulation_date)
            })
            
    return upcoming_birthdays

# --- Test Section ---
users_raw = [
    {"name": "Bill Gates", "birthday": "1955.3.25"},
    {"name": "Steve Jobs", "birthday": "1955.3.21"},
    {"name": "Jinny Lee", "birthday": "1956.3.22"},
    {"name": "Sarah Lee", "birthday": "1957.3.23"},
    {"name": "Jonny Lee", "birthday": "1958.3.22"},
    {"name": "John Doe", "birthday": "1985.01.23"},
    {"name": "Jane Smith", "birthday": "1990.01.27"}
]

prepared = prepare_user_list(users_raw)
print(get_upcoming_birthdays(prepared))