import tkinter as tk
from tkinter import messagebox, font
import requests
import os
import sys

# Agregar la ruta del proyecto al path para poder importar módulos
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

# URL base para las peticiones al backend
BASE_URL = "http://localhost:8000/"

class HorariosScreen:
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
            
        self.root.title("Gestión de Horarios")
        self.root.geometry("600x400")
        self.root.configure(bg="#f0f0f0")
        
        # Variable para controlar si hay cursos generados
        self.hay_cursos = False
        
        # Configurar el estilo de la ventana
        self.setup_ui()
        
        # Verificar si hay cursos generados
        self.verificar_cursos()
        
    def setup_ui(self):
        # Frame principal
        main_frame = tk.Frame(self.root, bg="#f0f0f0", padx=30, pady=30)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        title_font = font.Font(family="Arial", size=20, weight="bold")
        title_label = tk.Label(
            main_frame, 
            text="Gestión de Horarios Automáticos", 
            font=title_font,
            bg="#f0f0f0",
            fg="#333333"
        )
        title_label.pack(pady=(0, 30))
        
        # Descripción
        description_font = font.Font(family="Arial", size=12)
        description_text = (
            "Esta herramienta permite generar horarios automáticamente basados en los docentes, "
            "materias y salones disponibles en el sistema. También puede eliminar todos los "
            "horarios generados para comenzar de nuevo."
        )
        description_label = tk.Label(
            main_frame,
            text=description_text,
            font=description_font,
            bg="#f0f0f0",
            fg="#555555",
            wraplength=500,
            justify="center"
        )
        description_label.pack(pady=(0, 30))
        
        # Frame para los botones
        buttons_frame = tk.Frame(main_frame, bg="#f0f0f0")
        buttons_frame.pack(fill=tk.X, expand=True)
        
        # Botón para regresar
        back_button = tk.Button(
            buttons_frame,
            text="Regresar",
            command=self.volver_al_home,
            bg="#607D8B",  # Gris azulado
            fg="white",
            font=("Arial", 12),
            padx=15,
            pady=8,
            width=15
        )
        back_button.pack(side=tk.LEFT, padx=10)
        
        # Botón para generar horarios
        self.generar_button = tk.Button(
            buttons_frame,
            text="Generar Horarios",
            command=self.generar_horarios,
            bg="#4CAF50",  # Verde
            fg="white",
            font=("Arial", 12),
            padx=15,
            pady=8,
            width=15
        )
        self.generar_button.pack(side=tk.RIGHT, padx=10)
        
        # Botón para limpiar horarios
        self.limpiar_button = tk.Button(
            buttons_frame,
            text="Limpiar Horarios",
            command=self.limpiar_horarios,
            bg="#F44336",  # Rojo
            fg="white",
            font=("Arial", 12),
            padx=15,
            pady=8,
            width=15
        )
        self.limpiar_button.pack(side=tk.RIGHT, padx=10)
        
        # Estado de los horarios
        self.status_frame = tk.Frame(main_frame, bg="#f0f0f0", pady=20)
        self.status_frame.pack(fill=tk.X, expand=True, pady=20)
        
        self.status_label = tk.Label(
            self.status_frame,
            text="Estado: Verificando si hay horarios generados...",
            font=("Arial", 12),
            bg="#f0f0f0",
            fg="#333333"
        )
        self.status_label.pack()
        
        # Pie de página
        footer_label = tk.Label(
            main_frame,
            text="© 2023 Sistema de Gestión Académica - EAM",
            font=("Arial", 10),
            bg="#f0f0f0",
            fg="#888888"
        )
        footer_label.pack(side=tk.BOTTOM, pady=(20, 0))
    
    def verificar_cursos(self):
        """Verifica si hay cursos generados en el sistema"""
        try:
            # Realizar petición al backend para obtener cursos
            response = requests.get(f"{BASE_URL}cursos/detallados")
            
            # Verificar si hay cursos
            if response.status_code == 200:
                cursos = response.json()
                if cursos and len(cursos) > 0:
                    self.hay_cursos = True
                    self.status_label.config(text="Estado: Hay horarios generados en el sistema")
                    self.generar_button.config(state=tk.DISABLED)
                    self.limpiar_button.config(state=tk.NORMAL)
                else:
                    self.hay_cursos = False
                    self.status_label.config(text="Estado: No hay horarios generados en el sistema")
                    self.generar_button.config(state=tk.NORMAL)
                    self.limpiar_button.config(state=tk.DISABLED)
            else:
                self.status_label.config(text=f"Error al verificar horarios: {response.status_code}")
                self.hay_cursos = False
                self.generar_button.config(state=tk.NORMAL)
                self.limpiar_button.config(state=tk.DISABLED)
        except Exception as e:
            self.status_label.config(text=f"Error de conexión: {str(e)}")
            messagebox.showerror("Error", f"Error al verificar horarios: {str(e)}")
            self.hay_cursos = False
            self.generar_button.config(state=tk.NORMAL)
            self.limpiar_button.config(state=tk.DISABLED)
    
    def generar_horarios(self):
        """Genera horarios automáticamente"""
        if self.hay_cursos:
            messagebox.showinfo("Información", "Ya hay horarios generados. Debe limpiarlos primero.")
            return
        
        # Confirmar generación
        if not messagebox.askyesno("Confirmar", "¿Está seguro de generar horarios automáticamente?"):
            return
        
        try:
            # Realizar petición al backend
            response = requests.post(f"{BASE_URL}main/generar-horarios")
            
            # Verificar respuesta
            if response.status_code == 200:
                resultado = response.json()
                if resultado.get("exito", False):
                    messagebox.showinfo("Éxito", "Horarios generados correctamente")
                    self.hay_cursos = True
                    self.status_label.config(text="Estado: Hay horarios generados en el sistema")
                    self.generar_button.config(state=tk.DISABLED)
                    self.limpiar_button.config(state=tk.NORMAL)
                else:
                    messagebox.showerror("Error", f"Error al generar horarios: {resultado.get('mensaje', 'Error desconocido')}")
            else:
                # Mostrar mensaje de error
                try:
                    error_detail = response.json().get("detail", "")
                    messagebox.showerror("Error", f"Error al generar horarios: {response.status_code} - {error_detail}")
                except:
                    messagebox.showerror("Error", f"Error al generar horarios: {response.status_code} - {response.text}")
        
        except requests.exceptions.ConnectionError:
            messagebox.showerror("Error de Conexión", "No se pudo conectar al servidor. Verifique que el backend esté en ejecución en localhost:8000.")
        except Exception as e:
            messagebox.showerror("Error", f"Error inesperado: {str(e)}")
    
    def limpiar_horarios(self):
        """Limpia todos los horarios generados"""
        if not self.hay_cursos:
            messagebox.showinfo("Información", "No hay horarios para limpiar.")
            return
        
        # Confirmar eliminación
        if not messagebox.askyesno("Confirmar", "¿Está seguro de eliminar todos los horarios generados?"):
            return
        
        try:
            # Realizar petición al backend
            response = requests.delete(f"{BASE_URL}main/limpiar-horarios")
            
            # Verificar respuesta
            if response.status_code == 200:
                resultado = response.json()
                if resultado.get("exito", False):
                    messagebox.showinfo("Éxito", "Horarios eliminados correctamente")
                    self.hay_cursos = False
                    self.status_label.config(text="Estado: No hay horarios generados en el sistema")
                    self.generar_button.config(state=tk.NORMAL)
                    self.limpiar_button.config(state=tk.DISABLED)
                else:
                    messagebox.showerror("Error", f"Error al limpiar horarios: {resultado.get('mensaje', 'Error desconocido')}")
            else:
                # Mostrar mensaje de error
                try:
                    error_detail = response.json().get("detail", "")
                    messagebox.showerror("Error", f"Error al limpiar horarios: {response.status_code} - {error_detail}")
                except:
                    messagebox.showerror("Error", f"Error al limpiar horarios: {response.status_code} - {response.text}")
        
        except requests.exceptions.ConnectionError:
            messagebox.showerror("Error de Conexión", "No se pudo conectar al servidor. Verifique que el backend esté en ejecución en localhost:8000.")
        except Exception as e:
            messagebox.showerror("Error", f"Error inesperado: {str(e)}")
    
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
    
    def run(self):
        """Inicia el bucle principal de la aplicación"""
        if self.is_main_window:
            self.root.mainloop()

if __name__ == "__main__":
    app = HorariosScreen()
    app.run()