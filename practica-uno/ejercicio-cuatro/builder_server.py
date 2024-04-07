from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from urllib.parse import urlparse, parse_qs


pacientes = [
    {
        "ci": 2487566,
        "nombre": "Luz",
        "apellido": "Mamani",
        "edad": 30,
        "genero": "Femenino",
        "diagnostico": "Diabetes",
        "doctor": "Doctora Gabriela Flores", 
    },
    {
        "ci": 664559,
        "nombre": "Kamil",
        "apellido": "Garcia",
        "edad": 25,
        "genero": "Masculino",
        "diagnostico": "Cancer",
        "doctor": "Doctor Pedro Perez",
    },    
    {
        "ci": 8464559,
        "nombre": "Andres",
        "apellido": "Lopez",
        "edad": 20,
        "genero": "Masculino",
        "diagnostico": "Diabetes",
        "doctor": "Doctor Pedro Perez",
    }, 
]

class Paciente:
    def __init__(self):
        self.ci = None
        self.nombre = None
        self.apellido =None
        self.edad = None
        self.genero = None
        self.diagnostico = None
        self.doctor = None
    
    def __str__(self):
        return f"Paciente, ci: {self.ci}, nombre: {self.nombre}, apellido: {self.apellido}, edad: {self.edad}, genero: {self.genero}, diagnostico: {self.diagnostico}, doctor: {self.doctor}"
                    
class PacienteBuilder:
    def __init__(self):
        self.paciente = Paciente()
        
    def set_ci(self, ci):
        self.paciente.ci = ci
        
    def set_nombre(self, nombre):
        self.paciente.nombre = nombre
        
    def set_apellido(self, apellido):
        self.paciente.apellido = apellido
    
    def set_edad(self, edad):
        self.paciente.edad = edad
    
    def set_genero(self, genero):
        self.paciente.genero = genero
        
    def set_diagnostico(self, diagnostico):
        self.paciente.diagnostico = diagnostico
    
    def set_doctor(self, doctor):
        self.paciente.doctor = doctor
        
    def get_paciente(self):
        return self.paciente
        
class Hospital:
    def __init__(self, builder):
        self.builder = builder
    
    def create_paciente(self, ci, nombre, apellido, edad, genero, diagnostico, doctor):
        self.builder.set_ci(ci)
        self.builder.set_nombre(nombre)
        self.builder.set_apellido(apellido)
        self.builder.set_edad(edad)
        self.builder.set_genero(genero)
        self.builder.set_diagnostico(diagnostico)
        self.builder.set_doctor(doctor)
        
        return self.builder.get_paciente()

class PacienteService:
    def __init__(self):
        self.builder = PacienteBuilder()
        self.hospital = Hospital(self.builder)
        self.pacientes = pacientes
        
    def create_paciente(self, post_data):
        ci = post_data.get('ci', None)
        nombre = post_data.get('nombre', None)
        apellido = post_data.get('apellido', None)
        edad = post_data.get('edad', None)
        genero = post_data.get('genero', None)
        diagnostico = post_data.get('diagnostico', None)
        doctor = post_data.get('doctor', None)
        
        paciente = self.hospital.create_paciente(ci, nombre, apellido, edad, genero, diagnostico, doctor)
        self.pacientes.append(paciente.__dict__)

        return paciente
    
    def read_paciente(self):
        return pacientes
    
    def read_paciente_ci(self, ci):
        for paciente in self.pacientes:
            if paciente["ci"] == ci:
                return paciente
        return None
    
    def read_pacientes_por_diagnostico(self, diagnostico):
        return [paciente for paciente in self.pacientes if paciente['diagnostico'] == diagnostico]
    
    def read_pacientes_por_doctor(self, doctor):
        return [paciente for paciente in self.pacientes if paciente['doctor'] == doctor]
    
    def update_paciente(self, ci, post_data):
        for paciente in self.pacientes:
            if paciente["ci"] == ci:
                paciente.update(post_data)
                return paciente
        return None
    
    def delete_paciente(self, ci):
        for paciente in self.pacientes:
            if paciente["ci"] == ci:
                self.pacientes.remove(paciente)
                return paciente
        return None

class HTTPDataHandler:
    @staticmethod
    def handle_response(handler, status, data):
        handler.send_response(status)
        handler.send_header("Content-type", "application/json")
        handler.end_headers()
        handler.wfile.write(json.dumps(data).encode("utf-8"))
        
    @staticmethod
    def handle_reader(handler):
        content_length = int(handler.headers['Content-Length'])
        post_data = handler.rfile.read(content_length)
        return json.loads(post_data.decode('utf-8'))
    
class PacienteHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.controller = PacienteService()
        super().__init__(*args, **kwargs)

    def do_POST(self):
        # Crear un paciente
        if self.path == "/pacientes":
            data = HTTPDataHandler.handle_reader(self)
            response_data = self.controller.create_paciente(data)
            HTTPDataHandler.handle_response(self, 200, response_data.__dict__)
        else:
            HTTPDataHandler.handle_response(self, 404, {"Error": "Ruta no existente"})

    def do_GET(self):
        parsed_url = urlparse(self.path)
        query_params = parse_qs(parsed_url.query)
        
        # Listar todos los pacientes
        if self.path == "/pacientes":
            response_data = self.controller.read_paciente()
            HTTPDataHandler.handle_response(self, 200, response_data)
        
        # Listar a los pacientes que tienen diagnóstico específico
        elif self.path.startswith("/pacientes") and "diagnostico" in query_params:            
            diagnostico = query_params["diagnostico"][0]
            pacientes_diabetes = self.controller.read_pacientes_por_diagnostico(diagnostico)                
            if pacientes_diabetes:
                HTTPDataHandler.handle_response(self, 200, pacientes_diabetes)
            else:
                HTTPDataHandler.handle_response(self, 204, [])
        
        # Listar a los pacientes que atiende un doctor específico
        elif self.path.startswith("/pacientes") and "doctor" in query_params:            
            doctor = query_params['doctor'][0]
            pacientes_doctor = self.controller.read_pacientes_por_doctor(doctor)                
            HTTPDataHandler.handle_response(self, 200, pacientes_doctor)            
        
        # Buscar pacientes por CI
        elif self.path.startswith("/pacientes/"):            
            ci = int(self.path.split("/")[-1])
            response_data = self.controller.read_paciente_ci(ci)
            HTTPDataHandler.handle_response(self, 200, response_data)
        
        else:
            HTTPDataHandler.handle_response(self, 404, {"Error": "Ruta no existente"})

    def do_PUT(self):
        # Actualizar la información de un paciente
        if self.path.startswith("/pacientes/"):
            index = int(self.path.split("/")[2])
            data = HTTPDataHandler.handle_reader(self)
            response_data = self.controller.update_paciente(index, data)
            if response_data:
                HTTPDataHandler.handle_response(self, 200, response_data)
            else:
                HTTPDataHandler.handle_response(self, 404, {"Error": "Índice de paciente no válido"})
        else:
            HTTPDataHandler.handle_response(self, 404, {"Error": "Ruta no existente"})

    def do_DELETE(self):
        # Eliminar un paciente
        if self.path.startswith("/pacientes/"):
            index = int(self.path.split("/")[2])
            deleted_paciente = self.controller.delete_paciente(index)
            if deleted_paciente:
                HTTPDataHandler.handle_response(self, 200, {"message": "paciente eliminado correctamente"})
            else:
                HTTPDataHandler.handle_response(self, 404, {"Error": "Índice de paciente no válido"})
        else:
            HTTPDataHandler.handle_response(self, 404, {"Error": "Ruta no existente"})


def run(server_class=HTTPServer, handler_class=PacienteHandler, port=8000):
    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    print(f"Iniciando servidor HTTP en puerto {port}...")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nDeteniendo el servidor HTTP...")
        httpd.server_close()
        print("Servidor detenido correctamente.")

if __name__ == "__main__":
    run()