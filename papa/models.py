from sqlalchemy import Column, Integer, String, ForeignKey, orm
from sqlalchemy.ext.declarative import declarative_base
from marshmallow import Schema, fields, post_load
from papasha import session

Base = declarative_base()


class User(Base):
    __tablename__ = "user"
    user_id = Column("user_id", Integer, primary_key=True)
    username = Column('username', String)
    password = Column('password', String)


class Item(Base):
    __tablename__ = "item"
    name = Column('name', String, unique=True)
    item_id = Column('item_id', Integer, primary_key=True)
    quantity = Column("quantity", Integer)
    price = Column('price', String, unique=True)
    describe = Column('describe', String, unique=True)


class Provisor(Base):
    __tablename__ = "provisor"
    provisor_id = Column('provisor_id', Integer, primary_key=True)
    provisorname = Column('provisorname', String, unique=True)
    provisorpass = Column('provisorpass', String, unique=True)


class Order(Base):
    __tablename__ = "order"
    order_id = Column('order_id', Integer, primary_key=True)
    order_user_id = Column(Integer, ForeignKey(User.user_id))
    order_item_id = Column(Integer, ForeignKey(Item.item_id))
    quantity_in_order = Column('quantity_in_order', Integer)


class Order_demand(Base):
    __tablename__ = "order_demand"
    order_id = Column('order_demand_id', Integer, primary_key=True)
    order_demand_user_id = Column(Integer, ForeignKey(User.user_id))
    order_demand_item_id = Column(Integer, ForeignKey(Item.item_id))
    quantity_in_order_demand = Column('quantity_in_order_demand', Integer)


class UserSchema(Schema):
    user_id = fields.Int()
    username = fields.Str()
    password = fields.Str()

    @post_load
    def make_user(self, data, **kwargs):
        return User(**data)


class ItemSchema(Schema):
    name = fields.Str()
    item_id = fields.Int()
    quantity = fields.Int()
    price = fields.Str()
    describe = fields.Str()
    @post_load
    def make_item(self, data, **kwargs):
        return Item(**data)

class ProvisorSchema(Schema):
    provisor_id = fields.Int()
    provisorname = fields.Str()
    provisorpass = fields.Str()

    @post_load
    def make_provisor(self, data, **kwargs):
        return Provisor(**data)

class OrderSchema(Schema):
    order_id = fields.Int()
    order_user_id = fields.Int()
    order_item_id = fields.Int()
    quantity_in_order = fields.Int()
    @post_load
    def make_order(self, data, **kwargs):
        return Order(**data)

class Order_DemandSchema(Schema):
    order_demand_id = fields.Int()
    order_demand_user_id = fields.Int()
    order_demand_item_id = fields.Int()
    quantity_in_order_demand = fields.Int()
    @post_load
    def make_order_demand(self, data, **kwargs):
        return Order_demand(**data)
