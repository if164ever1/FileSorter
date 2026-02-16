
import customtkinter as ctk
import threading
from tkinter import PhotoImage
from src.filesorter.core.ai_client import GeminiClient

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("FileSorter")
        self.geometry("1100x700")

        # Set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Create navigation frame
        self.navigation_frame = ctk.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)

        self.navigation_frame_label = ctk.CTkLabel(self.navigation_frame, text="FileSorter",
                                                   font=ctk.CTkFont(size=20, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.dashboard_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10,
                                              text="Dashboard",
                                              fg_color="transparent", text_color=("gray10", "gray90"),
                                              hover_color=("gray70", "gray30"),
                                              anchor="w")
        self.dashboard_button.grid(row=1, column=0, sticky="ew")

        self.gemini_chat_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40,
                                                border_spacing=10, text="Gemini AI Chat",
                                                fg_color="transparent", text_color=("gray10", "gray90"),
                                                hover_color=("gray70", "gray30"),
                                                anchor="w")
        self.gemini_chat_button.grid(row=2, column=0, sticky="ew")

        self.settings_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40,
                                             border_spacing=10, text="Settings",
                                             fg_color="transparent", text_color=("gray10", "gray90"),
                                             hover_color=("gray70", "gray30"),
                                             anchor="w")
        self.settings_button.grid(row=3, column=0, sticky="ew")

        # Add a frame for the status indicators
        self.status_frame = ctk.CTkFrame(self.navigation_frame, corner_radius=0, fg_color="transparent")
        self.status_frame.grid(row=5, column=0, padx=20, pady=10, sticky="s")

        # File Monitor Status Indicator
        self.monitor_status_label = ctk.CTkLabel(self.status_frame, text="Monitor:", font=ctk.CTkFont(size=12))
        self.monitor_status_label.grid(row=0, column=0, sticky="w")
        self.monitor_status_indicator = ctk.CTkLabel(self.status_frame, text="Idle", text_color="gray", font=ctk.CTkFont(size=12))
        self.monitor_status_indicator.grid(row=0, column=1, sticky="w", padx=(5, 0))

        # Gemini AI Connection Status Indicator
        self.gemini_status_label = ctk.CTkLabel(self.status_frame, text="Gemini:", font=ctk.CTkFont(size=12))
        self.gemini_status_label.grid(row=1, column=0, sticky="w")
        self.gemini_status_led = ctk.CTkLabel(self.status_frame, text="", width=12, height=12, corner_radius=6, fg_color="gray")
        self.gemini_status_led.grid(row=1, column=1, sticky="w", padx=(5, 0))
        self.gemini_status_text = ctk.CTkLabel(self.status_frame, text="Initializing...", font=ctk.CTkFont(size=12), text_color="gray")
        self.gemini_status_text.grid(row=1, column=2, sticky="w", padx=(5, 0))

        # Start Gemini connection check
        self.check_gemini_connection()

    def check_gemini_connection(self):
        """Checks the Gemini API connection in a separate thread."""
        thread = threading.Thread(target=self._check_gemini_connection_thread)
        thread.daemon = True
        thread.start()

    def _check_gemini_connection_thread(self):
        """The actual connection check logic."""
        client = GeminiClient()
        if client.check_connection():
            self.after(0, self.update_gemini_status, True)
        else:
            self.after(0, self.update_gemini_status, False)

    def update_gemini_status(self, is_connected):
        """Updates the Gemini status indicator on the UI."""
        if is_connected:
            self.gemini_status_led.configure(fg_color="green")
            self.gemini_status_text.configure(text="Connected", text_color="green")
        else:
            self.gemini_status_led.configure(fg_color="red")
            self.gemini_status_text.configure(text="Failed", text_color="red")

if __name__ == "__main__":
    app = App()
    app.mainloop()
