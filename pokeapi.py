import requests
import json
import numpy as np
import numpy
import matplotlib.pyplot as plt
import openpyxl
nombres = []
altura = []
peso = []
estadistica = ["media","mediana"]
def bus_pokemon():
    nombre_o_id = input("\nIngrese el nombre o ID del Pokemon que desea buscar en la Pokedex: ")

    if nombre_o_id.isnumeric():
        url = f"https://pokeapi.co/api/v2/pokemon/{nombre_o_id}"
    else:
        url = f"https://pokeapi.co/api/v2/pokemon/{nombre_o_id.lower()}"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        print(f"\nNombre: {data['name'].capitalize()}")
        print(f"ID: {data['id']}")
        print(f"Altura: {data['height']/10} metros")
        print(f"Peso: {data['weight']/10} kg")
        tipos = [tipo['type']['name'] for tipo in data['types']]
        print(f"Tipos: {', '.join(tipos)}")
        guardar = input("¿Quieres guardar esta información en una pokedex de texto? (s/n): ")
        if guardar.lower() == "s":
            guardar_en_archivo(data)
        datos= input("¿Quieres guardar la altura para obtener sacar sus estadísticas? (s/n): ")
        if datos.lower() == "s":
            graficar_datos(data)
    else:
        print("\nNo se pudo encontrar el Pokemon en la Pokedex. Intente nuevamente.")

def lista_pokemon():
    offset = 0
    limit = input("Ingrese la cantidad de pokemones en lista que desea ver: ")

    if limit.isnumeric():

        while True:
            limit = int(limit)
            response = requests.get(f"https://pokeapi.co/api/v2/pokemon?offset={offset}&limit={limit}")

            if response.status_code == 200:
                data = response.json()
                resultados = data['results']

                for pokemon in resultados:
                    print(pokemon['name'].capitalize())

                print("")

                while True:
                    opcion = input(f"Presione 'n' para ver los siguientes {limit} pokemones o cualquier otra tecla para volver al menú: ")

                    if opcion.lower() == 'n':
                        offset += limit
                        break
                    else:
                        return
            else:
                print("\nNo se pudieron obtener los datos. Intente nuevamente.")
                return
    else:
        print("Digito incorrecto, ingrese por favor un número")
        return
    
def guardar_en_archivo(data):
        print("IMPORTANTE USO DE LA POKEDEX: si no existe la pokedex se creara uno nuevo para usted, en caso contrario el pokemon será agregado a tu pokedex existente \n")
        nombre_archivo = input("\nIngrese el nombre de tu nuevo/existente pokedex: ")
        try:
            with open(nombre_archivo, 'a') as archivo:
                archivo.write(f"Nombre: {data['name'].capitalize()}\n")
                archivo.write(f"ID: {data['id']}\n")
                archivo.write(f"Altura: {data['height']/10} metros\n")
                archivo.write(f"Peso: {data['weight']/10} kg\n")
                tipos = [tipo['type']['name'] for tipo in data['types']]
                archivo.write(f"Tipos: {', '.join(tipos)}\n")
                archivo.write("\n")
            print(f"\nLos datos del Pokemon se han guardado en la pokedex llamada '{nombre_archivo}' correctamente.")  
        except:
            print("\nNo se pudo guardarla pokedex. Intente nuevamente.")

    
def leer_archivo():
    nombre_archivo = input("\nIngrese de tu pokedex para leer los datos: ")

    try:
        with open(nombre_archivo, 'r') as archivo:
            print(archivo.read())
    except:
        print("\nNo se pudo leer la pokedex, la pokedex que solicitó no existe. Intente nuevamente.")

def graficar_datos(data):
    print ("La altura de los pokemón que deseas graficar se guardarán aquí para graficarlos.")
    grafica = input("\nIngrese el nombre de cómo quiere que se llame el documento con los datos a graficar: ")
    try:
        with open(grafica,'a') as dato:
            dato.write(f"Nombre: {data['name'].capitalize()}\n")
            dato.write(f"Altura: {data['height']/10} metros\n")
            dato.write(f"Peso: {data['weight']/10} kg\n")
            nombres.append(data['name'])
            altura.append(data['height']/10)
            peso.append(data['weight']/10)
            dato.write("\n")
        print(f"Los datos se guardaron con éxito, en '{grafica}' correctamente.")
    except:
        print("No se pudieron guardar los datos, Intente de nuevo.")


def guardar_promedios_en_excel(estadisticas, valores, excel_file):
    try:
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.append(["Estadística", "Valor"])
        for estadistica, valor in zip(estadisticas, valores):
            sheet.append([estadistica, valor])
        workbook.save(excel_file)
        print(f"Estadísticas guardadas en el archivo Excel '{excel_file}' correctamente.")
    except Exception as e:
        print(f"No se pudieron guardar las estadísticas en el archivo Excel. Error: {str(e)}")


def mostrar_gra():
    grafica = input("\nIngrese el nombre del archivo donde guardo los datos a graficar: ")

    try:
        with open(grafica, 'a') as dato:
            plt.subplot(1,3,1)
            plt.plot(nombres,altura, label="altura", color="green", marker="<")
            plt.title("Alturas pokemon")
            plt.ylabel('altura en metros')
            plt.yticks(np.arange(0,21,1))
            plt.grid()
            plt.minorticks_on()
            plt.legend()
            plt.subplot(1,3,2)
            plt.plot(nombres,peso, label="peso", color="red", marker="*", linestyle='--')
            plt.title("Peso de los pokemon")
            plt.ylabel('peso en kilogramos')
            plt.yticks(np.arange(0,601,20))
            plt.grid()
            plt.minorticks_on()
            plt.legend()
            plt.subplot(1,3,3)
            promedios = []
            media = numpy.mean(altura)
            mediana = numpy.median(altura)
            promedios.append(media)
            promedios.append(mediana)
            plt.plot(estadistica,promedios, label="promedios", color="black",marker="x", linestyle=' ')
            plt.title("Alturas Estadisticas")
            plt.yticks(np.arange(0,21,1))
            plt.grid()
            plt.minorticks_on()
            plt.legend()
            plt.show()
        promedios = [np.mean(altura), np.median(altura)]
        guardar_promedios_en_excel(estadistica, promedios, "estadisticas_pokemon.xlsx")
        print("Se graficó correctamente y las estadísticas se guardaron en 'estadisticas_pokemon.xlsx'.")
    except Exception as e:
        print(f"No se encontraron gráficas o hubo un error: {str(e)}")