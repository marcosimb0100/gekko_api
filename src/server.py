from flask import Flask, request, render_template
from flask_cors import CORS
from flask_socketio import SocketIO
from config import current_config
from werkzeug.middleware.proxy_fix import ProxyFix
# from helpers.socketHelper import register_socket_handlers

# Routes
from routers import ( 
                        RouterUsers
                        # usuariosRoute, usuariosAppRoute, biometricosRoute, perfilesRoute, contpaqRoute, horariosRoute, 
                        # supervisorRoute, gerenteRoute, correoRoute, empleadosSinVinculosRoute, permisosRoute, horariosPersonalExternoRoute,
                        # logsRoute, empleadosBiometricoRoute, fechaAltaRoute, diasInhabilesRoute
                    )

app = Flask(__name__)
CORS(app)
app.config.from_object(current_config)
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

socketio = SocketIO(
    app, 
    cors_allowed_origins="*",
    async_mode='eventlet',
    logger=False,
    engineio_logger=False
)

@app.route("/")
def homepage():
        return render_template("public/index.html")
    
def page_not_found(error):
    return "<h1>Not Found Page</h1>", 404

if __name__ == '__main__':
    
    # -------------------
    # Blueprint
    # -------------------
    app.register_blueprint(RouterUsers.main, url_prefix = '/api/usuarios')
    
    app.register_error_handler(404, page_not_found)
    
    debug_mode = str(current_config.DEBUG).lower() in ["true", "1", "yes"]
    
    socketio.run(
        app,
        host='0.0.0.0',
        port=current_config.PORT,
        debug=debug_mode,
        allow_unsafe_werkzeug=True
    )