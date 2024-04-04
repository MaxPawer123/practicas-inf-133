from http.server import HTTPServer, BaseHTTPRequestHandler
import json

class Player: 
    _instance = None
#haci se hace el sigleton 
    def __new__(cls, name): # se entiende este singleton si exite ya creado uan instacia de esta clase 
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance.name = name
            cls._instance.health = 100
        return cls._instance
    #Sacar el nombre del incubador la instancia es que tiene que tener los atributos 
    # notiene que haber nada en el sigleton 
    def to_dict(self):
        return {"name": self.name, "health": self.health}
    
    def take_damage(self, damage):
        self.health -= damage
        
        
        

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
#solo cambia el patron de diseño         
class PlayerHandler(BaseHTTPRequestHandler): # se crea los servidores que se hace 
    def do_GET(self):
        if self.path == "/player":
            data = HTTPDataHandler.handle_reader(self)
            response_data = self.zoologico_service.add_animal(data)
            HTTPDataHandler.handle_response(self, 201, response_data.__dict__)
        else:
            HTTPDataHandler.handle_response(
                self, 404, {"message": "Ruta no encontrada"}
            )
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            player_data = json.dumps(player.to_dict())
            self.wfile.write(player_data.encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == "/player/damage":
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)
            damage = json.loads(post_data.decode("utf-8"))["damage"]
            player.take_damage(damage)
            self.send_response(200)
            self.end_headers()
            player_data = json.dumps(player.to_dict())
            self.wfile.write(player_data.encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

def main():
    global player
    player = Player("Alice")  #Se hace una instancia 

    try:
        server_address = ("", 8000)
        httpd = HTTPServer(server_address, PlayerHandler)
        print("Iniciando servidor HTTP en puerto 8000...")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Apagando servidor HTTP")
        httpd.socket.close()

if __name__ == "__main__":
    main()