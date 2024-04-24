from typing import Any, Dict, List

from pymysql import connect
from pymysql.cursors import DictCursor

from flaskapp.config import DB_HOST, DB_USER, DB_PASS, DB_DATABASE

"""
Big Hint #1: Alexander used dictionaries. Example usages are at
the bottom of this file.

For example:

```
add_person(
    {
        "name": "Alan Perlis",
        "email": "perlis@example.com",
        "date_of_birth": "1990-01-01",
        "mobile_phone_number": "1112223333",
        "role": "member",
    }
)
```
"""


def get_connection():
    return connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASS,
        database=DB_DATABASE,
        cursorclass=DictCursor,
    )


def get_people() -> List[Dict[str, Any]]:
    """Get a list of dictionaries for every person in the database."""
    conn = get_connection()
    with conn.cursor() as curr:
        curr.execute("select * from i211_people")
        people = curr.fetchall()
    conn.close()
    return people


def get_person(person_id: int) -> Dict[str, Any]:
    """Get a person by their id, return a dictionary containing their data."""
    conn = get_connection()
    with conn.cursor() as curr:
        curr.execute("select * from i211_people where id = %s", (person_id,))
        person = curr.fetchone()
    conn.close()
    return person



def get_members() -> List[Dict[str, Any]]:
    """Only *members* can rent items.
    """
    conn = get_connection()
    with conn.cursor() as curr:
        curr.execute("select * from i211_people where role = 'member'")
        members = curr.fetchall()
    conn.close()
    return members


def add_person(new_person: Dict[str, Any]) -> None:
    """Takes data for a person, puts it in the person table.

    See also: Big Hint #1 (above)
    """
    conn = get_connection()
    with conn.cursor() as curr:
        curr.execute(
            "insert into i211_people (name, email, date_of_birth, mobile_phone_number, role) values (%s, %s, %s, %s, %s)",
            (
                new_person["name"],
                new_person["email"],
                new_person["date_of_birth"],
                new_person["mobile_phone_number"],
                new_person["role"],
            )
        )
    conn.commit()
    conn.close()



def update_person(person_id: int, person_data: Dict[str, str]) -> None:
    """Updates the person table with 'person_data' for the person with 'person_id'

    See also: Big Hint #1 (above)
    """
    conn = get_connection()
    with conn.cursor() as curr:
        curr.execute(
            "update i211_people set name=%s, email=%s, date_of_birth=%s, mobile_phone_number=%s, role=%s where id=%s",
            (
                person_data["name"],
                person_data["email"],
                person_data["date_of_birth"],
                person_data["mobile_phone_number"],
                person_data["role"],
                person_id,
            )
        )
    conn.commit()
    conn.close()


def get_all_items() -> List[Dict[str, Any]]:
    """Get all items from the 'item' table."""
    conn = get_connection()
    with conn.cursor() as curr:
        curr.execute("select * from i211_item")
        items = curr.fetchall()
    conn.close()
    return items



def get_one_item(item_id: int) -> Dict[str, Any]:
    """Get data for the item with `item_id`"""
    conn = get_connection()
    with conn.cursor() as curr:
        curr.execute("select * from i211_item where id = %s", (item_id,))
        item = curr.fetchone()
    conn.close()
    return item


def add_item(new_item: Dict[str, Any]) -> None:
    """Takes data for a new item, puts it in the 'item' table.
    """
    conn = get_connection()
    with conn.cursor() as curr:
        curr.execute(
            "insert into i211_item (name, summary, description, daily_rental_price, weight, purchase_date, item_condition, notes, image_path, currently_availible) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (
                new_item["name"],
                new_item["summary"],
                new_item["description"],
                new_item["daily_rental_price"],
                new_item["weight"],
                new_item["purchase_date"],
                "good",
                new_item["notes"],
                "images/null_image.jpg",
                1,
            )
        )
    conn.commit()
    conn.close()


def update_one_item(item_id: int, updated_equipment: Dict[str, Any]) -> None:
    """Updates data for an 'item' using the 'item_id'
    """
    conn = get_connection()
    with conn.cursor() as curr:
        curr.execute(
            "update i211_item set name=%s, summary=%s, description=%s, daily_rental_price=%s, weight=%s, purchase_date=%s, item_condition=%s, notes=%s, image_path=%s, currently_availible=%s where id = %s",
            (
                updated_equipment["name"],
                updated_equipment["summary"],
                updated_equipment["description"],
                updated_equipment["daily_rental_price"],
                updated_equipment["weight"],
                updated_equipment["purchase_date"],
                "good",
                updated_equipment["notes"],
                "images/null_image.jpg",
                1,
                item_id,
            )
        )
    conn.commit()
    conn.close()


def get_due_dates() -> List[Dict[str, Any]]:
    """Get the 'item_id' and the 'due_date' for each item that is rented out.
    """
    conn = get_connection()
    with conn.cursor() as curr:
        curr.execute("select item_id, due_date from i211_rental where return_date is null")
        items = curr.fetchall()
    conn.close()
    return items


def rent_one_item(person_id: int, item_ind: int) -> None:
    """
    Inserts appropriate data into the database representing the the person
    is renting an item.

    TODO(hayesall): This does not validate that an item is `currently_available`.
        I assume that has already been done elsewhere.
    """
    conn = get_connection()
    with conn.cursor() as curr:
        curr.execute("insert into i211_rental (person_id, item_id) values (%s, %s)", (person_id, item_ind))
        curr.execute("update i211_item set currently_available = 0 where id = %s", (item_ind,))
    conn.commit()
    conn.close()


def return_one_item(item_ind: int):
    """
    Updates the database to indicate the item was returned.

    TODO(hayesall): I *think* the updates will fail if this gets called on an
        invalid `item_id` (e.g. where there is not a NULL return date),
        but this hasn't been tested thoroughly.
    """
    conn = get_connection()
    with conn.cursor() as curr:

        # Since an item cannot be rented out
        # by multiple people at the same time:
        # we can update the `rental` table using
        # an item_id and a NULL value.
        #
        # A NULL can become a date, but not the
        # other way around.

        curr.execute("update i211_rental set return_date = curdate() where return_date is null and item_id = %s", (item_ind,))

        curr.execute("update i211_item set currently_available = 1 where id = %s", (item_ind,))

    conn.commit()
    conn.close()


def get_rentals_by_person(person_id: int) -> List[Dict[str, Any]]:
    """
    Return all attributes from the 'item' table for all items rented
    out by the person with 'person_id'.
    """
    conn = get_connection()
    with conn.cursor() as curr:

        # Since a person can rent the same item multiple times, this also
        # includes dates from the rental table to disambiguate rows.

        curr.execute("select i211_item.*, checkout_date, return_date, due_date from item join rental on rental.item_id = item.id where person_id = %s", (person_id,))
        items = curr.fetchall()
    conn.close()
    return items


def get_all_past_item_rentals(item_id: int) -> List[Dict[str, Any]]:
    """Return all data in 'rental' for item with 'item_id'."""
    conn = get_connection()
    with conn.cursor() as curr:

        # This also joins on the person table, since a human-readable
        # name is easier to understand than an indecipherable "1".

        curr.execute("select name, rental.* from i211_rental join person on rental.person_id = person.id where item_id = %s", (item_id,))
        items = curr.fetchall()
    conn.close()
    return items

def get_person_id(name):
    conn = get_connection()
    with conn.cursor() as curr:
        curr.execute("select id from i211_people where name = %s", (name,))
        id = curr.fetchall()
    conn.close()
    return id


def get_item_id(item):
    conn = get_connection()
    with conn.cursor() as curr:
        curr.execute("select id from i211_item where name = %s", (item,))
        id = curr.fetchall()
    conn.close()
    return id

if __name__ == "__main__":

    from pprint import pprint

    print(get_people())
    print(get_person(1))

    pprint(get_members())

    add_person(
        {
            "name": "Alan Perlis",
            "email": "perlis@example.com",
            "date_of_birth": "1990-01-01",
            "mobile_phone_number": "1112223333",
            "role": "member",
        }
    )

    update_person(
        7,
        {
            "name": "Alan Perlis",
            "email": "perlis@example.com",
            "date_of_birth": "1980-01-01",
            "mobile_phone_number": "1112223333",
            "role": "member",
        }
    )

    pprint(get_all_items())

    pprint(get_one_item(1))

    add_item(
        {
            "name": "Binoculars",
            "summary": "TODO",
            "description": "TODO",
            "daily_rental_price": "5",
            "weight": "2",
            "purchase_date": "2023-01-01",
            "item_condition": "new",
            "notes": "TODO",
            "image_path": "images/null_image.jpg",
            "currently_available": "1",
        }
    )

    update_one_item(
        7,
        {
            "name": "Binoculars",
            "summary": "TODO",
            "description": "TODO",
            "daily_rental_price": "5",
            "weight": "2",
            "purchase_date": "2023-01-01",
            "item_condition": "new",
            "notes": "TODO",
            "image_path": "images/null_image.jpg",
            "currently_available": "1",
        }
    )

    pprint(get_due_dates())

    rent_one_item(1, 1)
    return_one_item(1)

    pprint(get_rentals_by_person(1))

    pprint(get_all_past_item_rentals(1))