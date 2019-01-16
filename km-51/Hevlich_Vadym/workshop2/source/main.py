from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


@app.route('/')
def index():
    return '<h1>Hello from Flask<h1>'


product_dictionary = {
    "price": 123,
    "name": "product name"
}

shop_dictionary = {
    "street": "street 12",
    "name": "Shop123"
}

available_dictionary = dict.fromkeys(['repo_dictionary', 'user_dictionary'], "dict_name")


@app.route('/api/<action>', methods=['GET'])
def apiGet(action):
    if action == "product":
        return render_template("product.html", product=product_dictionary)
    elif action == "shop":
        return render_template("shop.html", shop=shop_dictionary)
    elif action == "all":
        return render_template("all.html", product=product_dictionary, shop=shop_dictionary)
    else:
        return render_template("404.html", action_value=action, available=available_dictionary)


@app.route('/api', methods=['POST'])
def apiPost():
    if request.form["action"] == "product_update":
        product_dictionary["price"] = request.form["price"]
        product_dictionary["name"] = request.form["name"]

        return redirect(url_for('apiGet', action="all"))

    elif request.form["action"] == "shop_update":
        shop_dictionary["street"] = request.form["street"]
        shop_dictionary["name"] = request.form["name"]

        return redirect(url_for('apiGet', action="all"))


if __name__ == '__main__':
    app.run(debug=True)
