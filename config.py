from flask import Flask
from routes import main
from delete import scheduleDelete

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "123"
    app.config['DEBUG'] = True
    app.register_blueprint(main)
    scheduleDelete('static', 8) #delete every 1 min | comment to stop tests
    return app


if __name__=="__main__":
    app = create_app()
    app.run()

