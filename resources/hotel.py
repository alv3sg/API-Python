from flask_restful import Resource, Api, reqparse
from models.hotel import HotelModel
from flask_jwt_extended import jwt_required

# Criando uma classe que herda alguns metodos da classe Resource
class Hoteis(Resource):    
    def get(self):
        return {'hoteis' : [hotel.json() for hotel in HotelModel.query.all()]}

class Hotel(Resource):
    # Argumentos vindos como request/parametros
    argumentos = reqparse.RequestParser()
    argumentos.add_argument('nome', type=str, required=True, help="The field 'name' cannot be left blank")
    argumentos.add_argument('estrelas')
    argumentos.add_argument('diaria')
    argumentos.add_argument('cidade')    
    
    def get(self, hotel_id):  
    #retornar um hotel 
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            return hotel.json()   
        return {'message': 'Hotel not found'}, 404
    
    @jwt_required()
    def post(self, hotel_id):
    # recebe um id como argumento, recebe dados como argumento, cria um novo hotel e adiciona os dados passados como argumento
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            return {'message': 'Hotel id already exists'}, 400        
        dados = Hotel.argumentos.parse_args()     
        # Criando uma nova instancia, passando os dados como argumento
        hotel = HotelModel(hotel_id, **dados)
        try:
            hotel.save_hotel()
        except:
            return {'message' : 'An internal error ocurred trying to save hotel'}, 500
        return hotel.json(), 200

    @jwt_required()
    def put(self, hotel_id):
        dados = Hotel.argumentos.parse_args()
        # Criando uma nova instancia, passando os dados como argumento

        hotel_encontrado = HotelModel.find_hotel(hotel_id)
        if hotel_encontrado:
            hotel_encontrado.update_hotel(**dados)
            hotel_encontrado.save_hotel()
            return hotel_encontrado.json(), 200
        
        hotel = HotelModel(hotel_id, **dados)
        try:
            hotel.save_hotel()
        except:
            return {'message' : 'An internal error ocurred trying to save hotel'}, 500
        return hotel.json(), 201
               
    @jwt_required()
    def delete(self, hotel_id):
        hotel = HotelModel.find_hotel( hotel_id)
        if hotel:
            try:
                hotel.delete_hotel()
            except:
                return {'message' : 'An internal error ocurred trying to delete hotel'}, 500
            return {'message': 'Hotel deleted'}, 200
        return {'message' : 'Hotel not found'}, 404