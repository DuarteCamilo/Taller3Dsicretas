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
        if root is None:
            self.root = tk.Tk()
            self.is_main_window = True
        else:
            self.root = root
            self.is_main_window = False
            
        self.show_home_callback = show_home_callback
        self.hay_cursos = False
        
        # Tema de colores coincidente con home_screen
        self.theme = {
            "primary": "#2563eb",
            "secondary": "#374151",
            "background": "#f8fafc",
            "accent": "#7c3aed",
            "success": "#10b981",
            "warning": "#f59e0b",
            "danger": "#ef4444",
            "text_dark": "#1e293b",
            "text_light": "#f1f5f9",
            "text_muted": "#64748b"
        }
        
        self.root.title("Gestión de Horarios")
        self.root.geometry("1000x500")
        self.root.minsize(900, 350)
        self.root.configure(bg=self.theme["background"])
        

        self.setup_ui()
        self.setup_button_effects()
        self.verificar_cursos()
        self.center_window()

        
    def setup_ui(self):
        # Contenedor principal
        main_container = tk.Frame(self.root, bg=self.theme["background"], padx=40, pady=30)
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Encabezado
        header_frame = tk.Frame(main_container, bg=self.theme["background"])
        header_frame.pack(fill=tk.X, pady=(0, 30))
        
        # Logo
        logo_frame = tk.Frame(header_frame, width=80, height=80, bg=self.theme["primary"])
        logo_frame.pack(side=tk.LEFT, padx=(0, 20))
        logo_frame.pack_propagate(False)
        
        logo_text = tk.Label(logo_frame, text="EAM", font=("Arial", 24, "bold"), 
                           fg="white", bg=self.theme["primary"])
        logo_text.place(relx=0.5, rely=0.5, anchor="center")
        
        # Títulos
        title_frame = tk.Frame(header_frame, bg=self.theme["background"])
        title_frame.pack(side=tk.LEFT)
        
        title_font = font.Font(family="Helvetica", size=28, weight="bold")
        title_label = tk.Label(
            title_frame, 
            text="Gestión de Horarios Automáticos", 
            font=title_font,
            bg=self.theme["background"],
            fg=self.theme["text_dark"]
        )
        title_label.pack(anchor=tk.W)
        
        subtitle_font = font.Font(family="Helvetica", size=14)
        subtitle_label = tk.Label(
            title_frame,
            text="Generación inteligente de horarios académicos",
            font=subtitle_font,
            bg=self.theme["background"],
            fg=self.theme["text_muted"]
        )
        subtitle_label.pack(anchor=tk.W)
        
        # Separador
        separator = tk.Frame(main_container, height=2, bg="#e2e8f0")
        separator.pack(fill=tk.X, pady=(0, 30))
        
        # Panel de contenido
        content_frame = tk.Frame(main_container, bg=self.theme["background"])
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Descripción
        desc_font = font.Font(family="Helvetica", size=14)
        desc_text = (
            "Esta herramienta permite generar horarios automáticamente basados en los docentes, "
            "materias y salones disponibles. También puede eliminar todos los horarios generados."
        )
        desc_label = tk.Label(
            content_frame,
            text=desc_text,
            font=desc_font,
            bg=self.theme["background"],
            fg=self.theme["text_muted"],
            wraplength=800,
            justify="center"
        )
        desc_label.pack(pady=(0, 20))
        
        # Panel de botones
        buttons_panel = tk.Frame(content_frame, bg=self.theme["background"])
        buttons_panel.pack(fill=tk.BOTH, expand=True)
        
        # Configuración de botones
        self.button_configs = {
            "Generar Horarios": {
                "icon": "⏱️",
                "color": self.theme["success"],
                "command": self.generar_horarios,
                "description": "Crea nuevos horarios automáticamente"
            },
            "Limpiar Horarios": {
                "icon": "🗑️",
                "color": self.theme["danger"],
                "command": self.limpiar_horarios,
                "description": "Elimina todos los horarios existentes"
            }
        }
        
        # Crear botones
        self.nav_buttons = {}
        col = 0
        for btn_text, config in self.button_configs.items():
            btn_container = tk.Frame(buttons_panel, bg=self.theme["background"], padx=15, pady=15)
            btn_container.grid(row=0, column=col, sticky="nsew", padx=20, pady=10)
            btn_container.columnconfigure(0, weight=1)
            btn_container.rowconfigure(0, weight=1)
            
            btn_frame = tk.Frame(
                btn_container,
                bg=self.theme["background"],
                highlightbackground="#e2e8f0",
                highlightthickness=1,
                bd=0
            )
            btn_frame.grid(row=0, column=0, sticky="nsew")
            
            btn = tk.Button(
                btn_frame,
                text=f"{config['icon']}  {btn_text}",
                font=("Helvetica", 14, "bold"),
                bg="white",
                fg=config['color'],
                activebackground=self.lighten_color(config['color'], 0.9),
                activeforeground="white",
                bd=0,
                relief=tk.FLAT,
                cursor="hand2",
                command=config['command'],
                compound=tk.LEFT,
                padx=15,
                pady=12,
                wraplength=300
            )
            btn.pack(fill=tk.BOTH, expand=True)
            
            desc_label = tk.Label(
                btn_container,
                text=config['description'],
                font=("Helvetica", 11),
                bg=self.theme["background"],
                fg=self.theme["text_muted"],
                wraplength=200
            )
            desc_label.grid(row=1, column=0, pady=(5, 0))
            
            self.nav_buttons[btn_text] = btn
            col += 1
        
        # Barra de estado
        status_frame = tk.Frame(main_container, bg=self.theme["background"], pady=10)
        status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        self.status_label = tk.Label(
            status_frame,
            text="Estado: Verificando horarios...",
            font=("Helvetica", 10),
            bg=self.theme["background"],
            fg=self.theme["success"]
        )
        self.status_label.pack(side=tk.LEFT)
        
        # Botón de regreso
        back_btn = tk.Button(
            status_frame,
            text="← Regresar",
            command=self.volver_al_home,
            font=("Helvetica", 10, "bold"),
            fg=self.theme["primary"],
            bg=self.theme["background"],
            activeforeground=self.theme["accent"],
            bd=0,
            cursor="hand2"
        )
        back_btn.pack(side=tk.RIGHT)
        
        # Ajustar grid
        buttons_panel.columnconfigure(0, weight=1)
        buttons_panel.columnconfigure(1, weight=1)
        
    def setup_button_effects(self):
        for btn_text, btn in self.nav_buttons.items():
            color = self.button_configs[btn_text]["color"]
            btn.bind("<Enter>", lambda e, b=btn, c=color: self.on_button_hover(b, c))
            btn.bind("<Leave>", lambda e, b=btn, c=color: self.on_button_leave(b, c))
            btn.bind("<Button-1>", lambda e, b=btn, c=color: self.on_button_click(b, c))
            btn.bind("<ButtonRelease-1>", lambda e, b=btn, c=color: self.on_button_release(b, c))
    
    # Métodos de efectos visuales (iguales que home_screen)
    def on_button_hover(self, button, color):
        button.config(bg=color, fg="white")
        
    def on_button_leave(self, button, color):
        button.config(bg="white", fg=color)
    
    def on_button_click(self, button, color):
        darker_color = self.darken_color(color, 0.8)
        button.config(bg=darker_color, fg="white")
    
    def on_button_release(self, button, color):
        button.config(bg=color, fg="white")
    
    def lighten_color(self, hex_color, factor=1.3):
        hex_color = hex_color.lstrip('#')
        r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        r = min(255, int(r * factor))
        g = min(255, int(g * factor))
        b = min(255, int(b * factor))
        return f"#{r:02x}{g:02x}{b:02x}"
    
    def darken_color(self, hex_color, factor=0.7):
        hex_color = hex_color.lstrip('#')
        r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        r = max(0, int(r * factor))
        g = max(0, int(g * factor))
        b = max(0, int(b * factor))
        return f"#{r:02x}{g:02x}{b:02x}"
    
    # Métodos existentes de funcionalidad (sin cambios)
    def verificar_cursos(self):
        try:
            response = requests.get(f"{BASE_URL}cursos/detallados")
            if response.status_code == 200:
                cursos = response.json()
                if cursos and len(cursos) > 0:
                    self.hay_cursos = True
                    self.status_label.config(text="Estado: Horarios generados ✓", fg=self.theme["success"])
                    self.nav_buttons["Generar Horarios"].config(state=tk.DISABLED)
                    self.nav_buttons["Limpiar Horarios"].config(state=tk.NORMAL)
                else:
                    self.hay_cursos = False
                    self.status_label.config(text="Estado: Sin horarios generados", fg=self.theme["text_muted"])
                    self.nav_buttons["Generar Horarios"].config(state=tk.NORMAL)
                    self.nav_buttons["Limpiar Horarios"].config(state=tk.DISABLED)
            else:
                self.status_label.config(text="Error al verificar horarios", fg=self.theme["danger"])
        except Exception as e:
            self.status_label.config(text=f"Error de conexión: {str(e)}", fg=self.theme["danger"])
    
    def generar_horarios(self):
        if self.hay_cursos:
            messagebox.showinfo("Información", "Ya existen horarios generados")
            return
        
        if messagebox.askyesno("Confirmar", "¿Generar nuevos horarios?"):
            try:
                response = requests.post(f"{BASE_URL}main/generar-horarios")
                if response.status_code == 200:
                    self.hay_cursos = True
                    self.status_label.config(text="Horarios generados ✓", fg=self.theme["success"])
                    self.nav_buttons["Generar Horarios"].config(state=tk.DISABLED)
                    self.nav_buttons["Limpiar Horarios"].config(state=tk.NORMAL)
                    messagebox.showinfo("Éxito", "Horarios generados correctamente")
                else:
                    messagebox.showerror("Error", f"Error del servidor: {response.status_code}")
            except Exception as e:
                messagebox.showerror("Error", f"Error de conexión: {str(e)}")
    
    def limpiar_horarios(self):
        if messagebox.askyesno("Confirmar", "¿Eliminar todos los horarios?"):
            try:
                response = requests.delete(f"{BASE_URL}main/limpiar-horarios")
                if response.status_code == 200:
                    self.hay_cursos = False
                    self.status_label.config(text="Horarios eliminados ✓", fg=self.theme["success"])
                    self.nav_buttons["Generar Horarios"].config(state=tk.NORMAL)
                    self.nav_buttons["Limpiar Horarios"].config(state=tk.DISABLED)
                    messagebox.showinfo("Éxito", "Horarios eliminados correctamente")
                else:
                    messagebox.showerror("Error", f"Error del servidor: {response.status_code}")
            except Exception as e:
                messagebox.showerror("Error", f"Error de conexión: {str(e)}")
    
    def center_window(self):
        # Actualizar tareas pendientes para asegurar dimensiones correctas
        self.root.update_idletasks()
        
        # Obtener dimensiones de la ventana y la pantalla
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Calcular posición x e y para centrar
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        
        # Aplicar nueva geometría
        self.root.geometry(f'+{x}+{y}')
        
    def volver_al_home(self):
        if self.show_home_callback:
            self.show_home_callback()
        else:
            self.root.destroy()
    
    def run(self):
        if self.is_main_window:
            self.root.mainloop()

if __name__ == "__main__":
    app = HorariosScreen()
    app.run()