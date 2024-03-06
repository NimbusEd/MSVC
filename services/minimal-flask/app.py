import requests
from flask import jsonify, request
from apiflask import APIFlask, Schema
from apiflask.fields import Float, Integer, String


app = APIFlask(__name__)

class OpIn(Schema):
    a = Float(required = True)
    b = Float(required = True)


@app.route("/calc/<op>")
@app.input(OpIn, location='query')
def calc(op, query_data):
    a = request.args.get("a", type=float)
    b = request.args.get("b", type=float)

    if a is None or b is None:
        return jsonify({"error": "Invalid parameters"})
    if op == "add":
        result = a + b
    elif op == "sub":
        result = a - b
    elif op == "mul":
        result = a * b
    elif op == "div":
        result = a / b
    else:
        return jsonify({"error": "Invalid operation"})
    return jsonify({"result": result})

class AmountIn(Schema):
    amount = Float(required = True)

@app.route("/bitcoin/<currency>")
@app.input(AmountIn, location='query')
def bitcoin(currency, query_data):
    amount = query_data["amount"]

    if amount is None:
        return jsonify({"error": "Invalid parameter"})
    response = requests.get(f"https://api.coindesk.com/v1/bpi/currentprice.json")
    if response.status_code == 200:
        rate = response.json()["bpi"][currency]["rate_float"]
        result = amount / rate
        return jsonify({"result": result})
    else:
        return jsonify({"error": "Conversion failed"})

if __name__ == "__main__":
    app.run(debug=True)
