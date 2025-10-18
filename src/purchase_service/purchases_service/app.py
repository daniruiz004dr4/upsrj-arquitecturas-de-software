# ============================================================
# Politécnica de Santa Rosa
#
# Materia: Arquitecturas de Software
# Profesor: Jesús Salvador López Ortega
# Grupo: ISW28
# Archivo: app.py
# Descripción: Backend del microservicio
# ============================================================
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from flask import Flask, request, render_template, redirect, url_for
from common.utils import load_item, save_item, get_host
from common.vars import PURCHASES_FILE, PURCHASE_SERVICE_URL, USERS_FILE, PRODUCTS_FILE
from datetime import datetime

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
app = Flask(__name__, template_folder=template_dir)

@app.route('/purchases', methods=['GET'])
def get_purchases():
    purchases = load_item(PURCHASES_FILE)
    return render_template("purchases.html", purchases=purchases)

@app.route('/purchases/create', methods=['GET'])
def create_purchase_form():
    return render_template("create_purchase.html")

@app.route('/purchases', methods=['POST'])
def create_purchase():

    users = load_item(USERS_FILE)
    products = load_item(PRODUCTS_FILE)

    user_id = request.form.get("user_id")
    product_id = request.form.get("product_id")

    if user_id is None:
        try:
            user_id = request.get_json().get("user_id")
        except:
            user_id = None
        
    if product_id is None:
        try:
            product_id = request.get_json().get("product_id") 
        except:
            product_id = None

    print(user_id, product_id)

    if not user_id or user_id is None:
        return "user_id", 400
    if not product_id or product_id is None:
        return "product_id", 400
    current_timestamp = datetime.now().isoformat()
    
    purchases = load_item(PURCHASES_FILE)
    purchase = {
        'id': int(len(purchases) + 1), 
        'user_id': int(user_id), 
        'product_id': int(product_id),
        'timestamp': current_timestamp
    }
    purchases.append(purchase)
    save_item(PURCHASES_FILE, purchases)

    users = load_item(USERS_FILE)
    users[int(user_id) - 1]['purchased_products'].append(int(product_id))
    save_item(USERS_FILE, users)

    return redirect(url_for('get_purchases'))

@app.route('/purchases/<user_id>', methods=['GET'])
def get_purchases_by_user(user_id):
    purchases = load_item(PURCHASES_FILE)
    users = load_item(USERS_FILE)
    products = load_item(PRODUCTS_FILE)
    if int(user_id) not in [int(u["id"]) for u in users]:
        return "user_id", 400
    user_purchases = [p for p in purchases if str(p['user_id']) == str(user_id)]
    
    return render_template("purchases.html", purchases=user_purchases)

if __name__ == '__main__':
    app.run(port=get_host(PURCHASE_SERVICE_URL))