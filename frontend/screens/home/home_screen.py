import tkinter as tk
from tkinter import messagebox, font
import os
import sys
from functools import partial

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
        self.root.geometry("1000x700")
        self.root.minsize(900, 650)
        
        # Colores del tema
        self.theme = {
            "primary": "#2563eb",         # Azul primario
            "secondary": "#374151",       # Gris oscuro
            "background": "#f8fafc",      # Fondo claro
            "accent": "#7c3aed",          # Púrpura acento
            "success": "#10b981",         # Verde éxito
            "warning": "#f59e0b",         # Naranja advertencia
            "danger": "#ef4444",          # Rojo peligro
            "text_dark": "#1e293b",       # Texto oscuro
            "text_light": "#f1f5f9",      # Texto claro
            "text_muted": "#64748b"       # Texto secundario
        }
        
        # Configurar el fondo
        self.root.configure(bg=self.theme["background"])
        
        # Cargar recursos
        self.load_resources()
        
        # Configurar el estilo de la ventana
        self.setup_ui()
        
        # Añadir efectos a los botones usando bind
        self.setup_button_effects()
        
    def load_resources(self):
        """Cargar imágenes e iconos necesarios"""
        self.icons = {}
        self.button_images = {}
        
        resources_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'resources'))
        if not os.path.exists(resources_dir):
            os.makedirs(resources_dir)
        
        logo_frame = tk.Frame(self.root, width=80, height=80, bg=self.theme["primary"])
        logo_label = tk.Label(logo_frame, text="EAM", font=("Arial", 24, "bold"), 
                             fg="white", bg=self.theme["primary"])
        logo_label.place(relx=0.5, rely=0.5, anchor="center")
        self.logo_widget = logo_frame
        
        self.button_configs = {
            "Docentes": {
                "icon": "👨‍🏫",
                "color": self.theme["primary"],
                "description": "Gestionar información de profesores"
            },
            "Ver Cursos": {
                "icon": "📚",
                "color": self.theme["warning"],
                "description": "Visualizar cursos disponibles"
            },
            "Materias": {
                "icon": "📝",
                "color": self.theme["accent"],
                "description": "Administrar materias académicas"
            },
            "Salones": {
                "icon": "🏫",
                "color": self.theme["danger"],
                "description": "Gestionar aulas y espacios"
            },
            "Generar Cursos": {
                "icon": "⏱️",
                "color": self.theme["success"],
                "description": "Crear y programar nuevos cursos"
            }
        }
        
    def setup_ui(self):
        """Configurar la interfaz de usuario"""
        # Contenedor principal con padding
        main_container = tk.Frame(self.root, bg=self.theme["background"], padx=40, pady=30)
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Panel superior con logo y título
        header_frame = tk.Frame(main_container, bg=self.theme["background"])
        header_frame.pack(fill=tk.X, pady=(0, 30))
        
        # Logo a la izquierda (usando Frame con texto en lugar de imagen)
        logo_frame = tk.Frame(header_frame, width=80, height=80, bg=self.theme["primary"])
        logo_frame.pack(side=tk.LEFT, padx=(0, 20))
        logo_frame.pack_propagate(False)  # Evitar que el frame se redimensione
        
        logo_text = tk.Label(logo_frame, text="EAM", font=("Arial", 24, "bold"), 
                           fg="white", bg=self.theme["primary"])
        logo_text.place(relx=0.5, rely=0.5, anchor="center")
        
        # Título y subtítulo a la derecha del logo
        title_frame = tk.Frame(header_frame, bg=self.theme["background"])
        title_frame.pack(side=tk.LEFT)
        
        # Título principal
        title_font = font.Font(family="Helvetica", size=28, weight="bold")
        title_label = tk.Label(
            title_frame, 
            text="Sistema de Gestión Académica", 
            font=title_font,
            bg=self.theme["background"],
            fg=self.theme["text_dark"]
        )
        title_label.pack(anchor=tk.W)
        
        # Subtítulo
        subtitle_font = font.Font(family="Helvetica", size=14)
        subtitle_label = tk.Label(
            title_frame,
            text="Plataforma integral para la administración educativa",
            font=subtitle_font,
            bg=self.theme["background"],
            fg=self.theme["text_muted"]
        )
        subtitle_label.pack(anchor=tk.W)
        
        # Separador
        separator = tk.Frame(main_container, height=2, bg="#e2e8f0")
        separator.pack(fill=tk.X, pady=(0, 30))
        
        # Frame para los botones de navegación
        nav_title_font = font.Font(family="Helvetica", size=16, weight="bold")
        nav_title = tk.Label(
            main_container,
            text="Panel de Control",
            font=nav_title_font,
            bg=self.theme["background"],
            fg=self.theme["text_dark"]
        )
        nav_title.pack(anchor=tk.W, pady=(0, 20))
        
        # Panel de botones con grid responsivo
        buttons_panel = tk.Frame(main_container, bg=self.theme["background"])
        buttons_panel.pack(fill=tk.BOTH, expand=True)
        
        # Hacer que el panel de botones sea responsive
        for i in range(3):
            buttons_panel.columnconfigure(i, weight=1)
        for i in range(2):
            buttons_panel.rowconfigure(i, weight=1)
        
        # Crear botones modernos
        buttons = {
            "Docentes": (0, 0, self.open_docentes),
            "Ver Cursos": (0, 1, self.open_cursos),
            "Materias": (0, 2, self.open_materias),
            "Salones": (1, 0, self.open_salones),
            "Generar Cursos": (1, 1, self.open_horarios)
        }
        
        self.nav_buttons = {}
        
        for btn_text, (row, col, command) in buttons.items():
            # Frame del botón (para contener el botón y su descripción)
            btn_container = tk.Frame(buttons_panel, bg=self.theme["background"], padx=15, pady=15)
            btn_container.grid(row=row, column=col, sticky="nsew", padx=10, pady=10)
            
            # Hacer que el contenedor se expanda
            btn_container.columnconfigure(0, weight=1)
            btn_container.rowconfigure(0, weight=1)
            
            # Configuración específica del botón
            btn_config = self.button_configs[btn_text]
            
            # Crear el marco del botón con efecto de elevación
            btn_frame = tk.Frame(
                btn_container,
                bg=self.theme["background"],
                highlightbackground="#e2e8f0",
                highlightthickness=1,
                bd=0
            )
            btn_frame.grid(row=0, column=0, sticky="nsew")
            
            # El botón real dentro del marco
            btn = tk.Button(
                btn_frame,
                text=f"{btn_config['icon']}  {btn_text}",
                font=("Helvetica", 14, "bold"),
                bg="white",
                fg=btn_config['color'],
                activebackground=self.lighten_color(btn_config['color'], 0.9),
                activeforeground="white",
                bd=0,
                relief=tk.FLAT,
                cursor="hand2",
                command=command,
                compound=tk.LEFT,
                padx=20,
                pady=30,
                wraplength=200
            )
            btn.pack(fill=tk.BOTH, expand=True)
            
            # Descripción del botón
            desc_label = tk.Label(
                btn_container,
                text=btn_config['description'],
                font=("Helvetica", 11),
                bg=self.theme["background"],
                fg=self.theme["text_muted"],
                wraplength=200
            )
            desc_label.grid(row=1, column=0, pady=(8, 0))
            
            # Guardar referencia al botón
            self.nav_buttons[btn_text] = btn
        
        # Panel de información en la parte inferior
        status_frame = tk.Frame(main_container, bg=self.theme["background"], pady=20)
        status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        # Información del estado del sistema
        status_label = tk.Label(
            status_frame,
            text="Sistema activo y funcionando correctamente",
            font=("Helvetica", 10),
            bg=self.theme["background"],
            fg=self.theme["success"]
        )
        status_label.pack(side=tk.LEFT)
        
        # Pie de página con copyright
        footer_label = tk.Label(
            status_frame,
            text="© 2025 Sistema de Gestión Académica - EAM",
            font=("Helvetica", 10),
            bg=self.theme["background"],
            fg=self.theme["text_muted"]
        )
        footer_label.pack(side=tk.RIGHT)
        
    def setup_button_effects(self):
        """Configurar efectos de hover para los botones"""
        for btn_text, btn in self.nav_buttons.items():
            color = self.button_configs[btn_text]["color"]
            
            # Efectos al pasar el ratón
            btn.bind("<Enter>", lambda e, b=btn, c=color: self.on_button_hover(b, c))
            btn.bind("<Leave>", lambda e, b=btn, c=color: self.on_button_leave(b, c))
            
            # Efecto al hacer clic
            btn.bind("<Button-1>", lambda e, b=btn, c=color: self.on_button_click(b, c))
            btn.bind("<ButtonRelease-1>", lambda e, b=btn, c=color: self.on_button_release(b, c))
    
    def on_button_hover(self, button, color):
        """Efecto al pasar el ratón sobre el botón"""
        button.config(
            bg=color,
            fg="white",
        )
        
    def on_button_leave(self, button, color):
        """Efecto al salir el ratón del botón"""
        button.config(
            bg="white",
            fg=color,
        )
    
    def on_button_click(self, button, color):
        """Efecto al presionar el botón"""
        darker_color = self.darken_color(color, 0.8)
        button.config(
            bg=darker_color,
            fg="white",
        )
    
    def on_button_release(self, button, color):
        """Efecto al soltar el botón"""
        button.config(
            bg=color,
            fg="white",
        )
    
    def lighten_color(self, hex_color, factor=1.3):
        """Aclara un color hexadecimal"""
        # Convertir hex a RGB
        hex_color = hex_color.lstrip('#')
        r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        
        # Aclarar
        r = min(255, int(r * factor))
        g = min(255, int(g * factor))
        b = min(255, int(b * factor))
        
        # Convertir de vuelta a hex
        return f"#{r:02x}{g:02x}{b:02x}"
    
    def darken_color(self, hex_color, factor=0.7):
        """Oscurece un color hexadecimal"""
        # Convertir hex a RGB
        hex_color = hex_color.lstrip('#')
        r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        
        # Oscurecer
        r = max(0, int(r * factor))
        g = max(0, int(g * factor))
        b = max(0, int(b * factor))
        
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
            horarios_window.geometry("1000x700")
            horarios_window.configure(bg=self.theme["background"])
            
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
            docentes_window.geometry("1000x700")
            docentes_window.configure(bg=self.theme["background"])
            
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
            cursos_window.geometry("1000x700")
            cursos_window.configure(bg=self.theme["background"])
            
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
            materias_window.geometry("1000x700")
            materias_window.configure(bg=self.theme["background"])
            
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
            salones_window.geometry("1000x700")
            salones_window.configure(bg=self.theme["background"])
            
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
        # Centrar la ventana en la pantalla
        self.center_window()
        
        if self.is_main_window:
            self.root.mainloop()
    
    def center_window(self):
        """Centra la ventana en la pantalla"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry('{}x{}+{}+{}'.format(width, height, x, y))

if __name__ == "__main__":
    app = HomeScreen()
    app.run()
    
    