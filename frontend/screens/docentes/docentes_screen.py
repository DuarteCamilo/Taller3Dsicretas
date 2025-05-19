import tkinter as tk
from tkinter import ttk, messagebox, font, simpledialog
import requests
import json
import os
import sys
from typing import List, Dict, Any, Optional

# Agregar la ruta del proyecto al path para poder importar módulos
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

# URL base para las peticiones al backend
BASE_URL = "http://localhost:8000/"  # Modificar esta línea según la estructura de tu API

class DocentesScreen:
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
            
        self.root.title("Gestión de Docentes")
        self.root.geometry("1000x700")
        self.root.configure(bg="#f0f0f0")
        
        # Variables para el formulario
        self.docente_id = tk.StringVar()
        self.cc = tk.StringVar()
        self.nombre = tk.StringVar()
        self.restricciones = tk.StringVar()
        self.materias = tk.StringVar()
        self.materia_search = tk.StringVar()  # Variable para la búsqueda de materias
        
        # Lista para almacenar todas las materias
        self.materias_list = []
        self.materias_seleccionadas = []  # Lista para almacenar IDs de materias seleccionadas
        
        # Variable para almacenar el docente seleccionado en la tabla
        self.selected_docente = None
        
        # Configurar el estilo de la ventana
        self.setup_ui()
        
        # Cargar datos iniciales
        self.load_docentes()
        self.load_materias()  # Cargar materias al iniciar
        
    def setup_ui(self):
        # Frame principal con dos columnas
        main_frame = tk.Frame(self.root, bg="#f0f0f0")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Título
        title_font = font.Font(family="Arial", size=18, weight="bold")
        title_label = tk.Label(
            main_frame, 
            text="Sistema de Gestión de Docentes", 
            font=title_font,
            bg="#f0f0f0",
            fg="#333333"
        )
        title_label.pack(pady=(0, 20))
        
        # Frame para el formulario (izquierda) y la tabla (derecha)
        content_frame = tk.Frame(main_frame, bg="#f0f0f0")
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Frame para el formulario (izquierda) - reducir el ancho
        form_frame = tk.LabelFrame(content_frame, text="Formulario de Docente", bg="#f0f0f0", padx=15, pady=15, width=400)
        form_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=(0, 10))
        form_frame.pack_propagate(False)  # Esto evita que el frame se redimensione automáticamente
        
        # Frame para la tabla (derecha) - aumentar el ancho
        table_frame = tk.LabelFrame(content_frame, text="Lista de Docentes", bg="#f0f0f0", padx=15, pady=15)
        table_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        # Crear formulario
        self.create_form(form_frame)
        
        # Crear tabla
        self.create_table(table_frame)
        
        # Frame para los botones de acción
        button_frame = tk.Frame(main_frame, bg="#f0f0f0")
        button_frame.pack(fill=tk.X, pady=(20, 0))
        
        # Botones de acción
        self.create_action_buttons(button_frame)
        
        # Pie de página
        footer_label = tk.Label(
            main_frame,
            text="© 2025 Sistema de Gestión Académica - EAM",
            font=("Arial", 10),
            bg="#f0f0f0",
            fg="#888888"
        )
        footer_label.pack(side=tk.BOTTOM, pady=(20, 0))
    
    def create_form(self, parent):
        # Estilo para las etiquetas
        label_font = font.Font(family="Arial", size=10)
        entry_font = font.Font(family="Arial", size=10)
        
        # Campo oculto para el ID (se usa para actualizar/eliminar)
        id_frame = tk.Frame(parent, bg="#f0f0f0")
        id_frame.pack(fill=tk.X, pady=5)
        
        id_label = tk.Label(id_frame, text="ID:", font=label_font, bg="#f0f0f0", width=12, anchor="w")
        id_label.pack(side=tk.LEFT)
        
        id_entry = tk.Entry(id_frame, textvariable=self.docente_id, font=entry_font, state="readonly", width=20)
        id_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Campo para la cédula
        cc_frame = tk.Frame(parent, bg="#f0f0f0")
        cc_frame.pack(fill=tk.X, pady=5)
        
        cc_label = tk.Label(cc_frame, text="Cédula:", font=label_font, bg="#f0f0f0", width=12, anchor="w")
        cc_label.pack(side=tk.LEFT)
        
        # Validación para permitir solo números
        validate_numeric = self.root.register(self.validate_only_numbers)
        cc_entry = tk.Entry(
            cc_frame, 
            textvariable=self.cc, 
            font=entry_font, 
            width=30,
            validate="key",
            validatecommand=(validate_numeric, '%P')
        )
        cc_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Campo para el nombre
        nombre_frame = tk.Frame(parent, bg="#f0f0f0")
        nombre_frame.pack(fill=tk.X, pady=5)
        
        nombre_label = tk.Label(nombre_frame, text="Nombre:", font=label_font, bg="#f0f0f0", width=15, anchor="w")
        nombre_label.pack(side=tk.LEFT)
        
        nombre_entry = tk.Entry(nombre_frame, textvariable=self.nombre, font=entry_font, width=30)
        nombre_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Campo para las restricciones (ahora con checkboxes)
        restricciones_frame = tk.Frame(parent, bg="#f0f0f0")
        restricciones_frame.pack(fill=tk.X, pady=5)
        
        restricciones_label = tk.Label(restricciones_frame, text="Restricciones:", font=label_font, bg="#f0f0f0", width=15, anchor="w")
        restricciones_label.pack(side=tk.LEFT, anchor="n")
        
        # Frame para los checkboxes
        checkboxes_frame = tk.Frame(restricciones_frame, bg="#f0f0f0")
        checkboxes_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, anchor="n")
        
        # Variables para los checkboxes
        self.restriccion_manana = tk.BooleanVar(value=False)
        self.restriccion_tarde = tk.BooleanVar(value=False)
        self.restriccion_noche = tk.BooleanVar(value=False)
        
        # Checkbox para mañana
        manana_checkbox = tk.Checkbutton(
            checkboxes_frame, 
            text="mañana", 
            variable=self.restriccion_manana, 
            bg="#f0f0f0",
            command=self.actualizar_restricciones
        )
        manana_checkbox.pack(side=tk.TOP, anchor="w")
        
        # Checkbox para tarde
        tarde_checkbox = tk.Checkbutton(
            checkboxes_frame, 
            text="tarde", 
            variable=self.restriccion_tarde, 
            bg="#f0f0f0",
            command=self.actualizar_restricciones
        )
        tarde_checkbox.pack(side=tk.TOP, anchor="w")
        
        # Checkbox para noche
        noche_checkbox = tk.Checkbutton(
            checkboxes_frame, 
            text="noche", 
            variable=self.restriccion_noche, 
            bg="#f0f0f0",
            command=self.actualizar_restricciones
        )
        noche_checkbox.pack(side=tk.TOP, anchor="w")
        
        # Cambiar el campo de texto a solo lectura
        restricciones_entry = tk.Entry(
            restricciones_frame, 
            textvariable=self.restricciones, 
            font=entry_font, 
            width=30,
            state="readonly"  # Hacer que el campo sea de solo lectura
        )
        restricciones_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
    
        
        # Campo para las materias (ahora con ComboBox y lista)
        materias_frame = tk.Frame(parent, bg="#f0f0f0")
        materias_frame.pack(fill=tk.X, pady=5)
        
        materias_label = tk.Label(materias_frame, text="Materias:", font=label_font, bg="#f0f0f0", width=15, anchor="w")
        materias_label.pack(side=tk.LEFT)
        
        # Frame para el ComboBox y la lista de materias seleccionadas
        materias_input_frame = tk.Frame(materias_frame, bg="#f0f0f0")
        materias_input_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # ComboBox para buscar materias
        self.materia_combobox = ttk.Combobox(
            materias_input_frame, 
            textvariable=self.materia_search,
            font=entry_font,
            width=30
        )
        self.materia_combobox.pack(side=tk.TOP, fill=tk.X, pady=(0, 5))
        
        # Vincular eventos al ComboBox
        self.materia_combobox.bind("<KeyRelease>", self.filter_materias)
        self.materia_combobox.bind("<<ComboboxSelected>>", self.add_materia_seleccionada)
        
        # Frame para mostrar materias seleccionadas
        materias_seleccionadas_frame = tk.Frame(materias_input_frame, bg="#f0f0f0", bd=1, relief=tk.SUNKEN)
        materias_seleccionadas_frame.pack(side=tk.TOP, fill=tk.X, expand=True)
        
        # Listbox para mostrar materias seleccionadas
        self.materias_seleccionadas_listbox = tk.Listbox(
            materias_seleccionadas_frame,
            height=4,
            font=entry_font,
            selectmode=tk.SINGLE
        )
        self.materias_seleccionadas_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Scrollbar para la lista de materias seleccionadas
        materias_scrollbar = ttk.Scrollbar(materias_seleccionadas_frame, orient="vertical", command=self.materias_seleccionadas_listbox.yview)
        materias_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.materias_seleccionadas_listbox.config(yscrollcommand=materias_scrollbar.set)
        
        # Botón para eliminar materia seleccionada
        remove_materia_button = tk.Button(
            materias_input_frame,
            text="Eliminar Materia",
            command=self.remove_materia_seleccionada,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 8),
            padx=5,
            pady=2
        )
        remove_materia_button.pack(side=tk.TOP, fill=tk.X, pady=(5, 0))
        
        # Botones de formulario
        form_buttons_frame = tk.Frame(parent, bg="#f0f0f0")
        form_buttons_frame.pack(fill=tk.X, pady=(20, 5))
        
        # Botón para limpiar el formulario
        clear_button = tk.Button(
            form_buttons_frame,
            text="Limpiar Formulario",
            command=self.clear_form,
            bg="#f44336",
            fg="white",
            font=("Arial", 10),
            padx=10,
            pady=5
        )
        clear_button.pack(side=tk.RIGHT, padx=5)
        
        # Botón para guardar (crear o actualizar)
        save_button = tk.Button(
            form_buttons_frame,
            text="Guardar Docente",
            command=self.save_docente,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 10),
            padx=10,
            pady=5
        )
        save_button.pack(side=tk.RIGHT, padx=5)
    
    def create_table(self, parent):
        # Frame para la tabla y scrollbar
        table_container = tk.Frame(parent)
        table_container.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbar vertical
        scrollbar_y = ttk.Scrollbar(table_container)
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Scrollbar horizontal
        scrollbar_x = ttk.Scrollbar(table_container, orient="horizontal")
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Estilo para la tabla
        style = ttk.Style()
        style.configure("Treeview", font=("Arial", 10))
        style.configure("Treeview.Heading", font=("Arial", 10, "bold"))
        
        # Crear tabla
        self.table = ttk.Treeview(
            table_container,
            columns=("id", "cc", "nombre", "restricciones", "materias"),
            show="headings",
            yscrollcommand=scrollbar_y.set,
            xscrollcommand=scrollbar_x.set
        )
        
        # Configurar scrollbars
        scrollbar_y.config(command=self.table.yview)
        scrollbar_x.config(command=self.table.xview)
        
        # Configurar columnas
        self.table.heading("id", text="ID")
        self.table.heading("cc", text="Cédula")
        self.table.heading("nombre", text="Nombre")
        self.table.heading("restricciones", text="Restricciones")
        self.table.heading("materias", text="Materias")
        
        self.table.column("id", width=30, anchor="center", minwidth=30)
        self.table.column("cc", width=80, anchor="center", minwidth=70)
        self.table.column("nombre", width=160, anchor="w", stretch=True, minwidth=140)
        self.table.column("restricciones", width=90, anchor="w", minwidth=80)
        self.table.column("materias", width=300, anchor="w", stretch=True, minwidth=200)
        
        # Empaquetar tabla
        self.table.pack(fill=tk.BOTH, expand=True)
        
        # Vincular evento de selección
        self.table.bind("<<TreeviewSelect>>", self.on_table_select)
    
    def create_action_buttons(self, parent):
        # Frame para contener los botones
        buttons_container = tk.Frame(parent, bg="#f0f0f0")
        buttons_container.pack(fill=tk.X)
        
        # Frame izquierdo para botones de navegación
        left_buttons = tk.Frame(buttons_container, bg="#f0f0f0")
        left_buttons.pack(side=tk.LEFT)
        
        # Frame derecho para botones de acción
        right_buttons = tk.Frame(buttons_container, bg="#f0f0f0")
        right_buttons.pack(side=tk.RIGHT)
        
        # Botón para regresar a la pantalla principal
        back_button = tk.Button(
            left_buttons,
            text="Regresar",
            command=self.volver_al_home,
            bg="#607D8B",  # Gris azulado
            fg="white",
            font=("Arial", 10),
            padx=15,
            pady=8
        )
        back_button.pack(side=tk.LEFT, padx=5)
        
        # Botón para actualizar la lista
        refresh_button = tk.Button(
            left_buttons,
            text="Actualizar Lista",
            command=self.load_docentes,
            bg="#2196F3",
            fg="white",
            font=("Arial", 10),
            padx=15,
            pady=8
        )
        refresh_button.pack(side=tk.LEFT, padx=5)
        
        # Botón para eliminar docente
        delete_button = tk.Button(
            right_buttons,
            text="Eliminar Docente",
            command=self.delete_docente,
            bg="#f44336",
            fg="white",
            font=("Arial", 10),
            padx=15,
            pady=8
        )
        delete_button.pack(side=tk.RIGHT, padx=5)
        
        # Botón para buscar por cédula
        search_button = tk.Button(
            right_buttons,
            text="Buscar por Cédula",
            command=self.search_by_cc,
            bg="#FF9800",
            fg="white",
            font=("Arial", 10),
            padx=15,
            pady=8
        )
        search_button.pack(side=tk.RIGHT, padx=5)

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

        
    
    def clear_form(self):
        """Limpia todos los campos del formulario"""
        self.docente_id.set("")
        self.cc.set("")
        self.nombre.set("")
        self.restricciones.set("")
        self.materias.set("")
        self.materia_search.set("")
        
        # Limpiar checkboxes de restricciones
        self.restriccion_manana.set(False)
        self.restriccion_tarde.set(False)
        self.restriccion_noche.set(False)
        
        self.materias_seleccionadas = []
        self.materias_seleccionadas_listbox.delete(0, tk.END)
        self.selected_docente = None
    
    def actualizar_restricciones(self):
        """Actualiza la variable restricciones basada en los checkboxes seleccionados"""
        restricciones = []
        
        # Contar cuántas restricciones están seleccionadas
        count = 0
        if self.restriccion_manana.get():
            count += 1
            restricciones.append("mañana")
        
        if self.restriccion_tarde.get():
            count += 1
            restricciones.append("tarde")
        
        if self.restriccion_noche.get():
            count += 1
            restricciones.append("noche")
        
        # Si hay más de 2 restricciones seleccionadas, mostrar mensaje y desmarcar la última
        if count > 2:
            messagebox.showwarning("Advertencia", "Solo se permiten máximo 2 restricciones")
            
            # Determinar cuál fue la última restricción marcada y desmarcarlo
            if self.restriccion_noche.get() and "noche" not in self.restricciones.get().split(","):
                self.restriccion_noche.set(False)
                restricciones.remove("noche")
            elif self.restriccion_tarde.get() and "tarde" not in self.restricciones.get().split(","):
                self.restriccion_tarde.set(False)
                restricciones.remove("tarde")
            elif self.restriccion_manana.get() and "mañana" not in self.restricciones.get().split(","):
                self.restriccion_manana.set(False)
                restricciones.remove("mañana")
        
        # Actualizar la variable restricciones
        self.restricciones.set(",".join(restricciones))
    
    def on_table_select(self, event):
        """Maneja el evento de selección en la tabla"""
        selected_items = self.table.selection()
        if not selected_items:
            return
        
        # Obtener el item seleccionado
        item = selected_items[0]
        values = self.table.item(item, "values")
        
        # Guardar el docente seleccionado
        self.selected_docente = {
            "id": values[0],
            "cc": values[1],
            "nombre": values[2],
            "restricciones": values[3],
            "materias": values[4]
        }
        
        # Actualizar el formulario
        self.docente_id.set(values[0])
        self.cc.set(values[1])
        self.nombre.set(values[2])
        self.restricciones.set(values[3])
        
        # Actualizar checkboxes de restricciones
        restricciones_list = values[3].split(",") if values[3] else []
        self.restriccion_manana.set("mañana" in restricciones_list)
        self.restriccion_tarde.set("tarde" in restricciones_list)
        self.restriccion_noche.set("noche" in restricciones_list)
        
        # Actualizar materias seleccionadas
        self.materias_seleccionadas = []
        self.materias_seleccionadas_listbox.delete(0, tk.END)
        
        # Obtener el docente completo del backend para tener acceso a los IDs de materias
        try:
            response = requests.get(f"{BASE_URL}docentes/get-by-id/{values[0]}")
            if response.status_code == 200:
                docente_completo = response.json()
                if docente_completo.get("materias"):
                    for materia in docente_completo.get("materias"):
                        self.materias_seleccionadas.append(materia)
                        self.materias_seleccionadas_listbox.insert(tk.END, f"{materia['nombre']} ({materia['codigo']})")
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar detalles del docente: {str(e)}")
        
        # Actualizar la variable materias para mantener compatibilidad
        self.materias.set(values[4])
    
    def load_docentes(self):
        """Carga todos los docentes desde el backend"""
        try:
            # Limpiar tabla
            for item in self.table.get_children():
                self.table.delete(item)
            
            # Realizar petición al backend
            response = requests.get(f"{BASE_URL}docentes/get-docentes")
            
            # Verificar si la petición fue exitosa
            if response.status_code == 200:
                docentes = response.json()
                
                # Llenar tabla con los datos
                for docente in docentes:
                    # Convertir listas a strings para mostrar en la tabla
                    restricciones_str = ",".join(docente.get("restricciones", [])) if docente.get("restricciones") else ""
                    
                    # Procesar materias para mostrar solo los nombres
                    materias_nombres = []
                    if docente.get("materias"):
                        for materia in docente.get("materias"):
                            if isinstance(materia, dict) and "nombre" in materia:
                                materias_nombres.append(materia["nombre"])
                    materias_str = ",".join(materias_nombres)
                    
                    self.table.insert("", "end", values=(
                        docente.get("id", ""),
                        docente.get("cc", ""),
                        docente.get("nombre", ""),
                        restricciones_str,
                        materias_str
                    ))
            else:
                # Mostrar mensaje de error con detalles
                try:
                    error_detail = response.json().get("detail", "")
                    error_message = f"Error al cargar docentes: {response.status_code}"
                    if error_detail:
                        error_message += f" - {error_detail}"
                    messagebox.showerror("Error", error_message)
                except:
                    messagebox.showerror("Error", f"Error al cargar docentes: {response.status_code} - {response.text}")
        
        except requests.exceptions.ConnectionError:
            messagebox.showerror("Error de Conexión", "No se pudo conectar al servidor. Verifique que el backend esté en ejecución en localhost:8000.")
        except Exception as e:
            messagebox.showerror("Error", f"Error inesperado: {str(e)}")
            
            # Mostrar mensaje en la tabla para indicar que no hay datos disponibles
            self.table.insert("", "end", values=("", "", "No hay datos disponibles", "", ""))
            
    def load_materias(self):
        """Carga las materias desde el backend"""
        try:
            response = requests.get(f"{BASE_URL}materias/get-materias")
            if response.status_code == 200:
                self.materias_list = response.json()
                
                # Actualizar el ComboBox con los nombres de las materias
                self.update_materias_combobox()
                return self.materias_list
            else:
                messagebox.showerror("Error", f"Error al cargar materias: {response.status_code}")
                return []
        except requests.exceptions.ConnectionError:
            messagebox.showerror("Error de Conexión", "No se pudo conectar al servidor. Verifique que el backend esté en ejecución en localhost:8000.")
            return []
    
    def update_materias_combobox(self):
        """Actualiza el ComboBox con la lista completa de materias"""
        if hasattr(self, 'materia_combobox'):
            materias_nombres = [f"{materia['nombre']} ({materia['codigo']})" for materia in self.materias_list]
            self.materia_combobox['values'] = materias_nombres
    
    def filter_materias(self, event):
        """Filtra las materias según el texto ingresado en el ComboBox"""
        search_text = self.materia_search.get().lower()
        
        if not search_text:
            # Si no hay texto de búsqueda, mostrar todas las materias
            self.update_materias_combobox()
            return
        
        # Filtrar materias que coincidan con el texto de búsqueda
        filtered_materias = [
            f"{materia['nombre']} ({materia['codigo']})" 
            for materia in self.materias_list 
            if search_text in materia['nombre'].lower() or search_text in materia['codigo'].lower()
        ]
        
        # Actualizar el ComboBox con las materias filtradas
        self.materia_combobox['values'] = filtered_materias
        
        # Mostrar la lista desplegable
        self.materia_combobox.event_generate('<Down>')
    
    def add_materia_seleccionada(self, event):
        """Agrega una materia a la lista de materias seleccionadas"""
        selected_text = self.materia_search.get()
        
        if not selected_text:
            return
        
        # Buscar la materia seleccionada en la lista de materias
        selected_materia = None
        for materia in self.materias_list:
            materia_text = f"{materia['nombre']} ({materia['codigo']})"
            if materia_text == selected_text:
                selected_materia = materia
                break
        
        if not selected_materia:
            return
        
        # Verificar si la materia ya está seleccionada
        for materia in self.materias_seleccionadas:
            if materia['id'] == selected_materia['id']:
                messagebox.showinfo("Información", "Esta materia ya está seleccionada")
                self.materia_search.set("")
                return
        
        # Agregar la materia a la lista de seleccionadas
        self.materias_seleccionadas.append(selected_materia)
        self.materias_seleccionadas_listbox.insert(tk.END, selected_text)
        
        # Actualizar la variable materias para mantener compatibilidad
        materias_ids = [str(materia['id']) for materia in self.materias_seleccionadas]
        self.materias.set(",".join(materias_ids))
        
        # Limpiar el campo de búsqueda
        self.materia_search.set("")
    
    def remove_materia_seleccionada(self):
        """Elimina una materia de la lista de materias seleccionadas"""
        selected_index = self.materias_seleccionadas_listbox.curselection()
        
        if not selected_index:
            messagebox.showinfo("Información", "Seleccione una materia para eliminar")
            return
        
        # Eliminar la materia de la lista y del listbox
        index = selected_index[0]
        self.materias_seleccionadas.pop(index)
        self.materias_seleccionadas_listbox.delete(index)
        
        # Actualizar la variable materias para mantener compatibilidad
        materias_ids = [str(materia['id']) for materia in self.materias_seleccionadas]
        self.materias.set(",".join(materias_ids))

    def save_docente(self):
        """Guarda (crea o actualiza) un docente"""
        # Validar campos obligatorios
        if not self.cc.get() or not self.nombre.get():
            messagebox.showerror("Error", "Los campos Cédula y Nombre son obligatorios")
            return
        
        # Validar que la cédula solo contenga números
        if not self.cc.get().isdigit():
            messagebox.showerror("Error", "La cédula debe contener solo números")
            return
            
        # Validar que no haya más de 2 restricciones
        restricciones = self.restricciones.get().split(",") if self.restricciones.get() else []
        if len(restricciones) > 2:
            messagebox.showerror("Error", "Solo se permiten máximo 2 restricciones")
            return
        
        # Validar que al menos una materia esté seleccionada
        if not self.materias_seleccionadas:
            messagebox.showerror("Error", "Debe seleccionar al menos una materia")
            return
        
        try:
            # Preparar datos
            docente_data = {
                "cc": int(self.cc.get()),
                "nombre": self.nombre.get(),
                "restricciones": self.restricciones.get().split(",") if self.restricciones.get() else None,
                "materias": [int(materia['id']) for materia in self.materias_seleccionadas] if self.materias_seleccionadas else None
            }
            
            # Determinar si es crear o actualizar
            if self.docente_id.get():
                # Actualizar docente existente
                docente_id = int(self.docente_id.get())
                response = requests.put(f"{BASE_URL}docentes/update/{docente_id}", json=docente_data)
                success_message = "Docente actualizado correctamente"
            else:
                # Crear nuevo docente
                response = requests.post(f"{BASE_URL}docentes/create", json=docente_data)
                success_message = "Docente creado correctamente"
            
            # Verificar respuesta
            if response.status_code in [200, 201]:
                messagebox.showinfo("Éxito", success_message)
                self.clear_form()
                self.load_docentes()
            else:
                # Mostrar mensaje de error
                error_detail = response.json().get("detail", "Error desconocido")
                messagebox.showerror("Error", f"Error al guardar docente: {response.status_code} - {error_detail}")
        
        except requests.exceptions.ConnectionError:
            messagebox.showerror("Error de Conexión", "No se pudo conectar al servidor. Verifique que el backend esté en ejecución en localhost:8000.")
        except ValueError as e:
            messagebox.showerror("Error de Validación", f"Error en los datos: {str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"Error inesperado: {str(e)}")
    
    def delete_docente(self):
        """Elimina un docente seleccionado"""
        if not self.docente_id.get():
            messagebox.showerror("Error", "Debe seleccionar un docente para eliminar")
            return
        
        # Confirmar eliminación
        if not messagebox.askyesno("Confirmar", "¿Está seguro de eliminar este docente?"):
            return
        
        try:
            # Realizar petición al backend
            docente_id = int(self.docente_id.get())
            response = requests.delete(f"{BASE_URL}docentes/delete/{docente_id}")
            
            # Verificar respuesta
            if response.status_code == 200:
                messagebox.showinfo("Éxito", "Docente eliminado correctamente")
                self.clear_form()
                self.load_docentes()
            else:
                # Mostrar mensaje de error
                error_detail = response.json().get("detail", "Error desconocido")
                messagebox.showerror("Error", f"Error al eliminar docente: {response.status_code} - {error_detail}")
        
        except requests.exceptions.ConnectionError:
            messagebox.showerror("Error de Conexión", "No se pudo conectar al servidor. Verifique que el backend esté en ejecución en localhost:8000.")
        except Exception as e:
            messagebox.showerror("Error", f"Error inesperado: {str(e)}")
            
    def validate_only_numbers(self, value):
        """Valida que el valor ingresado solo contenga números"""
        if value == "" or value.isdigit():
            return True
        return False
    
    def search_by_cc(self):
        """Busca un docente por su cédula"""
        # Solicitar la cédula al usuario
        cc = simpledialog.askstring("Buscar Docente", "Ingrese la cédula del docente:")
        
        if not cc:
            return
        
        try:
            # Realizar petición al backend
            response = requests.get(f"{BASE_URL}docentes/get-by-cc/{cc}")
            
            # Verificar si la petición fue exitosa
            if response.status_code == 200:
                docente = response.json()
                
                # Limpiar tabla
                for item in self.table.get_children():
                    self.table.delete(item)
                
                # Convertir listas a strings para mostrar en la tabla
                restricciones_str = ",".join(docente.get("restricciones", [])) if docente.get("restricciones") else ""
                
                # Procesar materias para mostrar solo los nombres
                materias_nombres = []
                if docente.get("materias"):
                    for materia in docente.get("materias"):
                        if isinstance(materia, dict) and "nombre" in materia:
                            materias_nombres.append(materia["nombre"])
                materias_str = ",".join(materias_nombres)
                
                # Insertar el docente en la tabla
                self.table.insert("", "end", values=(
                    docente.get("id", ""),
                    docente.get("cc", ""),
                    docente.get("nombre", ""),
                    restricciones_str,
                    materias_str
                ))
                
                # Seleccionar el docente en la tabla
                self.table.selection_set(self.table.get_children()[0])
                self.on_table_select(None)  # Simular selección para cargar datos en el formulario
            else:
                # Mostrar mensaje de error
                try:
                    error_detail = response.json().get("detail", "")
                    messagebox.showerror("Error", f"No se encontró ningún docente con la cédula {cc}. {error_detail}")
                except:
                    messagebox.showerror("Error", f"No se encontró ningún docente con la cédula {cc}.")
        except Exception as e:
            messagebox.showerror("Error", f"Error al buscar docente: {str(e)}")
    
    def run(self):
        """Inicia el bucle principal de la aplicación"""
        if self.is_main_window:
            self.root.mainloop()

if __name__ == "__main__":
    app = DocentesScreen()
    app.run()


    