from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from ..modelos.modelos import db, Usuario, Noticia, Comentario, Calificacion
from sqlalchemy.exc import IntegrityError

class VistaSignIn(Resource):
    def post(self):
        data = request.get_json()
        nombre = data.get('nombre')
        correo = data.get('correo')
        contraseña = data.get('contraseña')
        rol = data.get('rol')

        if Usuario.query.filter_by(correo=correo).first():
            return {"message": "El correo ya está registrado."}, 400
        
        try:
            usuario = Usuario(nombre=nombre, correo=correo, rol=rol)
            usuario.set_password(contraseña)
            db.session.add(usuario)
            db.session.commit()
            return {"message": "Usuario registrado exitosamente."}, 201
        except IntegrityError:
            db.session.rollback()
            return {"message": "Error al registrar el usuario."}, 500

class VistaLogIn(Resource):
    def post(self):
        data = request.get_json()
        correo = data.get('correo')
        contraseña = data.get('contraseña')

        usuario = Usuario.query.filter_by(correo=correo).first()
        if usuario and usuario.check_password(contraseña):
            return {"message": "Inicio de sesión exitoso."}, 200
        return {"message": "Credenciales inválidas."}, 401

class VistaNoticia(Resource):
    def get(self):
        noticias = Noticia.query.all()
        return [{"id": noticia.id, "titulo": noticia.titulo} for noticia in noticias]

class VistaComentario(Resource):
    @jwt_required()
    def post(self, id_noticia):
        data = request.get_json()
        contenido = data.get('contenido')

        noticia = Noticia.query.get_or_404(id_noticia)
        comentario = Comentario(contenido=contenido, noticia_id=noticia.id, usuario_id=1)  # Usar ID del usuario autenticado
        db.session.add(comentario)
        db.session.commit()
        return {"message": "Comentario añadido."}, 201

    def get(self, id_noticia):
        comentarios = Comentario.query.filter_by(noticia_id=id_noticia).all()
        return [{"id": comentario.id, "contenido": comentario.contenido} for comentario in comentarios]

class VistaCalificacion(Resource):
    @jwt_required()
    def post(self, id_noticia):
        data = request.get_json()
        valor = data.get('valor')

        if valor < 1 or valor > 5:
            return {"message": "La calificación debe estar entre 1 y 5."}, 400
        
        noticia = Noticia.query.get_or_404(id_noticia)
        calificacion = Calificacion(valor=valor, noticia_id=noticia.id, usuario_id=1)  # Usar ID del usuario autenticado
        db.session.add(calificacion)
        db.session.commit()
        return {"message": "Calificación añadida."}, 201
