from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from graphene import ObjectType, String, Int, List, Schema, Field, Mutation,Boolean


class Planta(ObjectType):
    id = Int()
    nombre = String()
    especie = String()
    edad = Int()
    altura = Int()
    frutos = Boolean()


class Query(ObjectType):
    plantas = List(Planta)
    planta_por_especie = Field(Planta, especie=String())
    planta_por_altura=List(Planta, altura=String())
    planta_por_fruto=List(Planta, frutos=Boolean())
    def resolve_plantas(root, info):
        return plantas
    
    def resolve_planta_por_especie(root, info, especie):
        for planta in plantas:
            if planta.especie == especie:
                return planta
        return None
    def resolve_planta_por_altura(root, info, altura):
        plantas_filtradas=[planta for planta in plantas if planta.altura==altura]
        return plantas_filtradas
    
    def resolve_planta_por_fruto(root, info, frutos):
        plantas_filtradas=[planta for planta in plantas if planta.frutos==frutos]
        
        return plantas_filtradas
    
    
class CrearPlanta(Mutation):
    class Arguments:
        nombre = String()
        especie = String()
        edad = Int()
        altura = Int()
        frutos = Boolean()

    planta = Field(Planta)

    def mutate(root, info, nombre, especie, edad,altura, frutos):
        nuevo_planta = Planta(
            id=len(plantas) + 1, 
            nombre=nombre, 
            especie=especie, 
            edad=edad,
            altura=altura,
            frutos=frutos,
        )
        plantas.append(nuevo_planta)
    
        return CrearPlanta(planta=nuevo_planta)

class ActualizarPlanta(Mutation):
    class Arguments:
        id = Int()
        edad=Int()
        altura=Int()
    planta = Field(Planta)
    
    def mutate(root, info, id,edad,altura):
        for planta in plantas:
            if planta.id == id:
                planta.edad=edad
                planta.altura=altura                
                return ActualizarPlanta(planta=planta)
        return None


class DeletePlanta(Mutation):
    class Arguments:
        id = Int()
    planta = Field(Planta)

    def mutate(root, info, id):
        for i, planta in enumerate(plantas):
            if planta.id == id:
                plantas.pop(i)
                return DeletePlanta(planta=planta)
        return None

class Mutations(ObjectType):
    crear_planta = CrearPlanta.Field()
    delete_planta = DeletePlanta.Field()

plantas = [
    Planta(id=1, nombre="Girasol", especie="Tulbalghia", edad=20, altura=30,frutos=True),
    Planta(id=2, nombre="Margarita", especie="Chlorophytum ", edad=25, altura=40,frutos=False),
    Planta(
        id=3, nombre="Rosa", especie="bonito", edad=30, altura=30,frutos=True),
    Planta(id=4, nombre="Coca", especie="Curativa ", edad=25, altura=40,frutos=False),
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
            print(data)
            result = schema.execute(data["query"])
            self.response_handler(200, result.data)
        else:
            self.response_handler(404, {"Error": "Ruta no ex0istente"})

    def do_DELETE(self):
        if self.path == "/graphql":
            content_length = int(self.headers["Content-Length"])
            data = self.rfile.read(content_length)
            data = json.loads(data.decode("utf-8"))
            print(data)
            result = schema.execute(data["query"])
            self.response_handler(200, result.data)
        else:
            self.response_handler(404, {"Error": "Ruta no existente"})

    
    def do_POST(self):
        if self.path == "/graphql":
            content_length = int(self.headers["Content-Length"])
            data = self.rfile.read(content_length)
            data = json.loads(data.decode("utf-8"))
            print(data)
            result = schema.execute(data["query"])
            self.response_handler(200, result.data)
        else:
            self.response_handler(404, {"Error": "Ruta no existente"})

    def do_PUT(self):
        if self.path == "/graphql":
            content_length = int(self.headers["Content-Length"])
            data = self.rfile.read(content_length)
            data = json.loads(data.decode("utf-8"))
            print(data)
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