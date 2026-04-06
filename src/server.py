import eventlet
eventlet.monkey_patch()

from flask import Flask, render_template
from flask_cors import CORS
from flask_socketio import SocketIO
from config import current_config
from werkzeug.middleware.proxy_fix import ProxyFix

from routers import RouterUsers, RouterEmail, RouterSat, RouterCompany

app = Flask(__name__)
CORS(app)
app.config.from_object(current_config)
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

socketio = SocketIO(
    app,
    cors_allowed_origins="*",
    async_mode="eventlet",
    logger=False,
    engineio_logger=False
)

@app.route("/")
def homepage():
    return render_template("public/index.html")

def page_not_found(error):
    return "<h1>Not Found Page</h1>", 404

# Registrar blueprints SIEMPRE, no dentro de __main__
app.register_blueprint(RouterUsers.main, url_prefix='/api/usuarios')
app.register_blueprint(RouterEmail.main, url_prefix='/api/servidor_correo')
app.register_blueprint(RouterSat.main, url_prefix='/api/sat')
app.register_blueprint(RouterCompany.main, url_prefix='/api/companias')

app.register_error_handler(404, page_not_found)

if __name__ == '__main__':
    debug_mode = str(current_config.DEBUG).lower() in ["true", "1", "yes"]

    socketio.run(
        app,
        host='0.0.0.0',
        port=current_config.PORT,
        debug=debug_mode,
        allow_unsafe_werkzeug=True
    )