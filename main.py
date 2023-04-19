from config import app
from flask import jsonify, make_response, render_template
from flask_swagger import swagger
from routes import all_routes

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/swagger")
def api():
    swag = swagger(app, from_file_keyword="swagger_from_file")
    swag['info']['version'] = "1.0"
    swag['info']['title'] = "API"

    return jsonify(swag)


if __name__ == "__main__":
    app.run(debug=True)