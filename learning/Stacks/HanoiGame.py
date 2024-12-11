from StackHanoi import Stack

print("\n¡Vamos a jugar a las torres de Hanoi!")

# Crear las pilas

stacks = []

left_stack = Stack("Left")
middle_stack = Stack("Middle")
right_stack = Stack("Right")

stacks.append(left_stack)
stacks.append(middle_stack)
stacks.append(right_stack)

# Configurar el juego

# Ingresar la cantidad de discos con la que se jugara
num_disks = int(input("¿Con cuántos discos quieres jugar? "))

# Asegurarse de que haya al menos 3 discos
while num_disks < 3:
    num_disks = int(input("Ingresa un número mayor o igual a 3\n"))
    
# Agregar los discos a la pila izquierda
for disk in range(num_disks, 0, -1):  # Comienza en num_disks y termina en 1
    left_stack.push(disk)

# Calcular el número de movimientos óptimos
num_optimal_moves = 2 ** num_disks - 1

# Impresión de movimientos óptimos
print(f"\nLo más rápido que puedes resolver este juego es en {num_optimal_moves} movimientos.")

# Obtener entrada del usuario

def get_input():
    choices = ['L', 'M', 'R']  # La primer letra de las filas
    while True:
        
        for i in range(len(stacks)):
            name = stacks[i].get_name()  
            letter = choices[i]
            print(f"Escribe {letter} para {name}")

        user_input = input("Elige una opción: ").upper()   # Usamos .upper() para manejar entradas en minúsculas

        if user_input in choices:

            for i in range(len(stacks)):
                if user_input == choices[i]:
                    return stacks[i]
        else:
            print("Entrada no válida. Por favor ingresa L, M o R.")

        
# Jugando el juego

num_user_moves = 0

while right_stack.get_size() != num_disks:
    print("\n\n\n...Pilas actuales...")
    for stack in stacks:
        stack.print_items()
    
    while True:

        print("\n¿Desde qué pila quieres mover un disco?\n")
        from_stack = get_input()

        print("\n¿A qué pila quieres mover el disco?\n")
        to_stack = get_input()
        
        if from_stack.is_empty():
            print("\n\nMovimiento no válido. Inténtalo de nuevo.")
            continue
        
        elif (to_stack.is_empty() or from_stack.peek() < to_stack.peek()):
            # Movimiento válido: sacar el disco de la pila de origen
            disk = from_stack.pop()
            # Mover el disco a la pila de destino
            to_stack.push(disk)
            num_user_moves += 1  # Incrementar el contador de movimientos
            break  # Salir del bucle interno si el movimiento es válido
        
        else:
            # Si el movimiento no es válido (el disco es más grande que el de la pila de destino)
            print("\n\nMovimiento no válido. Inténtalo de nuevo.")
            continue

print("\n\nCompletaste el juego en {0} movimientos y el número óptimo de movimientos es {1}".format(num_user_moves, num_optimal_moves))
