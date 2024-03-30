from zeep import Client 

client =Client(
    "http://localhost:8000/"
)
# peticion o requests

result = client.service.Sumar(1,2)
result2 = client.service.Resta(1,2)
result3 = client.service.Multiplicacion(1,2)
result4= client.service.Division(1,2)
print(result)
print(result2)
print(result3)
print(result4)







