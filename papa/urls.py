from flask import request, jsonify, abort
from marshmallow.utils import EXCLUDE
from papasha import session, app, bcrypt
from papa.models import UserSchema, User, Item, ItemSchema, Order, OrderSchema,Order_DemandSchema
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(username, password):
    user = session.query(User).filter(User.username == username).first()
    if user is None:
        return False
    else:
        return bcrypt.check_password_hash(user.password, password)


def g404(cls, pk):
    obj = session.query(cls).get(pk)
    if obj is None:
        raise Exception
    return obj


@app.route("/user", methods=["POST"])
def user_add():
    data = request.get_json()
    try:
        data['password'] = bcrypt.generate_password_hash(
            data['password']).decode('utf-8')
        user = UserSchema(partial=True).load(data, unknown=EXCLUDE)
    except Exception:
        return jsonify({'message': "Invalid input"}), 405


    session.add(user)
    session.commit()
    return jsonify({'message': "Success"}), 201


@app.route("/user/<int:pk>", methods=['PUT'])
@auth.login_required()
def update_user(pk):
    data = request.get_json()
    s = "password"
    if s in data:
        data["password"] = bcrypt.generate_password_hash(data["password"]).decode('utf-8')
    try:
        user = g404(User, pk)
    except Exception:
        return jsonify({'message': "User not found"}), 404

    session.query(User).filter(
            User.user_id == pk).update(data)
    session.commit()
    return jsonify({'message': "Success"}), 200


@app.route("/user/<int:pk>", methods=['DELETE'])
@auth.login_required()
def delete_user(pk):
    try:
        user = g404(User, pk)
    except Exception:
        return jsonify({'message': "User not found"}), 404

    session.delete(user)
    session.commit()
    return jsonify({'message': "Success"}), 200


@app.route("/user/<int:pk>", methods=["GET"])
def user_get(pk):
    try:
        user = g404(User, pk)
    except Exception:
        return jsonify({'message': "User not found"}), 404

    return jsonify(UserSchema().dump(user))


@app.route("/items/<int:pk>", methods=["GET"])
@auth.login_required()
def item_get(pk):
    try:
        item = g404(Item, pk)
    except Exception:
        return jsonify({'message': "Item not found"}), 404

    return jsonify(ItemSchema().dump(item))


@app.route("/items", methods=["GET"])
@auth.login_required()
def item_get_all():
    items = session.query(Item).all()

    return jsonify(ItemSchema(many=True).dump(items))


@app.route("/order", methods=['POST'])
@auth.login_required()
def order_add():
    data = request.get_json()
    try:
        order = OrderSchema(partial=True).load(data, unknown=EXCLUDE)
    except Exception:
        return jsonify({'message': "Invalid input"}), 405

    session.add(order)
    session.commit()
    return jsonify({'message': "Success"}), 201


@app.route("/order/<int:pk>", methods=["GET"])
def order_get(pk):
    try:
        order = g404(Order, pk)
    except Exception:
        return jsonify({'message': "Item not found"}), 404

    return jsonify(OrderSchema().dump(order))


@app.route("/order/<int:pk>", methods=['PUT'])
@auth.login_required()
def order_update(pk):
    data = request.get_json()
    try:
        order = g404(Order, pk)
    except Exception:
        return jsonify({'message': "Order not found"}), 404

    session.query(Order).filter(Order.order_id == pk).update(data)
    session.commit()

    return jsonify({'message': "Success"}), 200


@app.route("/order/<int:pk>", methods=['DELETE'])
@auth.login_required()
def order_delete(pk):
    try:
        order = g404(Order, pk)
    except Exception:
        return jsonify({'message': "Order not found"}), 404

    session.delete(order)
    session.commit()
    return jsonify({'message': "Success"}), 200


@app.route("/order/special", methods=['POST'])
@auth.login_required()
def order_demand_add():
    data = request.get_json()
    try:
        order_demand = Order_DemandSchema(partial=True).load(data, unknown=EXCLUDE)
    except Exception:
        return jsonify({'message': "Invalid input"}), 405


    session.add(order_demand)
    session.commit()
    return jsonify({'message': "Success"}), 201