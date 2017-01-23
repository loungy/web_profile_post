import config
from flask import Flask
from webpage import web_page

import logging


def create_app(config, debug=False, testing=False, config_override=None):
    app = Flask(__name__)
    app.config.from_object(config)
    app.debug = debug
    app.testing = testing

    if config_override:
        app.config.update(config_override)

    if not app.testing:
        logging.basicConfig(level=logging.INFO)

    app.register_blueprint(web_page)

    return app


app = create_app(config)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, threaded=True, debug=True)
