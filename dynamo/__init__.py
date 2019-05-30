import os
from flask import Flask
from flask_restful import Api


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        # DATABASE=os.path.join(app.instance_path, 'flask')
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/')
    def hello_world():
        # return 'Hello World!'
        return 'Hello DynamoDB!'

    from . import scrap_book
    # app.register_blueprint(scrap_book.bp)

    Api(app).add_resource(scrap_book.Content, '/scrap_book')

    return app
