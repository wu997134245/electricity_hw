from flask import Flask,session
from mods.user import user
from mods.product import product
from mods.shopping_cart import cart
from flask_cors import CORS


app = Flask(__name__,template_folder="views",static_url_path='', static_folder='')
CORS(app)

app.register_blueprint(user)
app.register_blueprint(product)
app.register_blueprint(cart)

app.config["SECRET_KEY"] = "test"




if __name__ == '__main__':
    app.run(debug=True, port=4000, host="0.0.0.0", threaded=True)


