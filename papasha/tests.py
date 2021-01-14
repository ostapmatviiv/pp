import json

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.util import b64encode
from flask_testing import TestCase
from papa.models import *
from papa import *

from main import *
from papasha import bcrypt

engine = create_engine('sqlite:///database.db', echo=True, connect_args={'check_same_thread': False})
Session = sessionmaker(bind=engine)
Base.metadata.bind = engine


def get_test_user_data(username='test_username',
                       password='test_password'):
    user = {'username': "user_name",
            'password': "password"
            }
    return user


class Tests(TestCase):
    app.config['TESTING'] = True
    app.config['LIVESERVER_PORT'] = 5000

    def create_app(self):
        return app

    def setUp(self):
        session = Session()
        Base.metadata.drop_all()
        Base.metadata.create_all()
        user = User(username="Ostap", password='$2b$12$drbRSWXPLKKsASeQ5VFiN.Vi7utInN5hxuXOpOdux8EqGrzDiucG2')
        user2 = User(username="Alex", password='$2b$12$WS9clYn2x68I/Z1c6LBlOOe.7A1JFZo9ygeKIBsNAJt.obSQ4FQVS')
        provisor1 = Provisor(provisorname="Valodya",
                             provisorpass="$2b$12$bloGTkJ770/BlZhhI1R/fODZfQCfBANCGGPdkOOj8SfaX3lBjB/re")
        item1 = Item(name='Mezym', quantity=30, price='29.90', describe='123 mezym, pislya yizhi lehshe z nym')
        item2 = Item(name='Sorbex', quantity=100, price='200', describe='sorbex vid zhyvota')
        order1 = Order(order_user_id=1, order_item_id=1, quantity_in_order=10)
        order2 = Order(order_user_id=1, order_item_id=2, quantity_in_order=13)
        session.add(user)
        session.add(user2)
        session.add(provisor1)
        session.add(item1)
        session.add(item2)
        session.add(order1)
        session.add(order2)
        session.commit()
        session.close()


class TestApi(Tests):
    def test_invalid_auth(self):
        credentials = b64encode(b"invalid:invalid")
        response = self.client.get('/user', headers={"Authorization": f"Basic {credentials}"})
        statuscode = response.status_code
        self.assertEqual(405, statuscode)

    def test_user_post(self):
        test = self.client.post("/user", json={"username": "Ostap", "password": "12"})
        print(test.data)
        self.assertEqual(201, test.status_code)

    def test_user_post_bad(self):
        test = self.client.post("/users", json={"username": "Ostap", "password": "12"})
        print(test.data)
        self.assertEqual(404, test.status_code)

    def test_getuserbyid(self):
        credentials = b64encode(b"Ostap:12")
        res = self.client.get("/user/1", headers={"Authorization": f"Basic {credentials}"})
        assert res.status_code == 200

    def test_getuserbyidwrong(self):
        credentials = b64encode(b"Ostap:12")
        res = self.client.get("/user/10", headers={"Authorization": f"Basic {credentials}"})
        assert res.status_code == 404

    def test_putuserbad(self):
        credentials = b64encode(b"Ostap:12")
        res = self.client.put("/user/1sad", headers={"Authorization": f"Basic {credentials}"},
                              json={"username": "not", "password": "123"}, content_type='application/json')
        print(res.data)
        self.assertEqual(404, res.status_code)

    def test_putuser(self):
        credentials = b64encode(b"Ostap:12")
        res = self.client.put("/user/1", headers={"Authorization": f"Basic {credentials}"},
                              json={"username": "not", "password": "123"}, content_type='application/json')
        print(res.data)
        self.assertEqual(200, res.status_code)

    def test_getuserbyid(self):
        credentials = b64encode(b"Ostap:12")
        res = self.client.get("/user/1", headers={"Authorization": f"Basic {credentials}"})
        assert res.status_code == 200

    def test_getuserbyidwrong(self):
        credentials = b64encode(b"Ostap:12")
        res = self.client.get("/user/100", headers={"Authorization": f"Basic {credentials}"})
        assert res.status_code == 404

    def test_deleteuser(self):
        credentials = b64encode(b"Ostap:12")
        res = self.client.delete("/user/1", headers={"Authorization": f"Basic {credentials}"})
        assert res.status_code == 200

    def test_deleteuserwrong(self):
        credentials = b64encode(b"Ostap:12")
        res = self.client.delete("/user/1as", headers={"Authorization": f"Basic {credentials}"})
        assert res.status_code == 404

    def test_user_post_not_acceptable(self):
        test = self.client.post("/user", json={"username": 1, "password": "sdfasfa"})
        print(test.data)
        self.assertEqual(405, test.status_code)

    def test_getitems(self):
        credentials = b64encode(b"Ostap:12")
        res = self.client.get("/items", headers={"Authorization": f"Basic {credentials}"})
        assert res.status_code == 200

    def test_getitembyid(self):
        credentials = b64encode(b"Ostap:12")
        res = self.client.get("/items/1", headers={"Authorization": f"Basic {credentials}"})
        assert res.status_code == 200

    def test_getwrongitembyid(self):
        credentials = b64encode(b"Ostap:12")
        res = self.client.get("/items/1asd", headers={"Authorization": f"Basic {credentials}"})
        assert res.status_code == 404

    def test_postorder(self):
        credentials = b64encode(b"Ostap:12")
        res = self.client.post("/order", headers={"Authorization": f"Basic {credentials}"},
                               json={"order_user_id": 1, "order_item_id": 1, "quantity_in_order": 10})
        assert res.status_code == 201

    def test_postorderwrong(self):
        credentials = b64encode(b"Ostap:12")
        res = self.client.post("/order", headers={"Authorization": f"Basic {credentials}"},
                               json={"order_user_id": "asd", "order_item_id": 1, "quantity_in_order": 10})
        assert res.status_code == 405

    def test_getorderbyid(self):
        credentials = b64encode(b"Ostap:12")
        res = self.client.get("/order/1", headers={"Authorization": f"Basic {credentials}"})
        assert res.status_code == 200

    def test_getorderbyidwrong(self):
        credentials = b64encode(b"Ostap:12")
        res = self.client.get("/order/6", headers={"Authorization": f"Basic {credentials}"})
        assert res.status_code == 404

    def test_deleteorderbyid(self):
        credentials = b64encode(b"Ostap:12")
        res = self.client.delete("order/1", headers={"Authorization": f"Basic {credentials}"})
        assert res.status_code == 200

    def test_deleteorderbyidwrong(self):
        credentials = b64encode(b"Ostap:12")
        res = self.client.delete("order/1asd", headers={"Authorization": f"Basic {credentials}"})
        assert res.status_code == 404

    def test_postorderspecial(self):
        credentials = b64encode(b"Ostap:12")
        res = self.client.post("/order/special", headers={"Authorization": f"Basic {credentials}"},
                               json={"order_demand_user_id": 1, "order_demand_item_id": 1,
                                     "quantity_in_order_demand": 10})
        assert res.status_code == 201

    def test_postorderspecialwrong(self):
        credentials = b64encode(b"Ostap:12")
        res = self.client.post("/order/special", headers={"Authorization": f"Basic {credentials}"},
                               json={"order_demand_user_id": "asd", "order_demand_item_id": 1,
                                     "quantity_in_order_demand": 10})
        assert res.status_code == 405

    def test_putorderbyidwrong(self):
        credentials = b64encode(b"Ostap:12")
        res = self.client.put("/order/asf", headers={"Authorization": f"Basic {credentials}"},
                              json={"order_user_id": 2, "order_item_id": 2, "quantity_in_order": 15})
        print(res.data)
        assert res.status_code == 404

    def test_putorderbywrongid(self):
        credentials = b64encode(b"Ostap:12")
        res = self.client.put("/order/5as", headers={"Authorization": f"Basic {credentials}"},
                              json={"order_user_id": 2, "order_item_id": 2, "quantity_in_order": 15})
        print(res.data)
        assert res.status_code == 404

    def test_putorder(self):
        credentials = b64encode(b"Ostap:12")
        res = self.client.put("/order/1", headers={"Authorization": f"Basic {credentials}"},
                              json={"order_user_id": 2, "order_item_id": 2, "quantity_in_order": 15})
        print(res.data)
        assert res.status_code == 200

    def test_postprovisor(self):
        test = self.client.post("/provisor", json={"provisorname": "os", "provisorpass": "pass123223"})
        print(test.data)
        self.assertEqual(201, test.status_code)

    def test_postprovisorbad(self):
        test = self.client.post("/provisor", json={"proviso": "os", "proviso": "pass123223"})
        print(test.data)
        self.assertEqual(405, test.status_code)

    def test_getprovisorbyid(self):
        credentials = b64encode(b"Valodya:12")
        res = self.client.get("/provisor/1", headers={"Authorization": f"Basic {credentials}"})
        assert res.status_code == 200

    def test_getprovisorbywrongid(self):
        credentials = b64encode(b"Valodya:12")
        res = self.client.get("/provisor/5", headers={"Authorization": f"Basic {credentials}"})
        assert res.status_code == 404

    def test_putprovisorbyid(self):
        credentials = b64encode(b"Valodya:12")
        res = self.client.put("/provisor/1", headers={"Authorization": f"Basic {credentials}"}
                              , json={"provisorname": "os", "provisorpass": "pass123223"})
        assert res.status_code == 200

    def test_putprovisorbywrongid(self):
        credentials = b64encode(b"Valodya:12")
        res = self.client.put("/provisor/5", headers={"Authorization": f"Basic {credentials}"}
                              , json={"provisorname": "os", "provisorpass": "pass123223"})
        assert res.status_code == 404

    def test_deleteprovisorbyid(self):
        credentials = b64encode(b"Valodya:12")
        res = self.client.delete("/provisor/1", headers={"Authorization": f"Basic {credentials}"})
        assert res.status_code == 200

    def test_deleteprovisorbywrongid(self):
        credentials = b64encode(b"Valodya:12")
        res = self.client.delete("/provisor/5", headers={"Authorization": f"Basic {credentials}"})
        assert res.status_code == 404

    def test_additem(self):
        credentials = b64encode(b"Valodya:12")
        res = self.client.post("/provisor/add", headers={"Authorization": f"Basic {credentials}"},
                                 json={"name":"Sorbex123", "quantity":1000, "price":"200.05", "describe":"sosgrbex vid zhyvota"})
        assert res.status_code == 201

    def test_additembad(self):
        credentials = b64encode(b"Valodya:12")
        res = self.client.post("/provisor/add", headers={"Authorization": f"Basic {credentials}"},
                                 json={"name":"Sorbex123", "quantity":100, "price":25, "describe":"sosgrbex vid zhyvota"})
        assert res.status_code == 405

    def test_putitembyid(self):
        credentials = b64encode(b"Valodya:12")
        res = self.client.put("/provisor/items/1", headers={"Authorization": f"Basic {credentials}"},
                               json={"name": "Sorbex123", "quantity": 100, "price":"200.05",
                                     "describe": "sosgrbex vid zhyvota"})
        assert res.status_code == 200

    def test_putitembywrongid(self):
        credentials = b64encode(b"Valodya:12")
        res = self.client.put("/provisor/items/10", headers={"Authorization": f"Basic {credentials}"},
                               json={"name": "Sorbex123", "quantity": 100, "price":"200.05",
                                     "describe": "sosgrbex vid zhyvota"})
        assert res.status_code == 404

    def test_putitembywrongid(self):
        credentials = b64encode(b"Valodya:12")
        res = self.client.delete("/provisor/items/10", headers={"Authorization": f"Basic {credentials}"})
        assert res.status_code == 404

    def test_putitembywrongid(self):
        credentials = b64encode(b"Valodya:12")
        res = self.client.delete("/provisor/items/1", headers={"Authorization": f"Basic {credentials}"})
        assert res.status_code == 200

    def test_deleteorderbyidprovisor(self):
        credentials = b64encode(b"Valodya:12")
        res = self.client.delete("/provisor/order/1", headers={"Authorization": f"Basic {credentials}"})
        assert res.status_code == 200

    def test_deleteorderbyidwrongprovisor(self):
        credentials = b64encode(b"Valodya:12")
        res = self.client.delete("/provisor/order/1asd", headers={"Authorization": f"Basic {credentials}"})
        assert res.status_code == 404

    def test_putorderbyidwrongprovisor(self):
        credentials = b64encode(b"Valodya:12")
        res = self.client.put("/provisor/order/asf", headers={"Authorization": f"Basic {credentials}"},
                              json={"order_user_id": 2, "order_item_id": 2, "quantity_in_order": 15})
        print(res.data)
        assert res.status_code == 404

    def test_putorderbywrongidprovisor(self):
        credentials = b64encode(b"Valodya:12")
        res = self.client.put("/provisor/order/5as", headers={"Authorization": f"Basic {credentials}"},
                              json={"order_user_id": 2, "order_item_id": 2, "quantity_in_order": 15})
        print(res.data)
        assert res.status_code == 404

    def test_putorderprovisor(self):
        credentials = b64encode(b"Valodya:12")
        res = self.client.put("/provisor/order/1", headers={"Authorization": f"Basic {credentials}"},
                              json={"order_user_id": 2, "order_item_id": 2, "quantity_in_order": 15})
        print(res.data)
        assert res.status_code == 200