from blacklist import BLACKLIST
from flask import Flask, jsonify
from flask_restful import  Api
from flask_jwt_extended import JWTManager
from resources.hotel import Hoteis, Hotel
from resources.usuario import User, UserRegister, UserLogin, UserLogout

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'DontTellAnyone'
app.config['JWT_BLACKLIST_ENABLED'] = True
api = Api(app)
jwt = JWTManager(app)

initialized = False
@app.before_request
def cria_banco():
    global initialized
    print('cria_banco out :' , initialized)
    if not initialized:
        banco.create_all()
        initialized = True
        print('cria_banco inside', initialized)
@jwt.token_in_blocklist_loader
def veririfica_blacklist(self, token):
    return token['jti'] in BLACKLIST

@jwt.revoked_token_loader
def token_de_acess_invalidado(jwt_header, jwt_payload):
    return (
        jsonify({'message': 'You have been logged out.'}), 401
    )

# Adicionando o recurso e definindo a rota para acessar
api.add_resource(Hoteis, '/hoteis')
api.add_resource(Hotel, '/hoteis/<string:hotel_id>')
api.add_resource(User, '/usuarios/<int:user_id>')
api.add_resource(UserRegister, '/usuario')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')


# Comando para rodar o servidor
if __name__ == '__main__':
    from sql_alchemy import banco
    banco.init_app(app)
    app.run(debug=True)