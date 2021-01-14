from flask import request, jsonify
from marshmallow.utils import EXCLUDE
from papasha import session, app, bcrypt
from papa.models import ProvisorSchema, Provisor, Item, ItemSchema, Order
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(username, password):
    provisor = session.query(Provisor).filter(Provisor.provisorname == username).first()
    if provisor is None:
        return False
    else:
        return bcrypt.check_password_hash(provisor.provisorpass,password)



def g404(cls, pk):
    obj = session.query(cls).get(pk)
    if obj is None:
        raise Exception
    return obj


@app.route("/provisor", methods=["POST"])
def provisor_add():
    data = request.get_json()
    try:
        data['provisorpass'] = bcrypt.generate_password_hash(
            data['provisorpass']).decode('utf-8')
        provisor = ProvisorSchema(partial=True).load(data, unknown=EXCLUDE)
    except KeyError:
        return jsonify({'message': "Invalid input"}), 405
    session.add(provisor)
    session.commit()
    return jsonify({'message': "Success"}), 201


@app.route("/provisor/<int:pk>", methods=["GET"])
def provisor_get(pk):
    try:
        provisor = g404(Provisor, pk)
    except Exception:
        return jsonify({'message': "User not found"}), 404

    return jsonify(ProvisorSchema().dump(provisor))


@app.route("/provisor/<int:pk>", methods=['PUT'])
@auth.login_required()
def update_provisor(pk):
    data = request.get_json()
    if "provisorpass" in data:
        data["provisorpass"] = bcrypt.generate_password_hash(
            data['provisorpass']).decode('utf-8')
    try:
        provisor = g404(Provisor, pk)
    except Exception:
        return jsonify({'message': "Provisor not found"}), 404

    session.query(Provisor).filter(
            Provisor.provisor_id == pk).update(data)
    session.commit()
    return jsonify({'message': "Success"}), 200


@app.route("/provisor/<int:pk>", methods=['DELETE'])
@auth.login_required()
def delete_provisor(pk):
    try:
        provisor = g404(Provisor, pk)
    except Exception:
        return jsonify({'message': "Provisor not found"}), 404

    session.delete(provisor)
    session.commit()
    return jsonify({'message': "Success"}), 200


@app.route("/provisor/add", methods=['POST'])
@auth.login_required()
def item_add():
    data = request.get_json()
    try:
        item = ItemSchema(partial=True).load(data, unknown=EXCLUDE)
    except Exception:
        return jsonify({'message': "Invalid input"}), 405

    session.add(item)
    session.commit()
    return jsonify({'message': "Success"}), 201


@app.route("/provisor/items/<int:pk>", methods=['PUT'])
@auth.login_required()
def item_update(pk):
    data = request.get_json()
    try:
        item = g404(Item, pk)
    except Exception:
        return jsonify({'message': "Item not found"}), 404

    session.query(Item).filter(Item.item_id == pk).update(data)
    session.commit()

    return jsonify({'message': "Success"}), 200


@app.route("/provisor/items/<int:pk>", methods=['DELETE'])
@auth.login_required()
def item_delete(pk):
    try:
        place = g404(Item, pk)
    except Exception:
        return jsonify({'message': "Item not found"}), 404

    session.delete(place)
    session.commit()
    return jsonify({'message': "Success"}), 200


@app.route("/provisor/order/<int:pk>", methods=['PUT'])
@auth.login_required()
def provisor_order_update(pk):
    data = request.get_json()
    try:
        order = g404(Order, pk)
    except Exception:
        return jsonify({'message': "Order not found"}), 404

    session.query(Order).filter(Order.order_id == pk).update(data)
    session.commit()

    return jsonify({'message': "Success"}), 200


@app.route("/provisor/order/<int:pk>", methods=['DELETE'])
@auth.login_required()
def proviser_order_delete(pk):
    try:
        order = g404(Order, pk)
    except Exception:
        return jsonify({'message': "Order not found"}), 404

    session.delete(order)
    session.commit()
    return jsonify({'message': "Success"}), 200