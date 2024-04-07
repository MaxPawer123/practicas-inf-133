from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from urllib.parse import urlparse, parse_qs

pacientes = [
    
    {
        "ci": 112233,
        "nombre": "Pedrito",
        "apellido": "García",
        "edad": 25,
        "genero": "Masculino",
        "diagnostico": "Cancer",
        "doctor": "Ariel"
    },
    
    {
        "ci": 334562,
        "nombre": "Jose",
        "apellido": "Mamani",
        "edad": 20,
        "genero": "Masculino",
        "diagnostico": "Diabetes",
        "doctor": "Doctor Pedro Perez"
    },
    
    {
        "ci": 135454,
        "nombre": "Luz",
        "apellido": "Choque",
        "edad": 25,
        "genero": "Femenina",
        "diagnostico": "fdf",
        "doctor": "Doctor Pedro Perez"
    },

]


class PacientesService:
    
    @staticmethod
    def add_patient(data):
        pacientes.append(data)
        return pacientes

    @staticmethod
    def update_patient(ci, data):
        paciente = PacientesService.find_patient(ci)
        if paciente:
            indice=pacientes.index(paciente)
            paciente[indice].update(data)
            return pacientes
        else:
            return None

    @staticmethod
    def delete_patient(ci):
        for paciente in pacientes:
            if paciente["ci"]==ci:
                pacientes.remove(paciente)
                return pacientes
        return None
    
    @staticmethod
    def find_patient(ci):
        return next((paciente for paciente in pacientes if paciente["ci"] == ci), None)

    @staticmethod
    def filter_pacientes_diagnostico(diagnostico):
        return [
            paciente for paciente in pacientes if paciente["diagnostico"] == diagnostico
        ]
    @staticmethod
    def filter_pacientes_doctor(doctor):
        return [
            paciente for paciente in pacientes if paciente["doctor"] == doctor
        ]

class HTTPResponseHandler:
    @staticmethod
    def handle_response(handler, status, data):
        handler.send_response(status)
        handler.send_header("Content-type", "application/json")
        handler.end_headers()
        handler.wfile.write(json.dumps(data).encode("utf-8"))


class RESTRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        query_params = parse_qs(parsed_path.query)

        if parsed_path.path == "/pacientes":
            if "diagnostico" in query_params:
                diagnostico = query_params["diagnostico"][0]
                pacientes_filtrados = PacientesService.filter_pacientes_diagnostico(
                    diagnostico
                )
                if pacientes_filtrados != []:
                    HTTPResponseHandler.handle_response(
                        self, 200, pacientes_filtrados
                    )
                else:
                    HTTPResponseHandler.handle_response(self, 204, [])
            elif "doctor" in query_params:
                doctor = query_params["doctor"][0]
                pacientes_filtrados = PacientesService.filter_pacientes_doctor(
                    doctor
                )
                if pacientes_filtrados != []:
                    HTTPResponseHandler.handle_response(
                        self, 200, pacientes_filtrados
                    )
                else:
                    HTTPResponseHandler.handle_response(self, 204, [])
            else:
                HTTPResponseHandler.handle_response(self, 200, pacientes)
      #Buscar los pacientes por ci
        elif self.path.startswith("/pacientes/"):
            ci = int(self.path.split("/")[-1])
            paciente = PacientesService.find_patient(ci)
            if paciente:
                HTTPResponseHandler.handle_response(self, 200, [paciente])
            else:
                HTTPResponseHandler.handle_response(self, 204, [])
        else:
            HTTPResponseHandler.handle_response(
                self, 404, {"Error": "Ruta no existente"}
            )

    def do_POST(self):
        if self.path == "/pacientes":
            data = self.read_data()
            pacientes = PacientesService.add_patient(data)
            HTTPResponseHandler.handle_response(self, 201, pacientes)
        else:
            HTTPResponseHandler.handle_response(
                self, 404, {"Error": "Ruta no existente"}
            )

    def do_PUT(self):
        if self.path.startswith("/pacientes/"):
            ci = int(self.path.split("/")[-1])
            data = self.read_data()
            pacientes = PacientesService.update_patient(ci, data)
            if pacientes:
                HTTPResponseHandler.handle_response(self, 200, pacientes)
            else:
                HTTPResponseHandler.handle_response(
                    self, 404, {"Error": "Estudiante no encontrado"}
                )
        else:
            HTTPResponseHandler.handle_response(
                self, 404, {"Error": "Ruta no existente"}
            )

    def do_DELETE(self):
        if self.path == "/pacientes":
            ci = int(self.path.split("/")[-1])
            pacientes = PacientesService.delete_patient(ci)
            HTTPResponseHandler.handle_response(self, 200, pacientes)
        else:
            HTTPResponseHandler.handle_response(
                self, 404, {"Error": "Ruta no existente"}
            )

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
        print("Apagando servidor web")
        httpd.socket.close()


if __name__ == "__main__":
    run_server()