import tkinter as tk
from tkinter import ttk, messagebox, font
import requests
import os
import sys

# Agregar la ruta del proyecto al path para poder importar módulos
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

# URL base para las peticiones al backend
BASE_URL = "http://localhost:8000/"

class SalonesScreen:
    def __init__(self, root=None):
        # Si no se proporciona una raíz, crear una nueva ventana
        if root is None:
            self.root = tk.Tk()
            self.is_main_window = True
        else:
            self.root = root
            self.is_main_window = False
            
        self.root.title("Gestión de Salones")
        self.root.geometry("1000x700")
        self.root.configure(bg="#f0f0f0")
        
        # Variables para el formulario
        self.salon_id = tk.StringVar()
        self.bloque = tk.StringVar()
        self.numero = tk.IntVar()
        self.es_sistemas = tk.BooleanVar()
        
        # Configurar el estilo de la ventana
        self.setup_ui()
        
        # Cargar datos iniciales
        self.load_salones()

    def setup_ui(self):
        # Configurar el estilo de la ventana
        self.style = ttk.Style()
        self.style.theme_use('clam')  # Tema base para personalización
        
        # Configurar estilo para Combobox
        self.style.configure('TCombobox',
                            fieldbackground='white',
                            background='white',
                            foreground='black',
                            selectbackground='white',
                            selectforeground='black')
        
        self.style.map('TCombobox',
                    fieldbackground=[('readonly', 'white')],
                    selectbackground=[('readonly', 'white')],
                    selectforeground=[('readonly', 'black')])
        
        # Frame principal con dos columnas
        main_frame = tk.Frame(self.root, bg="#f0f0f0")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Título
        title_font = font.Font(family="Arial", size=18, weight="bold")
        title_label = tk.Label(
            main_frame, 
            text="Sistema de Gestión de Salones", 
            font=title_font,
            bg="#f0f0f0",
            fg="#333333"
        )
        title_label.pack(pady=(0, 20))
        
        # Frame para el formulario (izquierda) y la tabla (derecha)
        content_frame = tk.Frame(main_frame, bg="#f0f0f0")
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Frame para el formulario (izquierda)
        form_frame = tk.LabelFrame(content_frame, text="Formulario de Salón", bg="#f0f0f0", padx=15, pady=15, width=400)
        form_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=(0, 10))
        form_frame.pack_propagate(False)
        
        # Frame para la tabla (derecha)
        table_frame = tk.LabelFrame(content_frame, text="Lista de Salones", bg="#f0f0f0", padx=15, pady=15)
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
            text="© 2023 Sistema de Gestión Académica - EAM",
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
        
        id_entry = tk.Entry(id_frame, textvariable=self.salon_id, font=entry_font, state="readonly", width=20)
        id_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Campo para el bloque
        bloque_frame = tk.Frame(parent, bg="#f0f0f0")
        bloque_frame.pack(fill=tk.X, pady=5)
        
        bloque_label = tk.Label(bloque_frame, text="Bloque:", font=label_font, bg="#f0f0f0", width=12, anchor="w")
        bloque_label.pack(side=tk.LEFT)
        
        bloque_combobox = ttk.Combobox(
            bloque_frame,
            textvariable=self.bloque,
            values=["A", "B", "C"],
            state="readonly",
            font=entry_font,
            width=28
        )
        bloque_combobox.set("A")  # Valor por defecto
        bloque_combobox.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Campo para el número
        numero_frame = tk.Frame(parent, bg="#f0f0f0")
        numero_frame.pack(fill=tk.X, pady=5)
        
        numero_label = tk.Label(numero_frame, text="Número:", font=label_font, bg="#f0f0f0", width=15, anchor="w")
        numero_label.pack(side=tk.LEFT)
        
        numero_entry = tk.Entry(numero_frame, textvariable=self.numero, font=entry_font, width=30)
        numero_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Checkbox para es_sistemas
        sistemas_frame = tk.Frame(parent, bg="#f0f0f0")
        sistemas_frame.pack(fill=tk.X, pady=5)
        
        sistemas_checkbox = tk.Checkbutton(
            sistemas_frame, 
            text="Es Sala de Sistemas", 
            variable=self.es_sistemas, 
            bg="#f0f0f0"
        )
        sistemas_checkbox.pack(side=tk.LEFT, anchor="w")
        
        # Botón para limpiar el formulario
        clear_frame = tk.Frame(parent, bg="#f0f0f0")
        clear_frame.pack(fill=tk.X, pady=(15, 5))
        
        clear_button = tk.Button(
            clear_frame,
            text="Limpiar Campos",
            command=self.clear_form,
            bg="#FF9800",
            fg="white",
            font=("Arial", 10),
            width=15
        )
        clear_button.pack(side=tk.LEFT)

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
            columns=("id", "bloque", "numero", "es_sistemas"),
            show="headings",
            yscrollcommand=scrollbar_y.set,
            xscrollcommand=scrollbar_x.set
        )
        
        # Configurar scrollbars
        scrollbar_y.config(command=self.table.yview)
        scrollbar_x.config(command=self.table.xview)
        
        # Configurar columnas
        self.table.heading("id", text="ID")
        self.table.heading("bloque", text="Bloque")
        self.table.heading("numero", text="Número")
        self.table.heading("es_sistemas", text="Sala de Sistemas")
        
        self.table.column("id", width=30, anchor="center", minwidth=30)
        self.table.column("bloque", width=80, anchor="center", minwidth=70)
        self.table.column("numero", width=160, anchor="w", stretch=True, minwidth=140)
        self.table.column("es_sistemas", width=120, anchor="center", minwidth=100)
        
        # Empaquetar tabla
        self.table.pack(fill=tk.BOTH, expand=True)
        
        # Vincular evento de selección
        self.table.bind("<<TreeviewSelect>>", self.on_table_select)

    def create_action_buttons(self, parent):
        # Botón para actualizar la lista
        refresh_button = tk.Button(
            parent,
            text="Actualizar Lista",
            command=self.load_salones,
            bg="#2196F3",
            fg="white",
            font=("Arial", 10),
            padx=15,
            pady=8
        )
        refresh_button.pack(side=tk.LEFT, padx=5)
        
        # Botón para eliminar salón
        delete_button = tk.Button(
            parent,
            text="Eliminar Salón",
            command=self.delete_salon,
            bg="#f44336",
            fg="white",
            font=("Arial", 10),
            padx=15,
            pady=8
        )
        delete_button.pack(side=tk.RIGHT, padx=5)
        
        # Botón para guardar salón
        save_button = tk.Button(
            parent,
            text="Guardar Salón",
            command=self.save_salon,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 10),
            padx=15,
            pady=8
        )
        save_button.pack(side=tk.RIGHT, padx=5)

    def load_salones(self):
        """Carga todos los salones desde el backend"""
        try:
            # Limpiar tabla
            for item in self.table.get_children():
                self.table.delete(item)
            
            # Realizar petición al backend
            response = requests.get(f"{BASE_URL}salones/get-salones")
            
            # Verificar si la petición fue exitosa
            if response.status_code == 200:
                salones = response.json()
                
                # Ordenar por ID de forma ascendente
                salones_ordenados = sorted(salones, key=lambda x: x['id'])

                # Llenar tabla con los datos ordenados
                for salon in salones_ordenados:
                    self.table.insert("", "end", values=(
                        salon.get("id", ""),
                        salon.get("bloque", ""),
                        salon.get("numero", ""),
                        "Sí" if salon.get("es_sistemas") else "No"
                    ))
            else:
                # Mostrar mensaje de error con detalles
                try:
                    error_detail = response.json().get("detail", "")
                    error_message = f"Error al cargar salones: {response.status_code}"
                    if error_detail:
                        error_message += f" - {error_detail}"
                    messagebox.showerror("Error", error_message)
                except:
                    messagebox.showerror("Error", f"Error al cargar salones: {response.status_code} - {response.text}")
        
        except requests.exceptions.ConnectionError:
            messagebox.showerror("Error de Conexión", "No se pudo conectar al servidor. Verifique que el backend esté en ejecución en localhost:8000.")
        except Exception as e:
            messagebox.showerror("Error", f"Error inesperado: {str(e)}")
            
            # Mostrar mensaje en la tabla para indicar que no hay datos disponibles
            self.table.insert("", "end", values=("", "", "No hay datos disponibles", "", ""))

    def on_table_select(self, event):
        """Maneja el evento de selección en la tabla"""
        selected_items = self.table.selection()
        if not selected_items:
            return
        
        # Obtener el item seleccionado
        item = selected_items[0]
        values = self.table.item(item, "values")
        
        # Actualizar el formulario
        self.salon_id.set(values[0])
        self.bloque.set(values[1])
        self.numero.set(values[2])
        self.es_sistemas.set(values[3] == "Sí")

    def save_salon(self):
        """Guarda (crea o actualiza) un salón"""
        # Validar campos obligatorios
        if not self.bloque.get() or not self.numero.get():
            messagebox.showerror("Error", "Los campos Bloque y Número son obligatorios")
            return
        
        try:
            # Validar número único en el bloque
            response = requests.get(f"{BASE_URL}salones/get-salones")
            if response.status_code == 200:
                salones_existentes = response.json()
                current_id = int(self.salon_id.get()) if self.salon_id.get() else None
                
                # Verificar duplicados para nuevos registros y actualizaciones
                for salon in salones_existentes:
                    # Excluir el registro actual en actualizaciones
                    if current_id and salon['id'] == current_id:
                        continue
                        
                    if (str(salon['bloque']) == self.bloque.get() 
                        and str(salon['numero']) == str(self.numero.get())):
                        messagebox.showerror("Error", f"Ya existe el salón {self.bloque.get()}-{self.numero.get()}")
                        return
            
            # Preparar datos
            salon_data = {
                "bloque": self.bloque.get(),
                "numero": self.numero.get(),
                "es_sistemas": self.es_sistemas.get()
            }
            
            # Determinar si es crear o actualizar
            if self.salon_id.get():
                # Actualizar salón existente
                salon_id = int(self.salon_id.get())
                response = requests.put(f"{BASE_URL}salones/update/{salon_id}", json=salon_data)
                success_message = "Salón actualizado correctamente"
            else:
                # Crear nuevo salón
                response = requests.post(f"{BASE_URL}salones/create", json=salon_data)
                success_message = "Salón creado correctamente"
            
            # Verificar respuesta
            if response.status_code in [200, 201]:
                messagebox.showinfo("Éxito", success_message)
                self.clear_form()
                self.load_salones()
            else:
                # Mostrar mensaje de error
                error_detail = response.json().get("detail", "Error desconocido")
                messagebox.showerror("Error", f"Error al guardar salón: {response.status_code} - {error_detail}")
        
        except requests.exceptions.ConnectionError:
            messagebox.showerror("Error de Conexión", "No se pudo conectar al servidor. Verifique que el backend esté en ejecución en localhost:8000.")
        except ValueError as e:
            messagebox.showerror("Error de Validación", f"Error en los datos: {str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"Error inesperado: {str(e)}")

    def delete_salon(self):
        """Elimina un salón seleccionado"""
        if not self.salon_id.get():
            messagebox.showerror("Error", "Debe seleccionar un salón para eliminar")
            return
        
        # Confirmar eliminación
        if not messagebox.askyesno("Confirmar", "¿Está seguro de eliminar este salón?"):
            return
        
        try:
            # Realizar petición al backend
            salon_id = int(self.salon_id.get())
            response = requests.delete(f"{BASE_URL}salones/delete/{salon_id}")
            
            # Verificar respuesta
            if response.status_code == 200:
                messagebox.showinfo("Éxito", "Salón eliminado correctamente")
                self.clear_form()
                self.load_salones()
            else:
                # Mostrar mensaje de error
                error_detail = response.json().get("detail", "Error desconocido")
                messagebox.showerror("Error", f"Error al eliminar salón: {response.status_code} - {error_detail}")
        
        except requests.exceptions.ConnectionError:
            messagebox.showerror("Error de Conexión", "No se pudo conectar al servidor. Verifique que el backend esté en ejecución en localhost:8000.")
        except Exception as e:
            messagebox.showerror("Error", f"Error inesperado: {str(e)}")

    def clear_form(self):
        """Limpia todos los campos del formulario"""
        self.salon_id.set("")
        self.bloque.set("A")  # Reiniciar a valor por defecto
        self.numero.set(0)
        self.es_sistemas.set(False)
        
        # Deseleccionar cualquier elemento de la tabla
        if self.table.selection():
            self.table.selection_remove(self.table.selection()[0])

    def run(self):
        """Inicia el bucle principal de la aplicación"""
        if self.is_main_window:
            self.root.mainloop()

if __name__ == "__main__":
    app = SalonesScreen()
    app.run()