import tkinter as tk
from tkinter import Frame, Entry, Button, Checkbutton, StringVar, IntVar, ttk, messagebox
import requests
import os
import sys

# Agregar la ruta del proyecto al path para poder importar módulos
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

# URL base para las peticiones al backend
BASE_URL = "http://localhost:8000/"

class CursosScreen:
    def __init__(self, root=None, show_home_callback=None):
        # Si no se proporciona una raíz, crear una nueva ventana
        if root is None:
            self.root = tk.Tk()
            self.is_main_window = True
        else:
            self.root = root
            self.is_main_window = False
            
        # Guardar el callback para volver al home
        self.show_home_callback = show_home_callback
            
        self.root.title("Gestión de Cursos")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")
        
        # Variables para los filtros
        self.filtro_tipo = StringVar(value="Selecciona")
        self.numero_salon = StringVar()
        self.bloque_seleccionado = StringVar(value="")
        self.docente_seleccionado = StringVar()
        self.curso_seleccionado = StringVar()
        
        # Variables para los checkboxes
        self.check_a = IntVar()
        self.check_b = IntVar()
        self.check_c = IntVar()
        
        # Datos de cursos y docentes
        self.cursos = []
        self.docentes = {}  # Diccionario para mapear nombres a cédulas
        
        # Configurar el estilo de la ventana
        self.setup_ui()
        
        # Cargar datos iniciales
        self.load_cursos()
        
    def setup_ui(self):
        # Frame principal
        main_frame = tk.Frame(self.root, bg="#f0f0f0")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Frame para los filtros y botón de regresar
        top_frame = tk.Frame(main_frame, bg="#f0f0f0")
        top_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Frame para los filtros (lado izquierdo)
        filter_frame = tk.Frame(top_frame, bg="#f0f0f0")
        filter_frame.pack(side=tk.LEFT, fill=tk.X)
        
        # Frame para el botón de regresar (lado derecho)
        back_frame = tk.Frame(top_frame, bg="#f0f0f0")
        back_frame.pack(side=tk.RIGHT, padx=(0, 10))
        
        # Botón para regresar (ahora en la parte superior derecha)
        back_button = tk.Button(
            back_frame,
            text="Regresar",
            command=self.volver_al_home,
            bg="#f44336",
            fg="white",
            font=("Arial", 10),
            padx=15,
            pady=5
        )
        back_button.pack(side=tk.RIGHT)
        
        # Combobox para tipo de filtro
        tipo_label = tk.Label(filter_frame, text="Filtrar por:", bg="#f0f0f0")
        tipo_label.grid(row=0, column=0, padx=(0, 5), pady=5)
        
        tipo_combo = ttk.Combobox(filter_frame, textvariable=self.filtro_tipo, state="readonly")
        tipo_combo['values'] = ["Selecciona", "Salon", "Docente", "Curso"]
        tipo_combo.current(0)
        tipo_combo.grid(row=0, column=1, padx=5, pady=5)
        tipo_combo.bind("<<ComboboxSelected>>", self.on_filtro_change)
        
        # Frame para componentes de filtro de salón
        self.salon_frame = tk.Frame(filter_frame, bg="#f0f0f0")
        self.salon_frame.grid(row=0, column=2, padx=5, pady=5)
        self.salon_frame.grid_remove()  # Inicialmente oculto
        
        # Campo de texto para número de salón
        numero_label = tk.Label(self.salon_frame, text="Número:", bg="#f0f0f0")
        numero_label.pack(side=tk.LEFT, padx=(0, 5))
        
        numero_entry = Entry(self.salon_frame, textvariable=self.numero_salon, width=10)
        numero_entry.pack(side=tk.LEFT, padx=5)
        
        # Frame para los checkboxes de bloque
        self.bloque_frame = tk.Frame(self.salon_frame, bg="#f0f0f0")
        self.bloque_frame.pack(side=tk.LEFT, padx=(10, 5))
        
        # Checkboxes para bloques
        def toggle_checkboxes(var, value, others):
            if var.get() == 1:
                self.bloque_seleccionado.set(value)
                for other_var in others:
                    other_var.set(0)
            else:
                self.bloque_seleccionado.set("")
        
        check_a = Checkbutton(
            self.bloque_frame, 
            text="A", 
            variable=self.check_a, 
            bg="#f0f0f0",
            command=lambda: toggle_checkboxes(self.check_a, "A", [self.check_b, self.check_c])
        )
        check_a.pack(side=tk.LEFT, padx=5)
        
        check_b = Checkbutton(
            self.bloque_frame, 
            text="B", 
            variable=self.check_b, 
            bg="#f0f0f0",
            command=lambda: toggle_checkboxes(self.check_b, "B", [self.check_a, self.check_c])
        )
        check_b.pack(side=tk.LEFT, padx=5)
        
        check_c = Checkbutton(
            self.bloque_frame, 
            text="C", 
            variable=self.check_c, 
            bg="#f0f0f0",
            command=lambda: toggle_checkboxes(self.check_c, "C", [self.check_a, self.check_b])
        )
        check_c.pack(side=tk.LEFT, padx=5)
        
        # Frame para componentes de filtro de docente
        self.docente_frame = tk.Frame(filter_frame, bg="#f0f0f0")
        self.docente_frame.grid(row=0, column=2, padx=5, pady=5)
        self.docente_frame.grid_remove()  # Inicialmente oculto
        
        # Combobox para selección de docente
        docente_label = tk.Label(self.docente_frame, text="Docente:", bg="#f0f0f0")
        docente_label.pack(side=tk.LEFT, padx=(0, 5))
        
        self.docente_combo = ttk.Combobox(self.docente_frame, textvariable=self.docente_seleccionado, width=60)  # Ancho duplicado
        self.docente_combo.pack(side=tk.LEFT, padx=5)
        
        # Configurar el combobox para permitir búsqueda
        self.docente_combo.bind('<KeyRelease>', self.filtrar_docentes_combobox)
        
        # Frame para componentes de filtro de curso
        self.curso_frame = tk.Frame(filter_frame, bg="#f0f0f0")
        self.curso_frame.grid(row=0, column=2, padx=5, pady=5)
        self.curso_frame.grid_remove()  # Inicialmente oculto
        
        # Combobox para selección de curso
        curso_label = tk.Label(self.curso_frame, text="Curso:", bg="#f0f0f0")
        curso_label.pack(side=tk.LEFT, padx=(0, 5))
        
        self.curso_combo = ttk.Combobox(self.curso_frame, textvariable=self.curso_seleccionado, width=60)  # Ancho duplicado
        self.curso_combo.pack(side=tk.LEFT, padx=5)
        
        # Configurar el combobox para permitir búsqueda
        self.curso_combo.bind('<KeyRelease>', self.filtrar_cursos_combobox)
        
        # Botón de filtrar
        filtrar_button = Button(
            filter_frame,
            text="Filtrar",
            command=self.aplicar_filtro,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 10),
            padx=15,
            pady=5
        )
        filtrar_button.grid(row=0, column=3, padx=(20, 0), pady=5)
        
        # Crear cuadrícula de 7x8
        grid_frame = tk.Frame(main_frame, bg="#f0f0f0")
        grid_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Crear celdas de la cuadrícula (7 columnas x 8 filas)
        self.grid_cells = []
        for row in range(8):
            row_cells = []
            for col in range(7):
                cell = tk.Frame(
                    grid_frame, 
                    width=100, 
                    height=60, 
                    bg="white",
                    highlightbackground="#cccccc",
                    highlightthickness=1
                )
                cell.grid(row=row, column=col, padx=2, pady=2, sticky="nsew")
                
                # Hacer que la celda mantenga su tamaño
                cell.grid_propagate(False)
                
                # Añadir un label vacío para cada celda
                label = tk.Label(cell, text="", bg="white", justify=tk.LEFT, anchor="nw", wraplength=95)
                label.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
                
                row_cells.append(label)
            self.grid_cells.append(row_cells)
        
        # Añadir los días de la semana en la primera fila
        dias_semana = ["", "", "LUNES", "MARTES", "MIÉRCOLES", "JUEVES", "VIERNES", "SÁBADO"]
        for col in range(1, 7):
            self.grid_cells[0][col].config(text=dias_semana[col+1], font=("Arial", 10, "bold"))
        
        # Añadir los horarios en la primera columna
        horarios = [
            "",
            "",
            "8 - 10",
            "10 - 12",
            "12 - 14",
            "14 - 16",
            "16 - 18",
            "18 - 20",
            "20 - 22"
        ]
        
        # Solo añadimos hasta la fila 7 (índice 7) para no exceder el tamaño de la cuadrícula
        for row in range(1, 8):
            if row < len(horarios):
                self.grid_cells[row][0].config(text=horarios[row+1], font=("Arial", 10, "bold"))
        
        # Configurar el peso de las filas y columnas para que se expandan proporcionalmente
        for i in range(8):
            grid_frame.grid_rowconfigure(i, weight=1)
        for i in range(7):
            grid_frame.grid_columnconfigure(i, weight=1)
    
    def volver_al_home(self):
        """Método para volver a la pantalla de inicio"""
        # Ocultar la ventana actual
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Si hay un callback para mostrar el home, llamarlo
        if self.show_home_callback:
            self.show_home_callback()
        else:
            # Si no hay callback, simplemente cerrar la ventana
            self.root.destroy()
    
    def on_filtro_change(self, event):
        """Maneja el cambio en el combobox de filtro"""
        filtro = self.filtro_tipo.get()
        
        # Ocultar todos los frames de filtro
        self.salon_frame.grid_remove()
        self.docente_frame.grid_remove()
        self.curso_frame.grid_remove()
        
        # Mostrar el frame correspondiente según la selección
        if filtro == "Salon":
            self.salon_frame.grid()
        elif filtro == "Docente":
            self.docente_frame.grid()
            self.actualizar_lista_docentes()
        elif filtro == "Curso":
            self.curso_frame.grid()
            self.actualizar_lista_cursos()
    
    def actualizar_lista_cursos(self):
        """Actualiza la lista de cursos en el combobox"""
        opciones_cursos = []
        for curso in self.cursos:
            if "codigo" in curso and "materia" in curso and "nombre" in curso["materia"]:
                opciones_cursos.append(f"{curso['codigo']} - {curso['materia']['nombre']}")
        
        self.curso_combo['values'] = opciones_cursos
        if opciones_cursos:
            self.curso_combo.current(0)
    
    def actualizar_lista_docentes(self):
        """Actualiza la lista de docentes en el combobox"""
        # Extraer docentes únicos de los cursos
        self.docentes = {}  # Reiniciar el diccionario
        for curso in self.cursos:
            if "docente" in curso and "cc" in curso["docente"] and "nombre" in curso["docente"]:
                cc = curso["docente"]["cc"]
                nombre = curso["docente"]["nombre"]
                if cc not in self.docentes:
                    self.docentes[cc] = nombre
        
        # Crear opciones para el combobox (solo nombres)
        opciones_docentes = list(self.docentes.values())
        
        self.docente_combo['values'] = opciones_docentes
        if opciones_docentes:
            self.docente_combo.current(0)
    
    def filtrar_cursos_combobox(self, event):
        """Filtra los cursos en el combobox según lo que se escribe"""
        texto = self.curso_combo.get().lower()
        opciones_filtradas = []
        
        for curso in self.cursos:
            if "codigo" in curso and "materia" in curso and "nombre" in curso["materia"]:
                opcion = f"{curso['codigo']} - {curso['materia']['nombre']}"
                if texto in opcion.lower():
                    opciones_filtradas.append(opcion)
        
        self.curso_combo['values'] = opciones_filtradas
    
    def filtrar_docentes_combobox(self, event):
        """Filtra los docentes en el combobox según lo que se escribe"""
        texto = self.docente_combo.get().lower()
        opciones_filtradas = []
        
        # Filtrar opciones (solo nombres)
        for nombre in self.docentes.values():
            if texto in nombre.lower():
                opciones_filtradas.append(nombre)
        
        self.docente_combo['values'] = opciones_filtradas
    
    def load_cursos(self):
        """Carga todos los cursos desde el backend"""
        try:
            # Realizar petición al backend para obtener cursos detallados
            response = requests.get(f"{BASE_URL}cursos/detallados")
            
            # Verificar si la petición fue exitosa
            if response.status_code == 200:
                self.cursos = response.json()
            else:
                # Manejar error silenciosamente
                pass
        except Exception as e:
            # Manejar error silenciosamente
            pass
    
    def limpiar_cuadricula(self):
        """Limpia todas las celdas de la cuadrícula excepto los encabezados"""
        for row in range(1, 8):
            for col in range(1, 7):
                self.grid_cells[row][col].config(text="", bg="white")
    
    def aplicar_filtro(self):
        """Aplica el filtro seleccionado y muestra los resultados en la cuadrícula"""
        # Limpiar la cuadrícula antes de aplicar el filtro
        self.limpiar_cuadricula()
        
        # Obtener el tipo de filtro seleccionado
        filtro = self.filtro_tipo.get()
        
        # Si no se ha seleccionado un filtro válido, no hacer nada
        if filtro == "Selecciona":
            messagebox.showinfo("Información", "Por favor seleccione un tipo de filtro")
            return
        
        # Mapeo de días a columnas
        dias_a_columnas = {
            "LUNES": 1,
            "MARTES": 2,
            "MIÉRCOLES": 3,
            "JUEVES": 4,
            "VIERNES": 5,
            "SÁBADO": 6
        }
        
        # Mapeo de horas a filas
        horas_a_filas = {
            8: 1,
            10: 2,
            12: 3,
            14: 4,
            16: 5,
            18: 6,
            20: 7
        }
        
        # Contador para cursos encontrados
        cursos_encontrados = 0
        
        # Aplicar filtro según el tipo seleccionado
        if filtro == "Salon":
            # Verificar si se ha seleccionado un filtro válido
            if not self.numero_salon.get() or not self.bloque_seleccionado.get():
                messagebox.showinfo("Información", "Por favor ingrese un número de salón y seleccione un bloque")
                return
            
            # Obtener los valores del filtro
            numero = self.numero_salon.get()
            bloque = self.bloque_seleccionado.get()
            
            # Filtrar cursos por salón
            for curso in self.cursos:
                if "horario" in curso and "bloques" in curso["horario"]:
                    for bloque_curso in curso["horario"]["bloques"]:
                        # Verificar si el salón coincide con el filtro
                        if ("salon" in bloque_curso and 
                            bloque_curso["salon"]["bloque"] == bloque and 
                            str(bloque_curso["salon"]["numero"]) == numero):
                            
                            # Obtener día y hora
                            dia = bloque_curso["dia"].upper()
                            hora_inicio = bloque_curso["horaInicio"]
                            
                            cursos_encontrados += 1
                            
                            # Verificar si el día y la hora están en nuestro mapeo
                            if dia in dias_a_columnas and hora_inicio in horas_a_filas:
                                col = dias_a_columnas[dia]
                                row = horas_a_filas[hora_inicio]
                                
                                # Crear texto para la celda (más compacto)
                                texto = f"{curso['materia']['nombre']}\n{curso['docente']['nombre']}\nCód: {curso['codigo']}"
                                
                                # Actualizar la celda
                                self.grid_cells[row][col].config(text=texto, bg="#e6f7ff")
            
            # Mostrar resumen
            if cursos_encontrados == 0:
                messagebox.showinfo("Información", f"No se encontraron cursos para el salón {bloque}-{numero}")
                
        elif filtro == "Docente":
            # Verificar si se ha seleccionado un docente
            if not self.docente_seleccionado.get():
                messagebox.showinfo("Información", "Por favor seleccione un docente")
                return
            
            # Obtener el nombre del docente seleccionado
            nombre_docente = self.docente_seleccionado.get()
            
            # Buscar la cédula correspondiente al nombre
            cedula = None
            for cc, nombre in self.docentes.items():
                if nombre == nombre_docente:
                    cedula = cc
                    break
            
            if not cedula:
                messagebox.showinfo("Información", "No se pudo encontrar la cédula del docente seleccionado")
                return
            
            # Filtrar cursos por docente
            for curso in self.cursos:
                if "docente" in curso and "cc" in curso["docente"] and str(curso["docente"]["cc"]) == str(cedula):
                    # Si el docente coincide, mostrar todos sus bloques de horario
                    if "horario" in curso and "bloques" in curso["horario"]:
                        for bloque_curso in curso["horario"]["bloques"]:
                            # Obtener día y hora
                            dia = bloque_curso["dia"].upper()
                            hora_inicio = bloque_curso["horaInicio"]
                            
                            cursos_encontrados += 1
                            
                            # Verificar si el día y la hora están en nuestro mapeo
                            if dia in dias_a_columnas and hora_inicio in horas_a_filas:
                                col = dias_a_columnas[dia]
                                row = horas_a_filas[hora_inicio]
                                
                                # Crear texto para la celda (más compacto)
                                salon_info = f"{bloque_curso['salon']['bloque']}-{bloque_curso['salon']['numero']}" if "salon" in bloque_curso else "Sin salón"
                                texto = f"{curso['materia']['nombre']}\nCód: {curso['codigo']}\nSalón: {salon_info}"
                                
                                # Actualizar la celda
                                self.grid_cells[row][col].config(text=texto, bg="#e6f7ff")
            
            # Mostrar resumen
            if cursos_encontrados == 0:
                messagebox.showinfo("Información", f"No se encontraron cursos para el docente {nombre_docente}")
        
        elif filtro == "Curso":
            # Verificar si se ha seleccionado un curso
            if not self.curso_seleccionado.get():
                messagebox.showinfo("Información", "Por favor seleccione un curso")
                return
            
            # Obtener el código del curso seleccionado (la primera parte antes del guión)
            curso_seleccionado = self.curso_seleccionado.get().split(" - ")[0]
            
            # Filtrar por el código del curso
            for curso in self.cursos:
                if "codigo" in curso and curso["codigo"] == curso_seleccionado:
                    # Si el curso coincide, mostrar todos sus bloques de horario
                    if "horario" in curso and "bloques" in curso["horario"]:
                        for bloque_curso in curso["horario"]["bloques"]:
                            # Obtener día y hora
                            dia = bloque_curso["dia"].upper()
                            hora_inicio = bloque_curso["horaInicio"]
                            
                            cursos_encontrados += 1
                            
                            # Verificar si el día y la hora están en nuestro mapeo
                            if dia in dias_a_columnas and hora_inicio in horas_a_filas:
                                col = dias_a_columnas[dia]
                                row = horas_a_filas[hora_inicio]
                                
                                # Crear texto para la celda
                                salon_info = f"{bloque_curso['salon']['bloque']}-{bloque_curso['salon']['numero']}" if "salon" in bloque_curso else "Sin salón"
                                texto = f"{curso['materia']['nombre']}\n{curso['docente']['nombre']}\nGrupo: {curso['grupo']}\nSalón: {salon_info}"
                                
                                # Actualizar la celda
                                self.grid_cells[row][col].config(text=texto, bg="#e6f7ff")
            
            # Mostrar resumen
            if cursos_encontrados == 0:
                messagebox.showinfo("Información", f"No se encontraron horarios para el curso {curso_seleccionado}")
    
    def run(self):
        """Inicia el bucle principal de la aplicación"""
        if self.is_main_window:
            self.root.mainloop()

if __name__ == "__main__":
    app = CursosScreen()
    app.run()