import requests

url = "http://localhost:8000/animales"

print("--- LISTAR A LOS ANIIMALES---")
get_response = requests.get(url)
print(get_response.text)

print("--- Nuevo animal ---")
nuevo_animal = {
    "nombre": "Tiburon",
    "especie": "Pez",
    "genero": "macho",
    "edad": 2,
    "peso": 20.5
}
response = requests.post(url, json=nuevo_animal)
print(response.text)

print("--- LISTAR A LOS ANIIMALES---")
response = requests.get(url)
print(response.text)

print("--- BUSCAR A ANIMAL especie ---")
especie = "Pez"
response_especie = requests.get(f"{url}/?especie={especie}")
print(response_especie.text)

print("--- BUSCAR A ANIMAL por  genero ---")
genero = "hembra"
response_genero = requests.get(f"{url}/?genero={genero}")
print(response_genero.text)

print("---PUT de animal ---")
id = 1
actualizacion_animal = {
    "nombre": "Max",
    "edad": 3
}
response = requests.put(f"{url}/{id}", json=actualizacion_animal)
print(response.text)

print("--- DELTE  animal ---")
id = 2
response_eliminar = requests.delete(f"{url}/{id}")
print(response_eliminar.text)