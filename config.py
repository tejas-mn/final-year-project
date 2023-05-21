from flask import Flask
# from flask_cors import CORS,cross_origin
from routes import main
from delete import scheduleDelete

def create_app():
    app = Flask(__name__)
    # cors = CORS(app)
    app.config["SECRET_KEY"] = "123"
    app.register_blueprint(main)

    # scheduleDelete('static', 2) #delete every 1 min | comment to stop tests

    return app


if __name__=="__main__":
    app = create_app()
    app.run()

