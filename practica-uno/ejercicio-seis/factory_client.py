import requests
import json

url = "http://localhost:8000/zoologicos"
headers = {"Content-Type": "application/json"}

# POST /zoologicos
new_animal_data = {
    "nombre": "Oso",
    "especie": "mamifero",
    "genero": "masculino",
    "edad": 30,
    "peso":"2000kg"
    
}
response = requests.post(url=url, json=new_animal_data, headers=headers)
print(response.json())
  
new_animal_data = {
    "nombre": "Condor",
    "especie": "ave",
    "genero": "femenina",
    "edad": 30, 
    "peso": "15kg"
}
response = requests.post(url=url, json=new_animal_data, headers=headers)
print(response.json())


new_animal_data = {
    "nombre": "Serpiente",
    "especie": "reptil",
    "genero": "masculino",
    "edad": 60, 
    "peso": "90kg"
}
response = requests.post(url=url, json=new_animal_data, headers=headers)
print(response.json())

new_animal_data = {
    "nombre": "Rana",
    "especie": "anfibio",
    "genero": "masculino",
    "edad": 50, 
    "peso": "80kg"
}
response = requests.post(url=url, json=new_animal_data, headers=headers)
print(response.json())


new_animal_data = {
    "nombre": "Pez Payaso",
    "especie": "pez",
    "genero": "femenina",
    "edad": 30, 
    "peso": "15kg"
}
response = requests.post(url=url, json=new_animal_data, headers=headers)
print(response.json())

# GET /zoologicos
response = requests.get(url=url)
print(response.json())

# PUT /deliveries/{vehicle_id}
aniamal_id_to_update = 1
updated_animal_data = {
    "nombre": "Salamandra"
}
response = requests.put(f"{url}/{aniamal_id_to_update}", json=updated_animal_data)
print("Vehículo actualizado:", response.json())
# GET /deliveries
response = requests.get(url=url)
print(response.json())

# DELETE /deliveries/{vehicle_id}
aniamal_id_to_update = 1
response = requests.delete(f"{url}/{aniamal_id_to_update}")
print("Animal eliminado:", response.json())

# GET /deliveries
response = requests.get(url=url)
print(response.json())