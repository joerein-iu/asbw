DROP TABLE IF EXISTS i211_rental;
DROP TABLE IF EXISTS i211_people;
DROP TABLE IF EXISTS i211_item;

CREATE TABLE i211_people (
    id INT NOT NULL AUTO_INCREMENT,
    name varchar(255) NOT NULL,
    email varchar(255) NOT NULL,
    date_of_birth DATE NOT NULL,
    mobile_phone_number bigint NOT NULL,
    role varchar(255) NOT NULL,
    PRIMARY KEY(id)
) ENGINE=Innodb;

CREATE TABLE i211_item (
    id INT NOT NULL AUTO_INCREMENT,
    name varchar(255) NOT NULL,
    summary varchar(255) NOT NULL,
    description varchar(255) NOT NULL,
    daily_rental_price float NOT NULL,
    weight int NOT NULL,
    image_path varchar(255) NOT NULL,
    item_condition varchar(255) NOT NULL,
    purchase_date date NOT NULL,
    notes varchar(255) NOT NULL,
    currently_availible BOOLEAN NOT NULL,
    PRIMARY KEY(id)
) ENGINE=Innodb;

CREATE TABLE i211_rental(
    id INT NOT NULL AUTO_INCREMENT,
    person_id INT NOT NULL,
    item_id INT NOT NULL,
    checkout_date DATE NOT NULL,
    due_date DATE NOT NULL,
    return_date DATE NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (person_id) REFERENCES i211_people(id),
    FOREIGN KEY (item_id) REFERENCES i211_item(id)
) ENGINE=Innodb;

INSERT INTO i211_people (name, email, date_of_birth, mobile_phone_number, role)
VALUES 
("Joe Reinert", "joerein@iu.edu","2002-11-10",5137661837,"member"),
("Rebecca Rhodes","rebeccarhodes@yahoo.com","2001-09-11",1234567890,"staff"),
("Emily Turner", "emturner@gmail.com", "1998-05-22", 9876543210, "member"),
("Michael Smith", "msmith@outlook.com", "2000-03-15", 4567891230, "member"),
("Lucas Grey", "lgrey@iu.edu", "2003-07-08", 5647382910, "staff"),
("Sarah Johnson", "sjohnson@yahoo.com", "1999-12-01", 7812345678, "member");

INSERT INTO i211_item (name, summary, description, daily_rental_price, weight, image_path, item_condition, purchase_date, notes, currently_availible)
VALUES
("Backpack", "A really cool backpack", "The most trust backpack ever", 10,6,"images/null_image.jpg","Good","2024-04-16","Cool zipper",1),
("Tent", "Compact camping tent", "Lightweight and easy to set up, fits two people comfortably", 15, 8, "images/tent_image.jpg", "Excellent", "2024-03-10", "Waterproof material", 1),
("Sleeping Bag", "Warm sleeping bag", "Suitable for temperatures down to 0 degrees Fahrenheit", 8, 3, "images/sleeping_bag.jpg", "Very Good", "2023-12-20", "Includes a compression sack", 1),
("Hiking Boots", "Durable hiking boots", "Waterproof and provides excellent ankle support", 12, 4, "images/boots_image.jpg", "Good", "2024-01-15", "Great for long hikes", 1),
("Portable Stove", "Gas portable stove", "Compact and reliable stove with adjustable heat settings", 9, 5, "images/stove_image.jpg", "Excellent", "2024-02-05", "Runs on butane canisters", 1),
("Flashlight", "Rechargeable flashlight", "High lumens flashlight with multiple light modes", 5, 1, "images/flashlight_image.jpg", "Excellent", "2024-04-01", "Battery lasts up to 48 hours", 1);

INSERT INTO i211_rental (person_id, item_id, checkout_date, due_date, return_date)
VALUES
(1, 1, '2024-04-10', '2024-04-20', '2024-04-18'),
(2, 2, '2024-04-12', '2024-04-22', '2024-04-22'),
(3, 3, '2024-04-15', '2024-04-25', '2024-04-25'),
(4, 4, '2024-04-18', '2024-04-28', '2024-04-27'),
(5, 5, '2024-04-20', '2024-04-30', '2024-04-30'),
(6, 6, '2024-04-22', '2024-05-02', '2024-05-01');



