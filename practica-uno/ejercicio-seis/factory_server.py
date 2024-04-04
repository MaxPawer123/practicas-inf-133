from http.server import HTTPServer, BaseHTTPRequestHandler
import json

# Base de datos simulada de vehículos
animales = {}


class ZoologicoAnimal:
    def __init__(self, nombre, especie,genero,edad, peso):
        self.nombre = nombre
        self.especie = especie
        self.genero = genero
        self.edad = edad
        self.peso = peso


class Mamifero(ZoologicoAnimal):
    def __init__(self,  nombre,genero,edad, peso):
        super().__init__("mamifero",nombre,genero,edad, peso)


class Ave(ZoologicoAnimal):
    def __init__(self, nombre,genero,edad, peso):
        super().__init__("ave", nombre,genero,edad, peso)

class Reptil(ZoologicoAnimal):
    def __init__(self, nombre,genero,edad, peso):
        super().__init__("reptil", nombre,genero,edad, peso)

class Anfibio(ZoologicoAnimal):
    def __init__(self, nombre, genero,edad, peso):
        super().__init__("anfibio", nombre,genero,edad, peso)

class Pez(ZoologicoAnimal):
    def __init__(self, nombre, genero,edad, peso):
        super().__init__("pez", nombre,genero,edad, peso)


class ZoologicoFactory:
    @staticmethod
    def create_animal(nombre, especie,genero,edad, peso):
        if especie == "mamifero":
            return Mamifero( nombre,genero,edad, peso)
        elif especie == "ave":
            return Ave( nombre,genero,edad, peso)
        elif especie == "reptil":
            return Reptil( nombre,genero,edad, peso)
        elif especie == "anfibio":
            return Anfibio( nombre,genero,edad, peso)
        elif especie == "pez":
            return Pez(nombre,genero,edad, peso)
        
        else:
            raise ValueError("Tipo de vehículo de entrega no válido")


class HTTPDataHandler:
    @staticmethod
    def handle_response(handler, status, data):
        handler.send_response(status)
        handler.send_header("Content-type", "application/json")
        handler.end_headers()
        handler.wfile.write(json.dumps(data).encode("utf-8"))

    @staticmethod
    def handle_reader(handler):
        content_length = int(handler.headers["Content-Length"])
        post_data = handler.rfile.read(content_length)
        return json.loads(post_data.decode("utf-8"))


class ZoologicoService:
    def __init__(self):
        self.factory = ZoologicoFactory()

    def add_animal(self, data):
        nombre = data.get("nombre", None)
        especie = data.get("especie", None)
        genero = data.get("genero", None)
        edad = data.get("edad", None)
        peso = data.get("peso", None)
        
        zoologico_animal = self.factory.create_animal(
            nombre, especie,genero,edad, peso
        )
        animales[len(animales) + 1] = zoologico_animal
        return zoologico_animal

    def list_animales(self):
        return {index: animal.__dict__ for index, animal in animales.items()}

    def update_animal(self, animal_id, data):
        if animal_id in animales:
            animal = animales[animal_id]
            nombre = data.get("nombre", None)
            genero = data.get("genero", None)
            edad = data.get("edad", None)
            peso = data.get("peso", None)

            if nombre:
                animal.nombre = nombre
            if genero:
                animal.genero = genero
            if edad:
                animal.edad =edad
            if peso:
                animal.peso = peso
            
            return animal
        else:
            raise None
        
  #recibimos un nombre un delete
    def delete_animal(self, animal_id):
        if animal_id in animales:
            del animales[animal_id]
            return {"message": "Animal eliminado"}
        else:
            return None


class ZoologicoRequestHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.zoologico_service = ZoologicoService()
        super().__init__(*args, **kwargs)

    def do_POST(self):
        if self.path == "/zoologicos":
            data = HTTPDataHandler.handle_reader(self)
            response_data = self.zoologico_service.add_animal(data)
            HTTPDataHandler.handle_response(self, 201, response_data.__dict__)
        else:
            HTTPDataHandler.handle_response(
                self, 404, {"message": "Ruta no encontrada"}
            )

    def do_GET(self):
        if self.path == "/zoologicos":
            response_data = self.zoologico_service.list_animales()
            HTTPDataHandler.handle_response(self, 200, response_data)
        else:
            HTTPDataHandler.handle_response(
                self, 404, {"message": "Ruta no encontrada"}
            )

    def do_PUT(self):
        if self.path.startswith("/zoologicos/"):
            animal_id = int(self.path.split("/")[-1])
            data = HTTPDataHandler.handle_reader(self)
            response_data = self.zoologico_service.update_animal(animal_id, data)
            if response_data:
                HTTPDataHandler.handle_response(self, 200, response_data.__dict__)
            else:
                HTTPDataHandler.handle_response(
                    self, 404, {"message": "Animal no encontrado"}
                )
        else:
            HTTPDataHandler.handle_response(
                self, 404, {"message": "Ruta no encontrada"}
            )

    def do_DELETE(self):
        if self.path.startswith("/zoologicos/"):
            animal_id = int(self.path.split("/")[-1])
            response_data = self.zoologico_service.delete_animal(animal_id)
            if response_data:
                HTTPDataHandler.handle_response(self, 200, response_data)
            else:
                HTTPDataHandler.handle_response(
                    self, 404, {"message": "Animal no encontrado"}
                )
        else:
            HTTPDataHandler.handle_response(
                self, 404, {"message": "Ruta no encontrada"}
            )


def main():
    try:
        server_address = ("", 8000)
        httpd = HTTPServer(server_address, ZoologicoRequestHandler)
        print("Iniciando servidor HTTP en puerto 8000...")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Apagando servidor HTTP")
        httpd.socket.close()
        

if __name__ == "__main__":
    main()
    
    
    
    
          