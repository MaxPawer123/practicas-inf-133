import requests
import json

url = "http://localhost:8000/animales"
headers = {"Content-Type": "application/json"}

new_animal = {
        "animal_type": "Mamifero",
        "nombre": "Leon",
        "especie": "Carnivoro",
        "genero": "Macho",
        "edad": 5,
        "peso": 190
}
response = requests.post(url=url, json=new_animal, headers=headers)
print(response.text)

new_animal = {
        "animal_type": "Ave",
        "nombre": "Aguila real",
        "especie": "Viento",
        "genero": "Hembra",
        "edad": 10,
        "peso": 7
}
response = requests.post(url=url, json=new_animal, headers=headers)
print(response.text)

new_animal = {
        "animal_type": "Reptil",
        "nombre": "Tortuga laud",
        "especie": "Dermochelys coriacea",
        "genero": "Hembra",
        "edad": 30,
        "peso": 700
}
response = requests.post(url=url, json=new_animal, headers=headers)
print(response.text)

new_animal = {
        "animal_type": "Anfibio",
        "nombre": "Salamandra comun",
        "especie": "Salamandra salamandra",
        "genero": "Indefinido",
        "edad": 30,
        "peso":10
}
response = requests.post(url=url, json=new_animal, headers=headers)
print(response.text)

new_animal = {
        "animal_type": "Pez",
        "nombre": "Pez payaso",
        "especie": "Acuatico",
        "genero": "Macho",
        "edad": 60,
        "peso": 30
}
response = requests.post(url=url, json=new_animal, headers=headers)
print(response.text)

print("Listado de todos los animales del Zoologico")
response = requests.get(url=url)
print(response.text)

print("--- Animales por especie ---")
especie = "Carnivoro"
response_especie = requests.get(f"{url}/?especie={especie}")
print(response_especie.text)

print("--- Animales por genero ---")
genero = "Hembra"
response_genero = requests.get(f"{url}/?genero={genero}")
print(response_genero.text)

print("--- Actualización de animal ---")
id = 1
actualizacion_animal = {
    "edad": 6,
    "peso": 300
}
response = requests.put(f"{url}/{id}", json=actualizacion_animal)
print(response.text)

print("--- Eliminar animal ---")
id = 2
response_eliminar = requests.delete(f"{url}/{id}")
print(response_eliminar.text)

print("Listar ANIMALES")
response = requests.get(url=url)
print(response.text)



