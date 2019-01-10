import os

from flask import stream_with_context, Response, Flask

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    PATH = os.path.abspath(os.path.dirname(__file__))
    PATH = os.path.join(PATH, 'resources', 'test.mp4')

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
        return 'Hello, World! test123'
        
    @app.route('/stream_data')
    def stream_data():
        def generate():
            with open(PATH, "rb") as f:
                byte = f.read(512)
                while byte:
                    yield byte
                    byte = f.read(512)
    
        t = os.stat(PATH)
        sz = str(t.st_size)
        return
    
    Response(generate(),mimetype='video/mp4',headers={"Content-Type":"video/mp4","Content-Disposition":"inline","Content-Transfer-Enconding":"binary","Content-Length":sz})

    app.run(port=50000, debug=True, threaded=True)

create_app()