import requests

# Consultando a un servidor RESTful
url = "http://localhost:8000/"
# GET obtener a todos los estudiantes por la ruta /estudiantes
ruta_get = url + "animales"
get_response = requests.request(method="GET", url=ruta_get)
print(get_response.text)
# POST agrega un nuevo estudiante por la ruta /estudiantes
ruta_post = url + "animales"
nuevo_animal = {
    "nombre": "cebra",
    "especie": "Vegetariano",
    "genero": "masculino",
    "edad": 50,
    "peso": "150kg"
}
post_response = requests.request(method="POST", url=ruta_post, json=nuevo_animal)
print(post_response.text)

# GET filtrando por nombre con query params
ruta_get = url + "animales?especie=Carniboro"
get_response = requests.request(method="GET", url=ruta_get)
print(get_response.text)

# GET filtrando por nombre con query params
ruta_get = url + "animales?genero=masculino"
get_response = requests.request(method="GET", url=ruta_get)
print(get_response.text)

print("---ACTULIZAR ANIMAL----")
ruta_actulizar = url + "animales"
animal_id=2
actulizar_animal={
    "nombre": "Leon",
    "especie": "Carnivoro",
    "genero": "masculino",
    "edad": 30,
    "peso": "100kg"
    
}
delete_response = requests.request(method="PUT", url=ruta_actulizar,json=actulizar_animal)
print(delete_response.text)



print("DELETE ANIMAL")

ruta_delete = url + "animales/delete"
delete_animal_id={
    "id": 1,
    "nombre": "Leon",
    "especie": "Carnivoro",
    "genero": "masculino",
    "edad": 30,
    "peso": "100kg"
    
}
delete_response = requests.request(method="DELETE", url=ruta_delete,json=delete_animal_id)
print(delete_response.text)

print(get_response.text)



