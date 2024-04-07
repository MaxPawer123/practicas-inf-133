from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from urllib import parse as urlparse


animales = {
    1:{
        
        "nombre": "Leon",
        "especie": "Carnivoro",
        "genero": "macho",
        "edad": 15,
        "peso": 3
    },
    2: {
      
        "nombre": "Foca",
        "especie": "Mamifero",
        "genero": "hembra",
        "edad": 6,
        "peso": 2
    },
    3:{
        
        "nombre": "perro",
        "especie": "domestico",
        "genero": "hembra ",
        "edad": 2,
        "peso": 3
    },
}

class HTTPResponseHandler:
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
    
class AnimalService:
    @staticmethod
    def buscar_animales_especie(especie):
        return {id_animal: animal for id_animal, animal in animales.items() if animal["especie"] == especie}
    
    @staticmethod
    def buscar_animales_genero(genero):
        return {id_animal: animal for id_animal, animal in animales.items() if animal["genero"] == genero}    

    @staticmethod
    def add_animal(data):
        id_animal_nuevo = max(animales.keys()) + 1 if animales else 1
        animales[id_animal_nuevo] = data
        print("Animal añadido con ID", id_animal_nuevo)
        return animales
    
    @staticmethod
    def update_animal(id_animal, data):         
        if id_animal in animales:
            animales[id_animal].update(data)
            print("Datos actualizados para el animal con ID", id_animal)
            return animales
        return None
    
    @staticmethod
    def delete_animal(id_animal):
        if id_animal in animales:
            animales.pop(id_animal)
            print("Animal con ID", id_animal, "eliminado")
            return animales
        return None
        
class RESTRequestHandler(BaseHTTPRequestHandler):
            
    def do_GET(self):
        parsed_path = urlparse.urlparse(self.path)
        query_params = urlparse.parse_qs(parsed_path.query)
    
        #Listar todos los animales
        if parsed_path.path == "/animales":
            HTTPResponseHandler.handle_response(self, 200, animales)        
        
        #Buscar animales por especie
        elif self.path.startswith("/animales") and "especie" in query_params:
            especie = query_params["especie"][0]
            animales_especie = AnimalService.buscar_animales_especie(especie)
            if animales_especie:
                HTTPResponseHandler.handle_response(self, 200, animales_especie)
            else:
                HTTPResponseHandler.handle_response(self,204,{})
        
        #Buscar animales por género    
        elif self.path.startswith("/animales") and "genero" in query_params:
            genero = query_params["genero"][0]
            animales_genero = AnimalService.buscar_animales_genero(genero)
            if animales_genero:
                HTTPResponseHandler.handle_response(self, 200, animales_genero)
            else:
                HTTPResponseHandler.handle_response(self,204,{})
    
    def read_data(self):
        content_length = int(self.headers["Content-Length"])
        data = self.rfile.read(content_length)
        data = json.loads(data.decode("utf-8"))
        return data
    
    def do_POST(self):
        #Crear un animal
        if self.path == "/animales":
            data = self.read_data()
            animales = AnimalService.add_animal(data)
            HTTPResponseHandler.handle_response(self, 201, animales)
        else:
            HTTPResponseHandler.handle_response(self, 404, {"message": "Ruta no encontrada"})
    
    
    def do_PUT(self):
        #Actualizar la información de un animal
        if self.path.startswith("/animales/"):
            id = int(self.path.split("/")[-1])
            data = self.read_data()
            animales = AnimalService.update_animal(id, data)
            if animales:
                HTTPResponseHandler.handle_response(self, 200, animales)
            else:
                HTTPResponseHandler.handle_response(self, 404, {"Error": "Animal no encontrado"})
        else:
            HTTPResponseHandler.handle_response(self, 404, {"Error": "Ruta no encontrada"})
                
    def do_DELETE(self):
        #Eliminar un animal
        if self.path.startswith("/animales/"):
            id = int(self.path.split("/")[-1])
            animales = AnimalService.delete_animal(id)
            if animales:
                HTTPResponseHandler.handle_response(self, 200, animales)
            else:
                HTTPResponseHandler.handle_response(self, 404, {"Error": "Animal no encontrado"})
        else:
            HTTPResponseHandler.handle_response(self, 404, {"Error": "Ruta no encontrada"})

def run_server(port=8000):
    try:
        server_address = ("", port)
        httpd = HTTPServer(server_address, RESTRequestHandler)
        print(f"Iniciando servidor web en http://localhost:{port}/")
        httpd.serve_forever()
    except KeyboardInterrupt:
            print("\nDeteniendo el servidor HTTP...")
            httpd.server_close()
            print("Servidor detenido correctamente.")


if __name__ == "__main__":
    run_server()