import json
import requests

url = 'http://localhost:8000/graphql'

# Crear una planta
print("--- Crear una planta ---")
mutation_crear = """
mutation {
    createPlanta(nombreComun: "Toronja", especie: "Sano", edad: 5, altura: 80, frutos: false) {
        planta {
            id
            nombreComun
            especie
            edad
            altura
            frutos
        }
    }
}
"""
response = requests.post(url, json={'query': mutation_crear})
print(response.text)

# Listar todas las plantas
print("--- Lista de plantas ---")
query_lista = """ 
{
    plantas {
        id
        nombreComun
        especie
        edad
        altura
        frutos
    }
}
"""
response = requests.get(url, json={'query': query_lista})
print(response.text)

#Buscar plantas por especie
print("--- Buscar plantas por especie ---")
query_especie = """ 
{
    plantasPorEspecie(especie:"Pinus") {
        id
        nombreComun
        especie
        edad
        altura
        frutos
    }
}
"""
response = requests.get(url, json={'query': query_especie})
print(response.text)

#Buscar las plantas que tienen frutos
print("--- Buscar las plantas que tienen frutos ---")
query_frutos = """ 
{
    plantasPorFrutos(frutos:true) {
        id
        nombreComun
        especie
        edad
        altura
        frutos
    }
}
"""
response = requests.get(url, json={'query': query_frutos})
print(response.text)

#Actualizar la información de una planta
print("--- Actualizar una planta ---")
mutation_actualizar = """
mutation {
    updatePlanta(id: 3, edad: 6, altura: 100) {
        planta {
            id
            nombreComun
            especie
            edad
            altura
            frutos
        }
    }
}
"""
response = requests.post(url, json={'query': mutation_actualizar})
print(response.text)

print("-- Nuevo listado --")
response = requests.get(url, json={'query': query_lista})
print(response.text)

#Eliminar una planta
print("Eliminar una planta")
mutation_eliminar = """
mutation {
    deletePlanta(id: 2) {
        planta {
            id
            nombreComun
            especie
            edad
            altura
            frutos
        }
    }
}
"""
response = requests.post(url, json={'query': mutation_eliminar})
print(response.text)

print("-- Nuevo listado --")
response = requests.get(url, json={'query': query_lista})
print(response.text)