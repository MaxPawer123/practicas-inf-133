from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from graphene import ObjectType, String, Int, Boolean, List, Schema, Field, Mutation

class Planta(ObjectType):
    id = Int()
    nombre_comun = String()
    especie = String()
    edad = Int() 
    altura = Int()
    frutos = Boolean()

class Query(ObjectType):
    
    plantas = List(Planta)
    plantas_por_especie = List(Planta, especie = String())
    plantas_por_frutos = List(Planta, frutos = Boolean())
    
    #Listar todas las plantas
    def resolve_plantas(root, info):
        return plantas
    
    #Buscar plantas por especie
    def resolve_plantas_por_especie(root, info, especie):
        plantas_especie = list(planta for planta in plantas if planta.especie == especie)
        return plantas_especie
    
    #Buscar las plantas que tienen frutos
    def resolve_plantas_por_frutos(root, info, frutos):
        plantas_frutos = list(planta for planta in plantas if planta.frutos == frutos)
        return plantas_frutos
    
#Crear una planta
class CreatePlanta(Mutation):
    class Arguments:
        nombre_comun = String()
        especie = String()
        edad = Int() 
        altura = Int()
        frutos = Boolean()
    
    planta = Field(Planta)
    
    def mutate(root, info, nombre_comun, especie, edad, altura, frutos):
        nueva_planta = Planta(
            id = len(plantas)+1,
            nombre_comun = nombre_comun,
            especie = especie,
            edad = edad, 
            altura = altura,
            frutos = frutos
        )
        plantas.append(nueva_planta)
        
        return CreatePlanta(planta = nueva_planta)

#Actualizar la información de una planta
class UpdatePlanta(Mutation):
    class Arguments:
        id = Int()
        edad = Int()
        altura = Int()
    
    planta = Field(Planta)
    
    def mutate(root, info, id, edad, altura):
        for planta in plantas:
            if planta.id == id:
                planta.edad = edad
                planta.altura = altura
                return UpdatePlanta(planta = planta)
        return None   
    
#Eliminar una planta
class DeletePlanta(Mutation):
    class Arguments:
        id = Int()
        
    planta = Field(Planta)
    
    def mutate(root, info, id):
        for i, planta in enumerate(plantas):
            if planta.id == id:
                plantas.pop(i)
                return DeletePlanta(planta = planta)
        return None

class Mutations(ObjectType):
    create_planta = CreatePlanta.Field()
    update_planta = UpdatePlanta.Field()
    delete_planta = DeletePlanta.Field()
    
plantas = [
    Planta(
        id=1,
        nombre_comun='Durazno',
        especie='Malus domestica',
        edad=3,
        altura=50,
        frutos=True
    ),
    Planta(
        id=2,
        nombre_comun='Pera',
        especie='Pinus',
        edad=30,
        altura=00,
        frutos=False
    )
]

schema = Schema(query=Query, mutation=Mutations)
    
class GraphQLRequestHandler(BaseHTTPRequestHandler):
    
    def response_handler(self, status, data):
        self.send_response(status)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode("utf-8"))
        
    def do_GET(self):
        if self.path == "/graphql":            
            content_length = int(self.headers["Content-Length"])
            data = self.rfile.read(content_length)
            data = json.loads(data.decode("utf-8"))
            result = schema.execute(data["query"])
            self.response_handler(200, result.data)
        else:
            self.response_handler(404, {"Error": "Ruta no existente"})
    
    def do_POST(self):
        if self.path == "/graphql":
            content_length = int(self.headers["Content-Length"])
            data = self.rfile.read(content_length)
            data = json.loads(data.decode("utf-8"))
            result = schema.execute(data["query"])
            self.response_handler(200, result.data)
        else:
            self.response_handler(404, {"Error": "Ruta no existente"})

def run_server(port=8000):
    try:
        server_address = ("", port)
        httpd = HTTPServer(server_address, GraphQLRequestHandler)
        print(f"Iniciando servidor web en http://localhost:{port}/")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Apagando servidor web")
        httpd.socket.close()

if __name__ == "__main__":
    run_server()