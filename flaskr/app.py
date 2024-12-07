from flask import Flask
from flask_restful import Api
from .modelos.modelos import db, Usuario
from flask_migrate import Migrate  # Aquí se importa la clase Migrate
from werkzeug.security import generate_password_hash

# Crear una instancia de Migrate
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    
    # Configuración de la base de datos
    USER_DB = 'root'
    PASS_DB = ''
    URL_DB = 'localhost'
    NAME_DB = 'bdnoticias'
    FULL_URL_DB = f'mysql+pymysql://{USER_DB}:{PASS_DB}@{URL_DB}/{NAME_DB}'

    app.config['SQLALCHEMY_DATABASE_URI'] = FULL_URL_DB
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'super-secret'

    # Inicialización de las extensiones
    db.init_app(app)
    migrate.init_app(app, db)  # Se usa la instancia 'migrate', no la clase

    # Importar vistas aquí para evitar importaciones circulares
    from .vistas import VistaSignIn, VistaLogIn, VistaNoticia, VistaComentario, VistaCalificacion

    api = Api(app)
    api.add_resource(VistaSignIn, '/registro')
    api.add_resource(VistaLogIn, '/login')
    api.add_resource(VistaNoticia, '/noticias')
    api.add_resource(VistaComentario, '/noticias/<int:id_noticia>/comentarios')
    api.add_resource(VistaCalificacion, '/noticias/<int:id_noticia>/calificacion')
def crear_superadmin():
    # Crea el rol y usuario Admin si no existen

    admin = Usuario.query.filter_by(correo="admin@example.com").first()
    if not admin:
        admin = Usuario(
            nombre="Admin",
            correo="admin@example.com",
            contrasena=generate_password_hash("admin123"),
        )
        db.session.add(admin)
        db.session.commit()
    return app
