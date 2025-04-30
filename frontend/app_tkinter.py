import tkinter as tk
from tkinter import messagebox
import requests
import threading

class APIClientApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Cliente API Horarios")
        self.root.geometry("500x300")
        self.root.configure(bg="#f0f0f0")
        
        # Configuración de la API
        self.api_url = "http://localhost:8000"
        
        # Crear widgets
        self.setup_ui()
    
    def setup_ui(self):
        # Frame principal
        main_frame = tk.Frame(self.root, bg="#f0f0f0", padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        title_label = tk.Label(
            main_frame, 
            text="Cliente para API de Horarios", 
            font=("Arial", 16, "bold"),
            bg="#f0f0f0"
        )
        title_label.pack(pady=(0, 20))
        
        # Información
        info_label = tk.Label(
            main_frame,
            text="Esta aplicación se conecta a la API de Horarios",
            font=("Arial", 10),
            bg="#f0f0f0",
            wraplength=400
        )
        info_label.pack(pady=(0, 20))
        
        # Estado de conexión
        self.status_var = tk.StringVar()
        self.status_var.set("Estado: No conectado")
        status_label = tk.Label(
            main_frame,
            textvariable=self.status_var,
            font=("Arial", 10),
            bg="#f0f0f0"
        )
        status_label.pack(pady=(0, 20))
        
        # Botón para verificar conexión
        check_button = tk.Button(
            main_frame,
            text="Verificar Conexión",
            command=self.check_connection,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=10,
            pady=5
        )
        check_button.pack()
        
        # Área de resultados
        self.result_text = tk.Text(main_frame, height=5, width=50)
        self.result_text.pack(pady=(20, 0))
        self.result_text.config(state=tk.DISABLED)
    
    def check_connection(self):
        """Verifica la conexión con la API en un hilo separado"""
        self.status_var.set("Estado: Verificando conexión...")
        threading.Thread(target=self._do_check_connection).start()
    
    def _do_check_connection(self):
        """Realiza la verificación de conexión en segundo plano"""
        try:
            # Intenta conectarse a la API
            response = requests.get(f"{self.api_url}/")
            
            # Actualiza la interfaz en el hilo principal
            self.root.after(0, self._update_ui_success, response.json())
        except Exception as e:
            # Maneja errores de conexión
            self.root.after(0, self._update_ui_error, str(e))
    
    def _update_ui_success(self, data):
        """Actualiza la UI cuando la conexión es exitosa"""
        self.status_var.set("Estado: Conectado")
        
        # Actualiza el área de resultados
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, f"Conexión exitosa a la API!\n\nRespuesta: {data}")
        self.result_text.config(state=tk.DISABLED)
        
        # Muestra un mensaje
        messagebox.showinfo("Conexión Exitosa", "Se ha conectado correctamente a la API de Horarios")
    
    def _update_ui_error(self, error_msg):
        """Actualiza la UI cuando hay un error de conexión"""
        self.status_var.set("Estado: Error de conexión")
        
        # Actualiza el área de resultados
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, f"Error al conectar con la API:\n{error_msg}\n\nAsegúrate de que el servidor esté en ejecución en {self.api_url}")
        self.result_text.config(state=tk.DISABLED)
        
        # Muestra un mensaje de error
        messagebox.showerror("Error de Conexión", f"No se pudo conectar a la API. Verifica que el servidor esté en ejecución.")

if __name__ == "__main__":
    root = tk.Tk()
    app = APIClientApp(root)
    root.mainloop()