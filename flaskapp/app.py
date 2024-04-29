# Copyright © 2023-2024, Indiana University
# BSD 3-Clause License

import re
from csv import DictReader, DictWriter
from datetime import date
from operator import itemgetter
from random import randint
from typing import Optional, List, Dict

from flask import Flask, request, render_template, redirect, url_for
import flaskapp.db as db


app = Flask(__name__)


def validate_date(date_string: str) -> str:
    """Return the string if it's in ISO format, or '' otherwise."""
    try:
        date.fromisoformat(date_string)
    except ValueError:
        return ""
    return date_string


def validate_phone(phone_string: str) -> str:
    """Return the 10 digits in a phone number, or '' otherwise."""
    new_phone = re.sub("[^0-9]", "", phone_string)
    if len(new_phone) != 10:
        return ""
    return new_phone


def load_equipment() -> List[Dict[str, str]]:
    """Return a list[dict] of the equipment sorted by name"""
    return db.get_all_items()


def load_item(item_id=Optional[str]) -> Optional[Dict[str, str]]:
    """Return something or nothing using an item's id"""
    return db.get_one_item(item_id)


def load_people() -> List[Dict[str, str]]:
    """Return a dictionary of people, sorted on `date_of_birth`"""
    return db.get_people()


def load_person(person_id=None) -> Optional[Dict[str, str]]:
    """Load a person based on their id."""
    return db.get_person(person_id)


@app.route("/")
def render_index():
    return render_template("index.html")


@app.route("/people/")
def render_people_page():
    return render_template("people.html", people=load_people())


def inspect_person(person: Dict[str, str]) -> None:
    """!mutates: any value that does not pass is replaced with empty string"""

    person["date_of_birth"] = validate_date(person["date_of_birth"])
    person["mobile_phone_number"] = validate_phone(person["mobile_phone_number"])

    if person["role"] not in ("staff", "member"):
        person["role"] = ""


@app.route("/people/add/", methods=["GET", "POST"])
def render_add_person():
    if request.method == "GET":
        return render_template("person_form.html", person=dict())

    # POST
    new_person = dict(request.form)

    inspect_person(new_person)
    if any(v == "" for v in new_person.values()):
        # If any error occurred, tell the user to try again
        return render_template("person_form.html", person=new_person, alert=True)

    # We didn't re-render, so we can save a new copy of the CSV
    # As an exercise: what *low-probability edge case* am I ignoring?
    db.add_person(new_person)
    return redirect(url_for("render_people_page"))


@app.route("/people/<person_id>/edit/", methods=["GET", "POST"])
def render_edit_person(person_id: Optional[str] = None):
    if request.method == "GET":
        return render_template(
            "person_form.html", person_id=person_id, person=load_person(person_id)
        )

    # POST
    updated_person = dict(request.form)
    inspect_person(updated_person)

    if any(v == "" for v in updated_person.values()):
        return render_template("person_form.html", person_id=person_id, person=updated_person, alert=True)

    # Validation success: Update the row with matching person_id
    db.update_person(person_id,updated_person)

    return redirect(url_for("render_one_person", person_id=person_id))


@app.route("/people/<person_id>/")
def render_one_person(person_id: Optional[str] = None):
    return render_template("person.html", person_id=person_id, person=load_person(person_id))


@app.route("/equipment/")
def render_equipment_page():
    return render_template("equipment.html", equipment=load_equipment())

@app.route("/equipment/<item_id>/")
@app.route("/equipment/<item_id>/")
def render_one_item(item_id: Optional[str] = None):
    item = load_item(item_id)
    if not item:
        return "Item not found", 404 
    print(item)
    people = load_people()
    members = [person for person in people if person["role"] == "member"]
    return render_template("item.html", item_id=item_id, item=item, members=members)



@app.route("/equipment/add/", methods=["GET", "POST"])
def render_add_equipment():
    if request.method == "GET":
        return render_template("item_form.html", item=dict())

    # POST: assume no bad data
    new_item = dict(request.form)
    db.add_item(new_item)

    return redirect(url_for("render_equipment_page"))


@app.route("/equipment/<item_id>/edit/", methods=["GET", "POST"])
def render_edit_equipment(item_id: Optional[str] = None):
    if request.method == "GET":
        return render_template("item_form.html", item_id=item_id, item=load_item(item_id))

    # POST
    updated = dict(request.form)

    # Keep the `id` and `image_path` the same from before.
    id = db.get_item_id(item_id)
    print(item_id)
    db.update_one_item(item_id, updated)

    return redirect(url_for("render_one_item", item_id=item_id))

@app.route("/equipment/<item_id>/rent/", methods=["POST"])
def rent_item(item_id):
    member_id = request.form['member_id']
    db.rent_one_item(member_id, item_id)
    return redirect(url_for("render_one_item", item_id=item_id))

@app.route("/equipment/<item_id>/return/", methods=["POST"])
def return_item(item_id):
    db.return_one_item(item_id)
    return redirect(url_for("render_one_item", item_id=item_id))



# @app.route("/equipment/<item_id>/rent/", methods=["POST"])
# def rent_item(person_id: int, item_id: int):
#     #uses a query to set an item as unavailable, then sets the due date and the takeout date
#     #redirects to the item

# @app.route("/equipment/<item_id>/return", methods=["POST"])
# def return_item(item_id):
#     #uses a query to set the item as returned
#     #redirects back to the item
#     pass


#so basically have to add a section in the html for the item to display whether its availible or not availible
#have to pass the item section the list of members if its not current rented out, 