import requests
# Definir la URL del servidor GraphQL
url = 'http://localhost:8000/graphql'

# Definir la consulta GraphQL simple
query_lista = """
{
        plantas{
            id
            nombre
            especie
            edad
            altura
            frutos
        }
    }
"""
# Solicitud POST al servidor GraphQL
response = requests.post(url, json={'query': query_lista})
print(response.text)

# Definir la consulta GraphQL con parametros po especie 
query = """
    {
        plantaPorEspecie(especie: "Tulbalghia"){
            id
            nombre
        }
    }
"""

# Solicitud POST al servidor GraphQL
response = requests.post(url, json={'query': query})
print(response.text)


# Definir la consulta GraphQL por  Buscar las plantas que tienen frutos
query = """
    {
        plantaPorEspecie(frutos: True){
            id
            nombre
            especie
            edad
        }
    }
"""

# Solicitud POST al servidor GraphQL
response = requests.post(url, json={'query': query})
print(response.text)




# Definir la consulta GraphQL para crear nuevo estudiante
query_crear = """
mutation {
        crearPlanta( nombre="Alfalfa", especie="Armeria ", edad=30, altura=40,frutos=false") {
            planta {
                id
                nombre
                especie
                edad
                altura
                frutos
            }
        }
    }
"""

response_mutation = requests.post(url, json={'query': query_crear})
print(response_mutation.text)

# Lista de todos los estudiantes
response = requests.post(url, json={'query': query_lista})
print(response.text)

# Definir la consulta GraphQL para eliminar un estudiante
query_eliminar = """
mutation {
        deletePlanta(id: 3) {
            planta {
                id
                nombre
                especie
                edad
                altura
                frutos
            }
        }
    }
"""

response_mutation = requests.post(url, json={'query': query_eliminar})
print(response_mutation.text)

# Lista de todos los estudiantes
response = requests.post(url, json={'query': query_lista})
print(response.text)