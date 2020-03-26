from flask import Flask
from flask_restful import Api
from resources.employee import employees
from resources.routes import initialize_routes

app = Flask(__name__)
api = Api(app)

app.register_blueprint(employees)

initialize_routes(api)


if __name__ == '__main__':
    app.run(debug=True)
