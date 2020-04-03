from flask import Flask
from flask_restful import Api
from flask_bcrypt import Bcrypt
from resources.routes import initialize_routes
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config.from_envvar('ENV_FILE_LOCATION')
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost:3306/employee'
#app.config['SQLALCHEMY_ECHO'] = True
#db = SQLAlchemy(app)

bcrypt = Bcrypt(app)
jwt = JWTManager(app)

initialize_routes(api)


if __name__ == '__main__':
    app.run(debug=True)
