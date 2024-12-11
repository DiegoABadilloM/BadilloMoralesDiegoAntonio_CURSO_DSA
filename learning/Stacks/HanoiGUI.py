import tkinter as tk
from tkinter import messagebox, simpledialog
from StackHanoi import Stack

class HanoiGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Torres de Hanoi")
        
        # Variables del juego
        self.stacks = []
        self.num_disks = 0
        self.num_user_moves = 0
        self.num_optimal_moves = 0
        self.selected_from = None

        # Configuración inicial
        self.setup_game()
    
    def setup_game(self):
        # Configuración de entrada
        self.start_frame = tk.Frame(self.root)
        self.start_frame.pack(pady=20)

        tk.Label(self.start_frame, text="Selecciona el número de discos (3-8):").pack()
        self.disk_input = tk.Entry(self.start_frame)
        self.disk_input.pack()

        tk.Button(self.start_frame, text="Iniciar Juego", command=self.start_game).pack(pady=10)
    
    def start_game(self):
        try:
            self.num_disks = int(self.disk_input.get())
            if self.num_disks < 3 or self.num_disks > 8:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingresa un número entre 3 y 8.")
            return

        # Configuración del juego
        self.num_user_moves = 0
        self.num_optimal_moves = 2 ** self.num_disks - 1

        self.start_frame.destroy()
        self.create_stacks()
        self.setup_gui()
    
    def create_stacks(self):
        # Crear pilas
        self.stacks = [
            Stack("Left"),
            Stack("Middle"),
            Stack("Right")
        ]

        # Agregar discos a la pila izquierda
        for disk in range(self.num_disks, 0, -1):
            self.stacks[0].push(disk)
    
    def setup_gui(self):
        # Configurar GUI principal
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack()

        # Área de visualización de pilas
        self.canvas = tk.Canvas(self.main_frame, width=600, height=400, bg="white")
        self.canvas.pack()

        # Botones de interacción
        self.buttons_frame = tk.Frame(self.main_frame)
        self.buttons_frame.pack(pady=10)

        tk.Button(self.buttons_frame, text="Seleccionar Origen", command=self.select_from).pack(side="left", padx=10)
        tk.Button(self.buttons_frame, text="Seleccionar Destino", command=self.select_to).pack(side="left", padx=10)
        tk.Button(self.buttons_frame, text="Reiniciar Juego", command=self.reset_game).pack(side="left", padx=10)

        self.info_label = tk.Label(self.main_frame, text=f"Movimientos: 0 | Mínimos: {self.num_optimal_moves}")
        self.info_label.pack(pady=10)

        self.draw_stacks()
    
    def draw_stacks(self):
        self.canvas.delete("all")
        positions = [100, 300, 500]

        # Colores para los discos
        colors = ["red", "orange", "yellow", "green", "blue", "indigo", "violet"]

        for i, stack in enumerate(self.stacks):
            # Dibujar base de la pila
            self.canvas.create_rectangle(positions[i] - 50, 350, positions[i] + 50, 360, fill="black")
            self.canvas.create_line(positions[i], 100, positions[i], 350, fill="black", width=3)

            # Dibujar discos
            disks = []
            pointer = stack.top_item
            while pointer:
                disks.append(pointer.get_value())
                pointer = pointer.get_next_node()

            # Dibujar en orden inverso para que el disco más grande esté abajo
            for j, disk in enumerate(reversed(disks)):
                width = disk * 20
                color = colors[(disk - 1) % len(colors)]  # Asignar color según el tamaño
                self.canvas.create_rectangle(
                    positions[i] - width // 2,
                    340 - j * 20,
                    positions[i] + width // 2,
                    360 - j * 20,
                    fill=color,
                    outline="black"
                )
    
    def select_from(self):
        self.selected_from = self.get_stack_choice("Selecciona la pila de origen:")
        if self.selected_from is not None:
            messagebox.showinfo("Origen Seleccionado", f"Pila seleccionada: {self.selected_from.get_name()}")
    
    def select_to(self):
        if not self.selected_from:
            messagebox.showerror("Error", "Primero selecciona una pila de origen.")
            return

        selected_to = self.get_stack_choice("Selecciona la pila de destino:")
        if selected_to is not None:
            if self.validate_move(self.selected_from, selected_to):
                disk = self.selected_from.pop()
                selected_to.push(disk)
                self.num_user_moves += 1
                self.info_label.config(
                    text=f"Movimientos: {self.num_user_moves} | Mínimos: {self.num_optimal_moves}"
                )
                self.draw_stacks()

                if self.stacks[2].get_size() == self.num_disks:
                    messagebox.showinfo(
                        "Juego Completado",
                        f"¡Completaste el juego en {self.num_user_moves} movimientos!"
                    )
                    self.reset_game()
            else:
                messagebox.showerror("Error", "Movimiento no válido. Inténtalo de nuevo.")
    
    def validate_move(self, from_stack, to_stack):
        if from_stack.is_empty():
            return False
        if to_stack.is_empty() or from_stack.peek() < to_stack.peek():
            return True
        return False
    
    def get_stack_choice(self, message):
        choice = simpledialog.askstring("Seleccionar Pila", message)
        if choice is None:
            return None

        choice = choice.upper()
        if choice == "L":
            return self.stacks[0]
        elif choice == "M":
            return self.stacks[1]
        elif choice == "R":
            return self.stacks[2]
        else:
            messagebox.showerror("Error", "Entrada no válida. Usa L, M o R.")
            return None

    def reset_game(self):
        self.main_frame.destroy()
        self.setup_game()

# Inicialización de la ventana
if __name__ == "__main__":
    root = tk.Tk()
    app = HanoiGUI(root)
    root.mainloop()
