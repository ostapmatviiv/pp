CREATE TABLE "user" (
	user_id INTEGER NOT NULL,
	username VARCHAR,
	password VARCHAR,
	PRIMARY KEY (user_id),
	UNIQUE (username),
	UNIQUE (password)
)

CREATE TABLE item (
	name VARCHAR,
	item_id INTEGER NOT NULL,
	quantity INTEGER,
	price VARCHAR,
	describe VARCHAR,
	PRIMARY KEY (item_id),
	UNIQUE (name),
	UNIQUE (price),
	UNIQUE (describe)
)

CREATE TABLE provisor (
	provisor_id INTEGER NOT NULL,
	provisorname VARCHAR,
	provisorpass VARCHAR,
	PRIMARY KEY (provisor_id),
	UNIQUE (provisorname),
	UNIQUE (provisorpass)
)

CREATE TABLE "order" (
	order_id INTEGER NOT NULL,
	order_user_id INTEGER,
	order_item_id INTEGER,
	quantity_in_order INTEGER,
	PRIMARY KEY (order_id),
	FOREIGN KEY(order_user_id) REFERENCES "User" (user_id),
	FOREIGN KEY(order_item_id) REFERENCES item (item_id)
)

CREATE TABLE "order_demand" (
	order_demand_id INTEGER NOT NULL,
	order_demand_user_id INTEGER,
	order_demand_item_id INTEGER,
	quantity_in_order_demand INTEGER,
	PRIMARY KEY (order_id_demand),
	FOREIGN KEY(order_demand_user_id) REFERENCES "User" (user_id),
	FOREIGN KEY(order_demand_item_id) REFERENCES item (item_id)
)