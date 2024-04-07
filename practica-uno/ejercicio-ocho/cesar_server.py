from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from urllib import parse as urlparse

mensajes = []

class MensajeService:
    @staticmethod
    def cifrar_mensaje(mensaje):
        mensaje = mensaje.lower()
        new_mensaje = ""
        for char in mensaje:
            if char.isalpha():
                ascii = ord(char)
                ascii = (ascii - 97 + 3) % 26 + 97
                new_mensaje += chr(ascii)
            else:
                new_mensaje += char
        return new_mensaje
    
    @staticmethod
    def create_mensaje(data):
        contenido = data.get("contenido", "")
        contenido_encriptado = MensajeService.cifrar_mensaje(contenido)
        mensaje = {
            "id" : len(mensajes)+1,
            "contenido": contenido,
            "contenido_encriptado": contenido_encriptado
        }
        mensajes.append(mensaje)
        return mensajes

    @staticmethod
    def list_mensajes():
        return mensajes

    @staticmethod
    def buscar_id(mensaje_id):
        for mensaje in mensajes:
            if mensaje["id"] == mensaje_id:
                return mensaje
        return None

    @staticmethod
    def update_mensaje(mensaje_id, data):
        mensaje = MensajeService.buscar_id(mensaje_id)
        if mensaje:
            contenido = data.get("contenido", "")
            contenido_encriptado = MensajeService.cifrar_mensaje(contenido)
            mensaje["contenido"] = contenido
            mensaje["contenido_encriptado"] = contenido_encriptado
            return mensaje
        return None

    @staticmethod
    def delete_mensaje(mensaje_id):
        for mensaje in mensajes:
            if mensaje["id"] == mensaje_id:
                mensajes.remove(mensaje)
                return mensajes
        return None
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

class RESTRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse.urlparse(self.path)
        if parsed_path.path == "/mensajes":
            HTTPResponseHandler.handle_response(self, 200, MensajeService.list_mensajes())
        elif self.path.startswith("/mensajes/"):
            mensaje_id = int(self.path.split("/")[-1])
            mensaje = MensajeService.buscar_id(mensaje_id)
            if mensaje:
                HTTPResponseHandler.handle_response(self, 200, mensaje)
            else:
                HTTPResponseHandler.handle_response(self, 404, {"error": "Mensaje no encontrado"})
        else:
            HTTPResponseHandler.handle_response(self, 404, {"error": "Ruta no encontrada"})

    def do_POST(self):
        if self.path == "/mensajes":
            data = self.read_data()
            mensaje = MensajeService.create_mensaje(data)
            HTTPResponseHandler.handle_response(self, 201, mensaje)
        else:
            HTTPResponseHandler.handle_response(self, 404, {"error": "Ruta no encontrada"})

    def do_PUT(self):
        if self.path.startswith("/mensajes/"):            
            mensaje_id = int(self.path.split("/")[-1])
            data = self.read_data()
            mensajes = MensajeService.update_mensaje(mensaje_id, data)
            if mensajes:
                HTTPResponseHandler.handle_response(self, 200, mensajes)
            else:
                HTTPResponseHandler.handle_response(self, 404, {"error": "Mensaje no encontrado"})
        else:
            HTTPResponseHandler.handle_response(self, 404, {"error": "Ruta no encontrada"})

    def do_DELETE(self):
        if self.path.startswith("/mensajes/"):
            mensaje_id = int(self.path.split("/")[-1])
            mensajes = MensajeService.delete_mensaje(mensaje_id)
            if mensajes:
                HTTPResponseHandler.handle_response(self, 200, mensajes)
            else:
                HTTPResponseHandler.handle_response(self, 404, {"error": "Mensaje no encontrado"})
        else:
            HTTPResponseHandler.handle_response(self, 404, {"error": "Ruta no encontrada"})

    def read_data(self):
        content_length = int(self.headers["Content-Length"])
        data = self.rfile.read(content_length)
        data = json.loads(data.decode("utf-8"))
        return data

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