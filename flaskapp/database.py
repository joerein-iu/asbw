from typing import Any, Dict, List

from pymysql import connect
from pymysql.cursors import DictCursor
from datetime import timedelta, datetime

from flaskapp.config import DB_HOST, DB_USER, DB_PASSWORD, DB_DATABASE

"""
Big Hint #1: For all items and people (adding and updating), you can either use dictionaries,
or write your functions with all of the attributes in the function
signature (like we did in the lecture repo).

For example:

```
add_person(new_person: Dict[str, str])
```

or

```
add_person(name, email, date_of_birth, mobile_phone_number, role)
```

Big Hint #2: Depending on how you wrote your 2.2 code, one might be
far easier than the other.
"""


def get_connection():
    return connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_DATABASE,
        cursorclass=DictCursor,
    )

conn = pymysql.connect(host=DB_HOST,
    user=DB_USER,
    password=DB_PASS,
    database=DB_DATABASE,
    cursorclass=pymysql.cursors.DictCursor)


def get_people() -> List[Dict[str, Any]]:
    """Get a list of dictionaries for every person in the database."""

    query = "SELECT * FROM i211_people"

    with conn:
        with conn.cursor() as cursor:
            cursor.execute(query)
            people = cursor.fetchall()
    return people
    


def get_person(person_id: int) -> Dict[str, Any]:
    """Get a person by their id, return a dictionary containing their data."""
    query = "SELECT * FROM i211_people WHERE id = %s"
    person = {}
    with conn.cursor() as cursor:
            cursor.execute(query, (person_id,))
            person = cursor.fetchone()
    conn.close()

    return person if person else {}


def get_members() -> List[Dict[str, Any]]:
    """
    Only *members* can rent items. Return a list of dictionaries for all
    people with role=member.

    Hint: You might need this in 3.3 for renting an item.
    """
    query = "SELECT * FROM i211_people WHERE role = 'member'"

    members = []


    with conn.cursor() as cursor:
        cursor.execute(query)
        members = cursor.fetchall()

    conn.close()  # we never did this in class but im at TA from 308 so this is just second nature and will do it everytime.

    return members


def add_person(new_person: Dict[str, Any]) -> None:
    """Takes data for a person, puts it in the person table.

    See also: Big Hint #1 (above)
    """
    query = """
    INSERT INTO i211_people (name, email, date_of_birth, mobile_phone_number, role)
    VALUES (%s, %s, %s, %s, %s)
    """

    with conn.cursor() as cursor:
        cursor.execute(query, (
            new_person['name'],
            new_person['email'],
            new_person['date_of_birth'],
            new_person['mobile_phone_number'],
            new_person['role']
        ))
        conn.commit()

    conn.close()



def update_person(person_id: int, person_data: Dict[str, str]) -> None:
    """Updates the person table with 'person_data' for the person with 'person_id'

    See also: Big Hint #1 (above)
    """
    update_parts = []
    values = []
    for key, value in person_data.items():
        update_parts.append(f"{key} = %s")
        values.append(value)
    update_statement = ", ".join(update_parts)

    query = f"UPDATE i211_people SET {update_statement} WHERE id = %s"
    values.append(person_id)

    with conn.cursor() as cursor:
            cursor.execute(query, values)
            conn.commit()  

    conn.close


def get_all_items() -> List[Dict[str, Any]]:
    """Get all items from the 'item' table."""
    query = "SELECT * FROM i211_item"

    items = [] 

    with conn.cursor() as cursor:
            cursor.execute(query)
            items = cursor.fetchall()

    conn.close()

    return items


def get_one_item(item_id: int) -> Dict[str, Any]:
    """Get data for the item with `item_id`"""
    
    query = "SELECT * FROM i211_item WHERE id = %s"
    item = {}

    with conn.cursor() as cursor:
            cursor.execute(query, (item_id,))
            item = cursor.fetchone()
    conn.close()

    return item if item else {}


def add_item(new_item: Dict[str, Any]) -> None:
    """Takes data for a new item, puts it in the 'item' table.

    See also: Big Hint #1 (above)
    """
    query = """
    INSERT INTO i211_item (name, summary, description, daily_rental_price, weight, image_path,
                           item_condition, purchase_date, notes, currently_availible)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    with conn.cursor() as cursor:
            cursor.execute(query, (
                new_item['name'],
                new_item['summary'],
                new_item['description'],
                new_item['daily_rental_price'],
                new_item['weight'],
                new_item['image_path'],
                new_item['item_condition'],
                new_item['purchase_date'],
                new_item['notes'],
                new_item['currently_availible']
            ))
            conn.commit() 
    conn.close() 


def update_one_item(item_id: int, updated_equipment: Dict[str, Any]) -> None:
    """Updates data for an 'item' using the 'item_id'

    See also: Big Hint #1 (above)
    """
    update_parts = []
    values = []
    for key, value in updated_equipment.items():
        update_parts.append(f"{key} = %s")
        values.append(value)
    update_statement = ", ".join(update_parts)

    query = f"UPDATE i211_item SET {update_statement} WHERE id = %s"
    values.append(item_id)

    with conn.cursor() as cursor:
            cursor.execute(query, values)
            conn.commit()

    conn.close()


def get_due_dates() -> List[Dict[str, Any]]:
    """Get the 'item_id' and the 'due_date' for each item that is rented out.

    Hint:
        [{"item_id": ..., "due_date": ...}, ...]
        You might need this in 3.3 for displaying an item.
    """
    query = "SELECT item_id, due_date FROM i211_rental"
    due_dates = []

    with conn.cursor() as cursor:
            cursor.execute(query)
            due_dates = cursor.fetchall()

    conn.close()

    return due_dates


def rent_one_item(person_id: int, item_id: int) -> None:
    """
    Inserts appropriate data into the database representing the the person
    is renting an item.

    "due date" in the rental table should be set to 14 days from the current date.
    """
    checkout_date = datetime.now()
    due_date = checkout_date + timedelta(days=14)

    query = """
    INSERT INTO i211_rental (person_id, item_id, checkout_date, due_date, return_date)
    VALUES (%s, %s, %s, %s, NULL)  # Set return_date as NULL initially
    """
    #I hate writing queries all on one line. Again, ta for 308, my brain works better this way for inserts

    with conn.cursor() as cursor:
            cursor.execute(query, (person_id, item_id, checkout_date.strftime('%Y-%m-%d'), due_date.strftime('%Y-%m-%d')))
            conn.commit()

    conn.close()



def return_one_item(item_id: int):
    """
    Updates the database to indicate the item was returned. Both the
    'item' and 'rental' table must be updated appropriately.
    """
    return_date = datetime.now().strftime('%Y-%m-%d')

    update_rental_query = """
    UPDATE i211_rental
    SET return_date = %s
    WHERE item_id = %s AND return_date IS NULL;  # ensures that only unreturned items are updated
    """

    update_item_query = """
    UPDATE i211_item
    SET currently_availible = TRUE
    WHERE id = %s;
    """
    with conn.cursor() as cursor:
            cursor.execute(update_rental_query, (return_date, item_id))
            cursor.execute(update_item_query, (item_id,))
            conn.commit()
    conn.close()


def get_rentals_by_person(person_id: int) -> List[Dict[str, Any]]:
    """
    Return all attributes from the 'item' table for all items rented
    out by the person with 'person_id'.
    """
    query = """
    SELECT i.*
    FROM i211_item i
    JOIN i211_rental r ON i.id = r.item_id
    WHERE r.person_id = %s;
    """#again 308 effect

    items = []  

    with conn.cursor() as cursor:
        cursor.execute(query, (person_id,))
        items = cursor.fetchall()
    conn.close()
    return items


def get_all_past_item_rentals(item_id: int) -> List[Dict[str, Any]]:
    """Return all data in 'rental' for item with 'item_id'."""
    query = """
    SELECT *
    FROM i211_rental
    WHERE item_id = %s;
    """# me no like 1 line queries

    rentals = []

    with conn.cursor() as cursor:
            cursor.execute(query, (item_id,))
            rentals = cursor.fetchall()
    
    conn.close()

    return rentals
