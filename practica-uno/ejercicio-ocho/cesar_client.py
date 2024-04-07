import requests

url = "http://localhost:8000/mensajes"

print("--POST---")
nuevo_mensaje = {
    "contenido": "Hola mundo"
}
response = requests.post(url, json=nuevo_mensaje)
print(response.text)

print("--POST---")
nuevo_mensaje = {
    "contenido": "hola a todos"
}
response = requests.post(url, json=nuevo_mensaje)
print(response.text)

print("--POST---")
response = requests.get(url)
print(response.text)

print("BUSCAR ID")
id = 2
response_ci = requests.get(f"{url}/{id}")
print(response_ci.text)

print("--- PUT mensaje con id ---")
id = 2
actualizacion_mensaje = {
    "contenido": "Vamos a jugar"
}
response = requests.put(f"{url}/{id}", json=actualizacion_mensaje)
print(response.text)


print("--- DELETE---")
id = 1
response = requests.delete(f"{url}/{id}")
print(response.text)

print("--- Mensajes Actuales ---")
response = requests.get(url)
print(response.text)










