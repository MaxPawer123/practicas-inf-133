import requests

# Consultando a un servidor RESTful
url = "http://localhost:8000/"
# GET obtener a todos los estudiantes por la ruta /pacientes
print("MUESTRA A LOS PACIENTES")
ruta_get = url + "pacientes"
get_response = requests.request(method="GET", url=ruta_get)
print(get_response.text)

print("---------POST---------")
# POST agrega un nuevo estudiante por la ruta /estudiantes
ruta_post = url + "pacientes"
nuevo_paciente = {
    "nombre": "David",
    "apellido": "Mamani",
    "edad": 25,
    "genero": "Masculino",
    "diagnostico":"Cancer",
    "doctor": "Pedro Pérez",
}
post_response = requests.request(method="POST", url=ruta_post, json=nuevo_paciente)
print(post_response.text)
# GET filtrando por nombre con query params

print("------Paciente ci")
ci=334562
responce_ci=requests.delete(f"{url}/{ci}")
print(responce_ci.text)


print("Listar a los pacientes que tienen diagnostico de Diabetes")
ruta_get = url + "pacientes?diagnostico=Diabetes"
get_response = requests.request(method="GET", url=ruta_get)
print(get_response.text)
print()

print("Listar a los pacientes que atiende el Doctor `Pedro Pérez`")
ruta_get = url + "pacientes?doctor=Pedro Pérez"
get_response = requests.request(method="GET", url=ruta_get)
print(get_response.text)





print("ACTUALIZAR")
ci = 334562
actualizacion_paciente_data = {
    "doctor": "Doctor Jose"
}
response = requests.request(f"{url}={ci}", method="PUT" ,json=actualizacion_paciente_data)
print(response.text)
print(get_response.text)


print("DELETE")
ci = 334562
response = requests.request(f"{url}/{ci}",method="DELETE")
print(response.text)
print(get_response.text)
# PUT /deliveries/{vehicle_id}









"""print("ACTUALIZAR")
ruta_put = url + "pacientes/1"
actualizar_paciente = {
    "diagnostico":"Conjutivitis",
    
}
put_response = requests.request(method="PUT", url=ruta_put, json=actualizar_paciente)
print(put_response.text)




ci = 334562
actualizacion_paciente_data = {
    "doctor": "Doctor Jose"
}
response_actualizar = requests.put(f"{url}/{ci}", json=actualizacion_paciente_data)
print(response_actualizar.text)
print(get_response.text)

"""



"""
# PUT /deliveries/{vehicle_id}
paciente_id_to_update = 1
ruta_put = url + "pacientes/"
updated_paciente_data = {
    "diagnostico":"Diabetes",
}
put_response = requests.request(f"{url}/{paciente_id_to_update}",method="PUT",json=updated_paciente_data,url=ruta_put)
print( put_response.text)

# GET /deliveries
response = requests.get(url=url)
print(response.json())

# DELETE /deliveries/{vehicle_id}
chocolate_id_to_delete = 1
response = requests.delete(f"{url}/{chocolate_id_to_delete}")
print("Chocolate eliminado:", response.json())

# GET /deliveries
response = requests.get(url=url)
print(response.json())

"""