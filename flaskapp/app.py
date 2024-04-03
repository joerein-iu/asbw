# Copyright © 2023, Indiana University
# BSD 3-Clause License

from flask import Flask, render_template, request, redirect, url_for
import csv


app = Flask(__name__)

equipKeys = [
    "name",
    "summary",
    "description",
    "daily_rental_price",
    'weight',
    'purchase_date',
    'quantity',
    'notes'
]

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
        people={ 
            row['name']: {
                'name' : row['name'], 'email':row['email'], 
                'date_of_birth' : row['date_of_birth'], 'mobile_phone_number' : row["mobile_phone_number"],
                'role' : row['role']
        } for row in contents}
    return people

def set_equipment(all_equipment):
    equipKeys = ['name', 'summary', 'description', 'daily_rental_price', 'quantity', 'weight', 'image_path', 'purchase_date', 'notes']
    with open('equipment.csv', mode='w', newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=equipKeys)
        writer.writeheader()
        for equip in all_equipment.values():
            writer.writerow(equip)

def set_people(all_people):
    with open('people.csv', mode='w', newline="") as csvfile:
        fieldnames = ['name', 'email', 'date_of_birth', 'mobile_phone_number', 'role']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for person in all_people.values():
            writer.writerow(person)
            


@app.route("/")
def render_index():
    return render_template("index.html")


@app.route("/people/")
@app.route("/people/add/")
@app.route("/person/<pid>")
@app.route("/person/<pid>/edit")
def render_people(pid=None):
    people = load_people()
    if pid and pid in people.keys():
        return render_template("person.html", person=people[pid])
    return render_template("people.html", people=people)

@app.route("/equipment/")
@app.route("/equipment/add/")
@app.route("/specific/<eid>")
def render_equipment(eid=None):
    equipment = load_equipment()
    if eid and eid in equipment.keys():
        return render_template('specific.html', specific=equipment[eid])
    return render_template("equipment.html",equipment=equipment)

@app.route("/add-equipment/", methods=['GET','POST'])
@app.route("/specific/<eid>/edit", methods=['GET', 'POST'])
def add_equipment(eid=None):
    equip = load_equipment()
    equipment_item = None
    if eid and eid in equip.keys():
        equip = equip[eid]
    if request.method=="POST":
        all_equip = load_equipment()
        new_equipment = {}
        new_equipment['name']  = request.form['name']
        new_equipment['summary']  = request.form['summary']
        new_equipment['description']  = request.form['description']
        new_equipment['daily_rental_price']  = request.form['price']
        new_equipment['weight'] = request.form['weight']
        new_equipment['purchase_date']  = request.form['purchase_date'] 
        new_equipment['image_path'] = "images/null_image.jpg"
        new_equipment['quantity'] = request.form['quantity']
        new_equipment['notes'] = request.form['notes']

        all_equip[new_equipment['name']] = new_equipment

        set_equipment(all_equip)

        return redirect(url_for('render_equipment'))
    else:
        return render_template('item_form.html', equipment=equip)
    


@app.route("/add-person/", methods=['GET', 'POST'])
def add_person():
    if request.method == "POST":
        all_people = load_people()
        new_person = {
            'name': request.form['name'],
            'email': request.form['email'],
            'date_of_birth': request.form['dob'],
            'mobile_phone_number': request.form['phone'],
            'role': request.form['role']
        }
        
        all_people[new_person['name']] = new_person  

        set_people(all_people)
        return redirect(url_for('render_people'))
    else:
        return render_template('person_form.html', person=None)


@app.route("/person/<pid>/edit", methods=['GET', 'POST'])
@app.route("/person/<pid>/edit", methods=['GET', 'POST'])
def edit_person(pid):
    people = load_people()
    person = people.get(pid)

    if not person:
        return "Person not found", 404

    if request.method == "POST":
        person['name'] = request.form['name']
        person['email'] = request.form['email']
        person['date_of_birth'] = request.form['dob']
        person['mobile_phone_number'] = request.form['phone']
        person['role'] = request.form['role']
        
        people[person['name']] = person 

        set_people(people)
        return redirect(url_for('render_people'))
    else:
        return render_template('person_form.html', person=person)


