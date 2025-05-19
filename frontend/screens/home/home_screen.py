import tkinter as tk
from tkinter import messagebox, font
import os
import sys

# Agregar la ruta del proyecto al path para poder importar módulos
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

class HomeScreen:
    def __init__(self, root=None):
        # Si no se proporciona una raíz, crear una nueva ventana
        if root is None:
            self.root = tk.Tk()
            self.is_main_window = True
        else:
            self.root = root
            self.is_main_window = False
            
        self.root.title("Sistema de Gestión Académica")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")
        
        # Configurar el estilo de la ventana
        self.setup_ui()
        
    def setup_ui(self):
        # Frame principal
        main_frame = tk.Frame(self.root, bg="#f0f0f0", padx=30, pady=30)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        title_font = font.Font(family="Arial", size=24, weight="bold")
        title_label = tk.Label(
            main_frame, 
            text="Sistema de Gestión Académica", 
            font=title_font,
            bg="#f0f0f0",
            fg="#333333"
        )
        title_label.pack(pady=(0, 40))
        
        # Subtítulo
        subtitle_font = font.Font(family="Arial", size=14)
        subtitle_label = tk.Label(
            main_frame,
            text="Seleccione una opción para gestionar",
            font=subtitle_font,
            bg="#f0f0f0",
            fg="#555555"
        )
        subtitle_label.pack(pady=(0, 30))
        
        # Frame para los botones
        buttons_frame = tk.Frame(main_frame, bg="#f0f0f0")
        buttons_frame.pack(fill=tk.BOTH, expand=True)
        
        # Estilo de botones
        button_font = font.Font(family="Arial", size=12, weight="bold")
        button_width = 20
        button_height = 2
        button_padx = 20
        button_pady = 15
        
        # Crear botones
        docentes_button = self.create_button(
            buttons_frame, 
            "Docentes", 
            "#2196F3",  # Azul
            self.open_docentes,
            button_font,
            button_width,
            button_height
        )
        
        cursos_button = self.create_button(
            buttons_frame, 
            "Ver Cursos", 
            "#FF9800",  # Naranja
            self.open_cursos,
            button_font,
            button_width,
            button_height
        )
        
        materias_button = self.create_button(
            buttons_frame, 
            "Materias", 
            "#9C27B0",  # Púrpura
            self.open_materias,
            button_font,
            button_width,
            button_height
        )
        
        salones_button = self.create_button(
            buttons_frame, 
            "Salones", 
            "#F44336",  # Rojo
            self.open_salones,
            button_font,
            button_width,
            button_height
        )
        
        # Nuevo botón para Horarios
        horarios_button = self.create_button(
            buttons_frame, 
            "Generar Cursos", 
            "#009688",  # Verde azulado
            self.open_horarios,
            button_font,
            button_width,
            button_height
        )
        
        # Organizar botones en grid (3 columnas, 2 filas)
        docentes_button.grid(row=0, column=0, padx=button_padx, pady=button_pady)
        cursos_button.grid(row=0, column=1, padx=button_padx, pady=button_pady)
        materias_button.grid(row=0, column=2, padx=button_padx, pady=button_pady)
        salones_button.grid(row=1, column=0, padx=button_padx, pady=button_pady)
        horarios_button.grid(row=1, column=1, padx=button_padx, pady=button_pady)
        
        # Configurar el grid para centrar los botones
        buttons_frame.grid_columnconfigure(0, weight=1)
        buttons_frame.grid_columnconfigure(1, weight=1)
        buttons_frame.grid_columnconfigure(2, weight=1)
        
        # Pie de página
        footer_label = tk.Label(
            main_frame,
            text="© 2023 Sistema de Gestión Académica - EAM",
            font=("Arial", 10),
            bg="#f0f0f0",
            fg="#888888"
        )
        footer_label.pack(side=tk.BOTTOM, pady=(30, 0))
    
    def create_button(self, parent, text, color, command, font, width, height):
        """Crea un botón con estilo personalizado"""
        button = tk.Button(
            parent,
            text=text,
            font=font,
            bg=color,
            fg="white",
            command=command,
            width=width,
            height=height,
            relief=tk.RAISED,
            bd=1,
            activebackground=self.adjust_color_brightness(color, 1.1),
            activeforeground="white"
        )
        return button
    
    def adjust_color_brightness(self, hex_color, factor):
        """Ajusta el brillo de un color hexadecimal"""
        # Convertir hex a RGB
        r = int(hex_color[1:3], 16)
        g = int(hex_color[3:5], 16)
        b = int(hex_color[5:7], 16)
        
        # Ajustar brillo
        r = min(255, int(r * factor))
        g = min(255, int(g * factor))
        b = min(255, int(b * factor))
        
        # Convertir de vuelta a hex
        return f"#{r:02x}{g:02x}{b:02x}"
    
    def open_horarios(self):
        """Abre la ventana de gestión de horarios"""
        try:
            # Importar la clase HorariosScreen
            from frontend.screens.horarios.horarios_screen import HorariosScreen
            
            # Ocultar la ventana principal (no destruirla)
            self.root.withdraw()
            
            # Crear una nueva ventana Toplevel
            horarios_window = tk.Toplevel()
            horarios_window.title("Gestión de Horarios")
            
            # Función para mostrar la pantalla de inicio cuando se cierra la ventana de horarios
            def mostrar_home():
                # Código para mostrar la pantalla de inicio
                horarios_window.destroy()
                self.root.deiconify()  # Mostrar nuevamente la ventana principal
            
            # Configurar función para cuando se cierre la ventana de horarios
            def on_horarios_close():
                horarios_window.destroy()
                self.root.deiconify()  # Mostrar nuevamente la ventana principal
                
            horarios_window.protocol("WM_DELETE_WINDOW", on_horarios_close)
            
            # Inicializar la pantalla de horarios con la ventana Toplevel y el callback
            horarios_screen = HorariosScreen(horarios_window, show_home_callback=mostrar_home)
        except Exception as e:
            messagebox.showerror("Error", f"Error al abrir la ventana de Horarios: {str(e)}")
            self.root.deiconify()  # Asegurar que la ventana principal se muestre en caso de error
    
    def open_docentes(self):
        """Abre la ventana de gestión de docentes"""
        try:
            # Importar la clase DocentesScreen
            from frontend.screens.docentes.docentes_screen import DocentesScreen
            
            # Ocultar la ventana principal (no destruirla)
            self.root.withdraw()
            
            # Crear una nueva ventana Toplevel
            docentes_window = tk.Toplevel()
            docentes_window.title("Gestión de Docentes")
            
            # Función para mostrar la pantalla de inicio cuando se cierra la ventana de docentes
            def mostrar_home():
                # Código para mostrar la pantalla de inicio
                docentes_window.destroy()
                self.root.deiconify()  # Mostrar nuevamente la ventana principal
            
            # Configurar función para cuando se cierre la ventana de docentes
            def on_docentes_close():
                docentes_window.destroy()
                self.root.deiconify()  # Mostrar nuevamente la ventana principal
                
            docentes_window.protocol("WM_DELETE_WINDOW", on_docentes_close)
            
            # Inicializar la pantalla de docentes con la ventana Toplevel y el callback
            docentes_screen = DocentesScreen(docentes_window, show_home_callback=mostrar_home)
        except Exception as e:
            messagebox.showerror("Error", f"Error al abrir la ventana de Docentes: {str(e)}")
            self.root.deiconify()  # Asegurar que la ventana principal se muestre en caso de error

    def open_cursos(self):
        """Abre la ventana de gestión de cursos"""
        try:
            # Verificar primero si hay cursos
            import requests
            
            # URL base para las peticiones al backend
            BASE_URL = "http://localhost:8000/"
            
            try:
                # Realizar petición al backend para obtener cursos
                response = requests.get(f"{BASE_URL}cursos/detallados")
                
                # Verificar si hay cursos
                if response.status_code == 200:
                    cursos = response.json()
                    if not cursos or len(cursos) == 0:
                        # No hay cursos, mostrar mensaje y abrir ventana de horarios
                        messagebox.showinfo("Información", "No hay cursos disponibles. Se abrirá la ventana de horarios.")
                        self.open_horarios()
                        return
                else:
                    # Error al obtener cursos, mostrar mensaje y continuar normalmente
                    messagebox.showwarning("Advertencia", "No se pudieron verificar los cursos. Se abrirá la ventana de cursos normalmente.")
            except Exception as e:
                # Error de conexión, mostrar mensaje y continuar normalmente
                messagebox.showwarning("Error de Conexión", f"No se pudo conectar al servidor: {str(e)}. Se abrirá la ventana de cursos normalmente.")
            
            # Si hay cursos o hubo un error, continuar con la apertura normal de la ventana de cursos
            # Importar la clase CursosScreen
            from frontend.screens.cursos.cursos_screen import CursosScreen
            
            # Ocultar la ventana principal (no destruirla)
            self.root.withdraw()
            
            # Crear una nueva ventana Toplevel
            cursos_window = tk.Toplevel()
            cursos_window.title("Gestión de Cursos")
            
            # Función para mostrar la pantalla de inicio cuando se cierra la ventana de cursos
            def mostrar_home():
                # Código para mostrar la pantalla de inicio
                cursos_window.destroy()
                self.root.deiconify()  # Mostrar nuevamente la ventana principal
            
            # Configurar función para cuando se cierre la ventana de cursos
            def on_cursos_close():
                cursos_window.destroy()
                self.root.deiconify()  # Mostrar nuevamente la ventana principal
                
            cursos_window.protocol("WM_DELETE_WINDOW", on_cursos_close)
            
            # Inicializar la pantalla de cursos con la ventana Toplevel y el callback
            cursos_screen = CursosScreen(cursos_window, show_home_callback=mostrar_home)
        except Exception as e:
            messagebox.showerror("Error", f"Error al abrir la ventana de Cursos: {str(e)}")
            self.root.deiconify()  # Asegurar que la ventana principal se muestre en caso de error

    def open_materias(self):
        """Abre la ventana de gestión de materias"""
        try:
            # Importar la clase MateriasScreen
            from frontend.screens.materias.materias_screen import MateriasScreen
            
            # Ocultar la ventana principal (no destruirla)
            self.root.withdraw()
            
            # Crear una nueva ventana Toplevel
            materias_window = tk.Toplevel()
            materias_window.title("Gestión de Materias")
            
            # Función para mostrar la pantalla de inicio cuando se cierra la ventana de materias
            def mostrar_home():
                # Código para mostrar la pantalla de inicio
                materias_window.destroy()
                self.root.deiconify()  # Mostrar nuevamente la ventana principal
            
            # Configurar función para cuando se cierre la ventana de materias
            def on_materias_close():
                materias_window.destroy()
                self.root.deiconify()  # Mostrar nuevamente la ventana principal
                
            materias_window.protocol("WM_DELETE_WINDOW", on_materias_close)
            
            # Inicializar la pantalla de materias con la ventana Toplevel y el callback
            materias_screen = MateriasScreen(materias_window, show_home_callback=mostrar_home)      
        except Exception as e:
            messagebox.showerror("Error", f"Error al abrir la ventana de Materias: {str(e)}")
            self.root.deiconify()

    def open_salones(self):
        """Abre la ventana de gestión de salones"""
        try:
            # Importar la clase SalonesScreen
            from frontend.screens.salones.salones_screen import SalonesScreen
            
            # Ocultar la ventana principal (no destruirla)
            self.root.withdraw()
            
            # Crear una nueva ventana Toplevel
            salones_window = tk.Toplevel()
            salones_window.title("Gestión de Salones")
            
            # Función para mostrar la pantalla de inicio cuando se cierra la ventana de salones
            def mostrar_home():
                # Código para mostrar la pantalla de inicio
                salones_window.destroy()
                self.root.deiconify()  # Mostrar nuevamente la ventana principal
            
            # Configurar función para cuando se cierre la ventana de salones
            def on_salones_close():
                salones_window.destroy()
                self.root.deiconify()  # Mostrar nuevamente la ventana principal
                
            salones_window.protocol("WM_DELETE_WINDOW", on_salones_close)
            
            # Inicializar la pantalla de salones con la ventana Toplevel y el callback
            salones_screen = SalonesScreen(salones_window, show_home_callback=mostrar_home)
        except Exception as e:
            messagebox.showerror("Error", f"Error al abrir la ventana de Salones: {str(e)}")
            self.root.deiconify()

    def run(self):
        """Inicia el bucle principal de la aplicación"""
        if self.is_main_window:
            self.root.mainloop()

if __name__ == "__main__":
    app = HomeScreen()
    app.run()