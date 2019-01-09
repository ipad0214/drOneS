import os

from flask import stream_with_context, Response, Flask

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'
        
    @app.route('/stream_data')
    def stream_data():
        with open('/resources/test.mp4') as f:
            while True:
                chunk = ...
                yield chunk
                
        return Response(stream_with_context(generate()), mimetype("video/mp4"))

    app.run(port=50000, debug=True)

create_app()