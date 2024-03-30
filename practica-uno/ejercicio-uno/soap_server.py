from http.server import HTTPServer
from pysimplesoap.server import SoapDispatcher, SOAPHandler



#Construye un servidor con el protocolo SOAP que permita a un cliente realizar las operaciones de suma,
# resta, multiplicación y división de dos números enteros.


def sumar(num1,num2):
    resultado=num1+num2
    return "La suma es {} y {}".format(num1,num2,resultado)

def resta(num1,num2):
    resultado=num1-num2
    return "La resta es {} y {}".format(num1,num2,resultado)

def multiplicacion(num1,num2):
    resultado=num1*num2
    return "La multiplicacion es {} y {}".format(num1,num2,resultado)

def division(num1,num2):
    resultado=num1/num2
    return "La division es {} y {}".format(num1,num2,resultado)




dispatcher = SoapDispatcher(
   "ejemplo-soap-server",
   location="http://localhost:8000/",
   action="http://localhost:8000/",
   namespace="http://localhost:8000/",
   trace=True,
   ns=True
)



dispatcher.register_function(
    "Sumar",
    sumar,
    returns={"resultado": int},
    args={"num1": int, "num2": int},
)

dispatcher.register_function(
    "Resta",
    resta,
    returns={"resultado": int},
    args={"num1": int, "num2": int},
)
dispatcher.register_function(
    "Multiplicacion",
    multiplicacion,
    returns={"resultado": int},
    args={"num1": int, "num2": int},
)
dispatcher.register_function(
    "Division",
    division,
    returns={"resultado": int},
    args={"num1": int, "num2": int},
)
server = HTTPServer(("0.0.0.0", 8000), SOAPHandler)
server.dispatcher = dispatcher
print("Servidor SOAP iniciando en http://localhost:8000/")
server.serve_forever()





