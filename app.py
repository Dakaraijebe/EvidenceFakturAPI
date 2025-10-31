from flask import Flask, jsonify, request
from datetime import datetime
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)

# Swagger UI
SWAGGER_URL = '/api'
API_URL = '/static/openapi.yaml'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={'app_name': "Firemni evidence faktur API"}
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

# "Databaze"
invoices = []
next_id = 1


@app.route('/')
def root():
    return jsonify({"message": "Pouzij endpoint /invoices"})


# GET /invoices – seznam vsech faktur
@app.route('/invoices', methods=['GET'])
def get_invoices():
    paid = request.args.get('paid')
    customer = request.args.get('customer')
    result = invoices

    if paid is not None:
        if paid.lower() == "true":
            result = [i for i in result if i["paid"]]
        elif paid.lower() == "false":
            result = [i for i in result if not i["paid"]]

    if customer:
        result = [i for i in result if customer.lower() in i["customer"].lower()]

    return jsonify(result)


# GET /invoices/<id> – detail faktury
@app.route('/invoices/<int:invoice_id>', methods=['GET'])
def get_invoice(invoice_id):
    for i in invoices:
        if i["id"] == invoice_id:
            return jsonify(i)
    return jsonify({"error": "Invoice not found"}), 404


# POST /invoices – vytvoreni nove faktury
@app.route('/invoices', methods=['POST'])
def add_invoice():
    global next_id
    data = request.get_json()

    required_fields = ["number", "issueDate", "dueDate", "customer", "total", "vat"]
    if not data or not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        datetime.strptime(data["issueDate"], "%Y-%m-%d")
        datetime.strptime(data["dueDate"], "%Y-%m-%d")
    except ValueError:
        return jsonify({"error": "Invalid date format, expected YYYY-MM-DD"}), 400

    invoice = {
        "id": next_id,
        "number": data["number"],
        "issueDate": data["issueDate"],
        "dueDate": data["dueDate"],
        "customer": data["customer"],
        "supplier": data.get("supplier", "MyCompany s.r.o."),
        "description": data.get("description", ""),
        "total": float(data["total"]),
        "vat": float(data["vat"]),
        "paid": data.get("paid", False),
        "paymentDate": data.get("paymentDate")
    }

    next_id += 1
    invoices.append(invoice)
    return jsonify(invoice), 201


# DELETE /invoices/<id> – smazani faktury
@app.route('/invoices/<int:invoice_id>', methods=['DELETE'])
def delete_invoice(invoice_id):
    global invoices
    for i in invoices:
        if i["id"] == invoice_id:
            invoices = [x for x in invoices if x["id"] != invoice_id]
            return "", 204
    return jsonify({"error": "Invoice not found"}), 404


# GET /reports/unpaid – nezaplacene faktury
@app.route('/reports/unpaid', methods=['GET'])
def report_unpaid():
    unpaid = [i for i in invoices if not i["paid"]]
    return jsonify(unpaid)


# GET /reports/debtors – top dluznici podle objemu
@app.route('/reports/debtors', methods=['GET'])
def report_debtors():
    debtors = {}
    for i in invoices:
        if not i["paid"]:
            debtors[i["customer"]] = debtors.get(i["customer"], 0) + i["total"]
    result = [{"customer": k, "totalDebt": v} for k, v in sorted(debtors.items(), key=lambda x: x[1], reverse=True)]
    return jsonify(result)


# GET /reports/statistics – prumerna doba uhrady + soucty
@app.route('/reports/statistics', methods=['GET'])
def report_statistics():
    paid_invoices = [i for i in invoices if i["paid"] and i.get("paymentDate")]
    total_sum = sum(i["total"] for i in invoices)
    paid_sum = sum(i["total"] for i in paid_invoices)

    # Vypocet prumerne doby uhrady (v dnech)
    total_days = 0
    for i in paid_invoices:
        try:
            issue = datetime.strptime(i["issueDate"], "%Y-%m-%d")
            payment = datetime.strptime(i["paymentDate"], "%Y-%m-%d")
            total_days += (payment - issue).days
        except ValueError:
            pass

    avg_days = total_days / len(paid_invoices) if paid_invoices else 0

    stats = {
        "totalInvoices": len(invoices),
        "paidInvoices": len(paid_invoices),
        "totalAmount": total_sum,
        "paidAmount": paid_sum,
        "averagePaymentDays": round(avg_days, 2)
    }

    return jsonify(stats)

@app.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    if data.get("username") == "admin" and data.get("password") == "admin":
        return jsonify({"token": "demo-jwt-token"})
    return jsonify({"code": "UNAUTHORIZED", "message": "Invalid credentials"}), 401


if __name__ == '__main__':
    app.run(debug=True, port=5000)
