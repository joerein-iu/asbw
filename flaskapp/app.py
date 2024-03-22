# Copyright © 2023, Indiana University
# BSD 3-Clause License

from flask import Flask, render_template
import csv

app = Flask(__name__)

def load_people():
    with open('people.csv') as csvfile:
        contents=csv.DictReader(csvfile)
        people={ row['name']: {'name' : row['name'], 'email':row['email'],
                             'date_of_birth': row['date_of_birth'],
                             'mobile_phone_number':row['mobile_phone_number'], 'role':row['role']
        } for row in contents}
        return people

def load_equipment():
    with open('equipment.csv') as csvfile:
        contents=csv.DictReader(csvfile)
        equipment={ row['name']: {'name' : row['name'], 'summary':row['summary'],
                             'description': row['description'], 'daily_rental_price' : row['daily_rental_price'],
                             'quantity':row['quantity'],'weight':row['weight'],
                             'image_path':row['image_path'], 'purchase_date':row['purchase_date'],
                             'notes':row['notes']
        } for row in contents}
    return equipment

def load_people():
    with open('people.csv') as csvfile:
        contents=csv.DictReader(csvfile)
        equipment={ 
            row['name']: {
                'name' : row['name'], 'email':row['email'], 
                'date_of_birth' : row['date_of_birth'], 'mobile_phone_number' : row["mobile_phone_number"],
                'role' : row['role']
        } for row in contents}
    return equipment



@app.route("/")
def render_index():
    return render_template("index.html")


@app.route("/people/")
@app.route("/person/<pid>")
def render_people(pid=None):
    people = load_people()
    if pid and pid in people.keys():
        return render_template("person.html", person=people[pid])
    return render_template("people.html", people=people)

@app.route("/equipment/")
@app.route("/specific/<eid>")
def render_equipment(eid=None):
    equipment = load_equipment()
    if eid and eid in equipment.keys():
        return render_template('specific.html', specific=equipment[eid])
    return render_template("equipment.html",equipment=equipment)


