import pokeapi

def menu():
    print("\n\n *\*\*\*\*\*\*\*\*\* POKEDEX */*/*/*/*/*/*/*/*\n")
    print("1. Buscar un Pokemon por nombre o ID en la Pokedex")
    print("2. Lista de pokemones")
    print("3. Leer Pokemon desde tu Pokedex")
    print("4. Mostrar graficas")
    print("5. Salir")

    while True:
        opcion = input("\nIngrese una opción: ")

        if opcion.isnumeric():
            opcion = int(opcion)

            if opcion == 1:
                pokeapi.bus_pokemon()
            elif opcion == 2:
                pokeapi.lista_pokemon()
            elif opcion == 3:
                pokeapi.leer_archivo()
            elif opcion == 4:
                pokeapi.mostrar_gra()
            elif opcion == 5:
                print("\nGracias por utilizar POKEAPI.")
                break
            else:
                print("\nOpción inválida. Intente nuevamente.")
        else:
            print("\nOpción inválida. Intente nuevamente.")

if __name__=='__main__':
    menu()