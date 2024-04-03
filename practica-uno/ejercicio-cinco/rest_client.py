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
    "nombre": "Ariel",
    "especie": "Vegetariano",
    "genero": "cebra",
    "edad": 50,
    "peso": "150kg"
}
post_response = requests.request(method="POST", url=ruta_post, json=nuevo_animal)
print(post_response.text)


# GET filtrando por nombre con query params
ruta_get = url + "animales?especie=Carnivoro"
get_response = requests.request(method="GET", url=ruta_get)
print(get_response.text)