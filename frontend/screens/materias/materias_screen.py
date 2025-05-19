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

class MateriasScreen:
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
            
        self.root.title("Gestión de Materias")
        self.root.geometry("1000x700")
        self.root.configure(bg="#f0f0f0")
        
        # Variables para el formulario
        self.materia_id = tk.StringVar()
        self.codigo = tk.StringVar()
        self.nombre = tk.StringVar()
        self.cantidad_horas = tk.StringVar(value="2")  # Valor por defecto 2
        self.requiere_sala_sistemas = tk.BooleanVar()
        
        self.setup_ui()
        self.load_materias()
        self.center_window()

    def setup_ui(self):
        # Configurar el estilo de la ventana
        self.style = ttk.Style()
        self.style.theme_use('clam')  # Tema base más personalizable
        
        # Configurar estilo para el Combobox
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
            text="Sistema de Gestión de Materias", 
            font=title_font,
            bg="#f0f0f0",
            fg="#333333"
        )
        title_label.pack(pady=(0, 20))
        
        # Frame para el formulario (izquierda) y la tabla (derecha)
        content_frame = tk.Frame(main_frame, bg="#f0f0f0")
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Frame para el formulario (izquierda)
        form_frame = tk.LabelFrame(content_frame, text="Formulario de Materia", bg="#f0f0f0", padx=15, pady=15, width=400)
        form_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=(0, 10))
        form_frame.pack_propagate(False)
        
        # Frame para la tabla (derecha)
        table_frame = tk.LabelFrame(content_frame, text="Lista de Materias", bg="#f0f0f0", padx=15, pady=15)
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
        
        id_entry = tk.Entry(id_frame, textvariable=self.materia_id, font=entry_font, state="readonly", width=20)
        id_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Remove the codigo entry field
        # Campo para el nombre
        nombre_frame = tk.Frame(parent, bg="#f0f0f0")
        nombre_frame.pack(fill=tk.X, pady=5)
        
        nombre_label = tk.Label(nombre_frame, text="Nombre:", font=label_font, bg="#f0f0f0", width=15, anchor="w")
        nombre_label.pack(side=tk.LEFT)
        
        nombre_entry = tk.Entry(nombre_frame, textvariable=self.nombre, font=entry_font, width=30)
        nombre_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Combo para la cantidad de horas
        horas_frame = tk.Frame(parent, bg="#f0f0f0")
        horas_frame.pack(fill=tk.X, pady=5)
        
        horas_label = tk.Label(horas_frame, text="Cantidad de Horas:", 
                            font=label_font, bg="#f0f0f0", width=15, anchor="w")
        horas_label.pack(side=tk.LEFT)
        
        horas_combobox = ttk.Combobox(
            horas_frame,
            textvariable=self.cantidad_horas,
            values=["2", "3", "4"],  # Valores permitidos
            state="readonly",  # Solo selección de lista
            font=entry_font,
            width=28
        )
        horas_combobox.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Checkbox para requerir sala de sistemas
        sistemas_frame = tk.Frame(parent, bg="#f0f0f0")
        sistemas_frame.pack(fill=tk.X, pady=5)
        
        sistemas_checkbox = tk.Checkbutton(
            sistemas_frame, 
            text="Requiere Sala de Sistemas", 
            variable=self.requiere_sala_sistemas, 
            bg="#f0f0f0"
        )
        sistemas_checkbox.pack(side=tk.LEFT, anchor="w")
        
        # Botón para limpiar el formulario (NUEVO)
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
            columns=("id", "codigo", "nombre", "cantidad_horas", "requiere_sala_sistemas"),
            show="headings",
            yscrollcommand=scrollbar_y.set,
            xscrollcommand=scrollbar_x.set
        )
        
        # Configurar scrollbars
        scrollbar_y.config(command=self.table.yview)
        scrollbar_x.config(command=self.table.xview)
        
        # Configurar columnas
        self.table.heading("id", text="ID")
        self.table.heading("codigo", text="Código")
        self.table.heading("nombre", text="Nombre")
        self.table.heading("cantidad_horas", text="Horas")
        self.table.heading("requiere_sala_sistemas", text="Sala de Sistemas")
        
        self.table.column("id", width=30, anchor="center", minwidth=30)
        self.table.column("codigo", width=80, anchor="center", minwidth=70)
        self.table.column("nombre", width=160, anchor="w", stretch=True, minwidth=140)
        self.table.column("cantidad_horas", width=90, anchor="center", minwidth=80)
        self.table.column("requiere_sala_sistemas", width=120, anchor="center", minwidth=100)
        
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
            command=self.load_materias,
            bg="#2196F3",
            fg="white",
            font=("Arial", 10),
            padx=15,
            pady=8
        )
        refresh_button.pack(side=tk.LEFT, padx=5)
        
        # Botón para eliminar materia
        delete_button = tk.Button(
            right_buttons,
            text="Eliminar Materia",
            command=self.delete_materia,
            bg="#f44336",
            fg="white",
            font=("Arial", 10),
            padx=15,
            pady=8
        )
        delete_button.pack(side=tk.RIGHT, padx=5)
        
        # Botón para guardar materia
        save_button = tk.Button(
            right_buttons,
            text="Guardar Materia",
            command=self.save_materia,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 10),
            padx=15,
            pady=8
        )
        save_button.pack(side=tk.RIGHT, padx=5)

    def volver_al_home(self):
        """Utiliza el callback para volver a la pantalla principal"""
        if self.show_home_callback:
            self.show_home_callback()
        else:
            self.return_to_home()
    
    def return_to_home(self):
        """Cierra la ventana actual y regresa a la pantalla principal"""
        if not self.is_main_window:
            self.root.destroy()  # Esto activará el protocolo WM_DELETE_WINDOW

    def load_materias(self):
        """Carga todas las materias desde el backend"""
        try:
            # Limpiar tabla
            for item in self.table.get_children():
                self.table.delete(item)
            
            # Realizar petición al backend
            response = requests.get(f"{BASE_URL}materias/get-materias")
            
            # Verificar si la petición fue exitosa
            if response.status_code == 200:
                materias = response.json()
                
                # Llenar tabla con los datos
                for materia in materias:
                    self.table.insert("", "end", values=(
                        materia.get("id", ""),
                        materia.get("codigo", ""),
                        materia.get("nombre", ""),
                        materia.get("cantidad_horas", ""),
                        "Sí" if materia.get("requiere_sala_sistemas") else "No"
                    ))
            else:
                # Mostrar mensaje de error con detalles
                try:
                    error_detail = response.json().get("detail", "")
                    error_message = f"Error al cargar materias: {response.status_code}"
                    if error_detail:
                        error_message += f" - {error_detail}"
                    messagebox.showerror("Error", error_message)
                except:
                    messagebox.showerror("Error", f"Error al cargar materias: {response.status_code} - {response.text}")
        
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
        self.materia_id.set(values[0])
        self.codigo.set(values[1])
        self.nombre.set(values[2])
        self.cantidad_horas.set(values[3])
        self.requiere_sala_sistemas.set(values[4] == "Sí")

    def save_materia(self):
        """Guarda (crea o actualiza) una materia"""
        if not self.nombre.get():
            messagebox.showerror("Error", "El campo Nombre es obligatorio")
            return
        
        # Validar horas
        try:
            horas = int(self.cantidad_horas.get())
            if horas not in [2, 3, 4]:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Seleccione una cantidad válida de horas (2, 3 o 4)")
            return

        try:
            materia_data = {
                "nombre": self.nombre.get(),
                "cantidad_horas": self.cantidad_horas.get(),
                "requiere_sala_sistemas": self.requiere_sala_sistemas.get()
            }

            if self.materia_id.get():
                materia_id = int(self.materia_id.get())
                materia_data["codigo"] = self.codigo.get()
                response = requests.put(f"{BASE_URL}materias/update/{materia_id}", json=materia_data)
                success_message = "Materia actualizada correctamente"
            else:
                response = requests.get(f"{BASE_URL}materias/get-materias")
                if response.status_code == 200:
                    materias = response.json()
                    max_num = 0

                    for materia in materias:
                        codigo = materia.get("codigo", "")
                        if "-" in codigo:
                            parts = codigo.split("-")
                            if len(parts) == 2:
                                try:
                                    current_num = int(parts[1])
                                    if current_num > max_num:
                                        max_num = current_num
                                except ValueError:
                                    continue

                    nombre_prefix = self.nombre.get()[:3].upper()
                    nuevo_numero = max_num + 1
                    materia_data["codigo"] = f"{nombre_prefix}-{nuevo_numero:03d}"

                    response = requests.post(f"{BASE_URL}materias/create", json=materia_data)
                    success_message = "Materia creada correctamente"
                else:
                    messagebox.showerror("Error", "No se pudo obtener las materias existentes")
                    return

            if response.status_code in [200, 201]:
                messagebox.showinfo("Éxito", success_message)
                self.clear_form()
                self.load_materias()
            else:
                error_detail = response.json().get("detail", "Error desconocido")
                messagebox.showerror("Error", f"Error al guardar: {response.status_code} - {error_detail}")

        except requests.exceptions.ConnectionError:
            messagebox.showerror("Error", "No se pudo conectar al servidor")
        except Exception as e:
            messagebox.showerror("Error", f"Error inesperado: {str(e)}")
    
    def delete_materia(self):
        """Elimina una materia seleccionada"""
        if not self.materia_id.get():
            messagebox.showerror("Error", "Debe seleccionar una materia para eliminar")
            return
        
        # Confirmar eliminación
        if not messagebox.askyesno("Confirmar", "¿Está seguro de eliminar esta materia?"):
            return
        
        try:
            # Realizar petición al backend
            materia_id = int(self.materia_id.get())
            response = requests.delete(f"{BASE_URL}materias/delete/{materia_id}")
            
            # Verificar respuesta
            if response.status_code == 200:
                messagebox.showinfo("Éxito", "Materia eliminada correctamente")
                self.clear_form()
                self.load_materias()
            else:
                # Mostrar mensaje de error
                error_detail = response.json().get("detail", "Error desconocido")
                messagebox.showerror("Error", f"Error al eliminar materia: {response.status_code} - {error_detail}")
        
        except requests.exceptions.ConnectionError:
            messagebox.showerror("Error de Conexión", "No se pudo conectar al servidor. Verifique que el backend esté en ejecución en localhost:8000.")
        except Exception as e:
            messagebox.showerror("Error", f"Error inesperado: {str(e)}")

    def clear_form(self):
        """Limpia todos los campos del formulario"""
        self.materia_id.set("")
        self.codigo.set("")
        self.nombre.set("")
        self.cantidad_horas.set("2") 
        self.requiere_sala_sistemas.set(False)
        
        # Deseleccionar cualquier elemento de la tabla
        if self.table.selection():
            self.table.selection_remove(self.table.selection()[0])

    def center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'+{x}+{y}')
    
    def run(self):
        """Inicia el bucle principal de la aplicación"""
        if self.is_main_window:
            self.root.mainloop()

if __name__ == "__main__":
    app = MateriasScreen()
    app.run()


    