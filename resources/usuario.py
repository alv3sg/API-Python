from blacklist import BLACKLIST
from flask_restful import Resource, Api, reqparse
from models.usuario import UserModel
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
# from werkzeug.security import safe_str_cmp
from secrets import compare_digest


atributos = reqparse.RequestParser()
atributos.add_argument('login', type=str, required=True, help='The fied login cannot blanked')
atributos.add_argument('senha', type=str, required=True, help='The fied senha cannot blanked')
# Criando uma classe que herda alguns metodos da classe Resource
class User(Resource):
      
    def get(self, user_id):  
    #retornar um usuario 
        usuario = UserModel.find_user(user_id)
        if usuario:
            return usuario.json()   
        return {'message': 'usuario not found'}, 404
    
    @jwt_required()
    def delete(self, user_id):
        usuario = UserModel.find_user( user_id)
        if usuario:
            try:
                usuario.delete_user()
            except:
                return {'message' : 'An internal error ocurred trying to delete usuario'}, 500
            return {'message': 'usuario deleted'}, 200
        return {'message' : 'usuario not found'}, 404
    
class UserRegister(Resource):
    def post(self):
        dados = atributos.parse_args()

        if UserModel.find_by_login(dados['login']):
            return{'message' : ' The login already exists'}
        user = UserModel(**dados)
        user.save_user()
        return  {'message': 'User created success'}, 201
    
class UserLogin(Resource):
    @classmethod
    def post(cls):
        dados = atributos.parse_args()
        
        user = UserModel.find_by_login(dados['login'])

        if user and compare_digest(user.senha, dados['senha']):
            token_de_acesso = create_access_token(identity=user.user_id)
            return {'acess_token': token_de_acesso}, 200
        return {'message': 'The username or password is incorrect'}, 401
    
class UserLogout(Resource):
    @jwt_required()
    def post(self):
        jwt_id = get_jwt()['jti']
        BLACKLIST.add(jwt_id)
        return {'message': 'Logged out successfully'}, 200