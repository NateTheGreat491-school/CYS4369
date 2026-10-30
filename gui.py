# File:     Custom GUI
# Dev:      Nathan W. Barros
# Origin:   2026-10-26 11:55:22
# Edited:   2026-10-28 22:15:00

import tkinter as tk
from tkinter import ttk, messagebox

import encrypt
import decrypt
import hack

# --- THEME CONSTANTS (Hacker / Cyberpunk Palette) ---
BG_VOID = "#090a0f"       # Deepest background
BG_PANEL = "#12151e"      # Slightly elevated panel tone (glass effect base)
NEON_GREEN = "#00ff66"    # Primary accent / success highlights
NEON_YELLOW = "#ccff00"   # Secondary accent / keys highlights
TEXT_MAIN = "#f0f6fc"     # Crisp white text
TEXT_MUTED = "#6e7681"    # Terminal dim text
FONT_MONO = ("Consolas", 10)
FONT_MONO_BOLD = ("Consolas", 10, "bold")

class CipherGUI:
    def __init__(self):
        self._root = tk.Tk()
        self._root.title("root@cipher-workbench:~#")
        
        # Sizing & Window Properties (Using native decorations for stability)
        self._root.geometry("540x720")
        self._root.minsize(480, 620)
        self._root.configure(bg=BG_VOID)
        
        # Configure TTK Theme for Dark Mode
        self._style = ttk.Style()
        self._style.theme_use("clam")
        
        # Custom TTK Styling bindings
        self._style.configure(".", background=BG_VOID, foreground=TEXT_MAIN, font=FONT_MONO)
        self._style.configure("TLabel", background=BG_VOID, foreground=TEXT_MAIN, font=FONT_MONO)
        self._style.configure("TLabelFrame", background=BG_VOID, foreground=NEON_YELLOW, font=FONT_MONO_BOLD, bordercolor=TEXT_MUTED)
        self._style.configure("TLabelFrame.Label", background=BG_VOID, foreground=NEON_YELLOW)
        self._style.configure("TRadiobutton", background=BG_VOID, foreground=TEXT_MAIN, font=FONT_MONO)
        self._style.map("TRadiobutton", background=[("active", BG_VOID)], foreground=[("active", NEON_GREEN)])
        
        # Configure combobox colors to match the dark neon theme (Neon Green text)
        self._style.map(
            "TCombobox",
            fieldbackground=[("readonly", BG_PANEL)],
            selectbackground=[("readonly", BG_PANEL)],
            selectforeground=[("readonly", NEON_GREEN)],
            foreground=[("readonly", NEON_GREEN)]
        )

        # Application state variables
        self._cipher_var = tk.StringVar(value="Reverse")
        self._mode_var = tk.StringVar(value="Encrypt")

        # UI Component references
        self._plaintext_entry = None
        self._key_entry = None
        self._output_text = None

        self._build_ui()

    def run(self) -> None:
        self._root.mainloop()

    def _build_ui(self) -> None:
        # Main container with dark padding
        main_frame = tk.Frame(self._root, bg=BG_VOID, padx=15, pady=15)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # 1. Configuration Panel (Mode & Cipher)
        config_frame = ttk.LabelFrame(main_frame, text=" [ CONFIGURATION ] ", padding=12)
        config_frame.pack(fill=tk.X, pady=(0, 12))

        # Mode Selection
        mode_frame = tk.Frame(config_frame, bg=BG_VOID)
        mode_frame.pack(fill=tk.X, pady=(0, 8))
        ttk.Label(mode_frame, text="MODE >", foreground=NEON_YELLOW).pack(side=tk.LEFT, padx=(0, 15))
        
        for mode in ["Encrypt", "Decrypt", "Hack"]:
            rb = ttk.Radiobutton(mode_frame, text=mode, variable=self._mode_var, value=mode)
            rb.pack(side=tk.LEFT, padx=10)

        # Cipher Selection
        cipher_frame = tk.Frame(config_frame, bg=BG_VOID)
        cipher_frame.pack(fill=tk.X, pady=4)
        ttk.Label(cipher_frame, text="CIPHER>", foreground=NEON_YELLOW).pack(side=tk.LEFT, padx=(0, 15))

        options = [
            "Affine", "Caesar", "Matrix", "One-Time Pad",
            "Reverse", "Substitution", "Transposition", "Wild"
        ]
        
        cipher_dropdown = ttk.Combobox(
            cipher_frame, textvariable=self._cipher_var, values=options, state="readonly", font=FONT_MONO
        )
        cipher_dropdown.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # 2. Input Fields Panel
        inputs_frame = ttk.LabelFrame(main_frame, text=" [ DATA STREAMS ] ", padding=12)
        inputs_frame.pack(fill=tk.X, pady=(0, 12))

        ttk.Label(inputs_frame, text="Input Payload:", foreground=TEXT_MUTED).pack(anchor="w")
        
        # Scrollable Input Text Container
        input_container = tk.Frame(inputs_frame, bg=BG_VOID)
        input_container.pack(fill=tk.X, pady=(4, 10))

        self._plaintext_entry = tk.Text(
            input_container, wrap=tk.WORD, height=5, font=FONT_MONO,
            bg=BG_PANEL, fg=NEON_GREEN, insertbackground=NEON_GREEN,
            relief="flat", bd=0, highlightbackground=TEXT_MUTED, highlightcolor=NEON_GREEN, highlightthickness=1
        )
        
        input_scrollbar = ttk.Scrollbar(input_container, orient=tk.VERTICAL, command=self._plaintext_entry.yview)
        self._plaintext_entry.configure(yscrollcommand=input_scrollbar.set)

        input_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self._plaintext_entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        ttk.Label(inputs_frame, text="Encryption Key:", foreground=TEXT_MUTED).pack(anchor="w")
        self._key_entry = tk.Entry(
            inputs_frame, bg=BG_PANEL, fg=NEON_YELLOW, insertbackground=NEON_YELLOW,
            font=FONT_MONO, relief="flat", highlightbackground=TEXT_MUTED, highlightcolor=NEON_YELLOW, highlightthickness=1
        )
        self._key_entry.pack(fill=tk.X, pady=(4, 4), ipady=4)

        # 3. Action Button
        self._submit_btn = tk.Button(
            main_frame, text="> EXECUTE TRANSFORMATION", command=self._execute,
            bg=BG_PANEL, fg=NEON_GREEN, activebackground=NEON_GREEN, activeforeground=BG_VOID,
            font=FONT_MONO_BOLD, relief="flat", bd=0, cursor="hand2", padx=10, pady=8
        )
        self._submit_btn.pack(fill=tk.X, pady=6)
        
        self._submit_btn.bind("<Enter>", lambda e: self._submit_btn.configure(bg=NEON_GREEN, fg=BG_VOID))
        self._submit_btn.bind("<Leave>", lambda e: self._submit_btn.configure(bg=BG_PANEL, fg=NEON_GREEN))

        # 4. Output Display Area
        output_frame = ttk.LabelFrame(main_frame, text=" [ SYSTEM OUTPUT ] ", padding=12)
        output_frame.pack(fill=tk.BOTH, expand=True, pady=(6, 0))

        self._output_text = tk.Text(
            output_frame, wrap=tk.WORD, font=FONT_MONO, bg=BG_PANEL, fg=TEXT_MAIN,
            insertbackground=TEXT_MAIN, relief="flat", bd=0, highlightthickness=0
        )
        
        scrollbar = ttk.Scrollbar(output_frame, orient=tk.VERTICAL, command=self._output_text.yview)
        self._output_text.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self._output_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def _execute(self) -> None:
        mode    = self._mode_var.get()
        cipher  = self._cipher_var.get()
        text_in = self._plaintext_entry.get("1.0", tk.END).strip()
        key_in  = self._key_entry.get().strip()

        if not text_in:
            messagebox.showwarning("Warning", "Payload cannot be empty.")
            return

        match (mode):
            case "Encrypt":
                method: object = encrypt
            case "Decrypt":
                method: object = decrypt
            case "Hack":
                method: object = hack

        match cipher.lower():
            case "reverse":
                result = method.reverse(text_in, key_in)

            case "caesar":
                try:
                    shift = int(key_in)
                except ValueError:
                    messagebox.showwarning("Warning", "Caesar Cipher expects an integer key.")
                result = method.caesar(text_in, shift)

            case "transposition":
                result = method.transposition(text_in, int(key_in))

            case "affine"|"matrix"|"one-time pad"|"substitution"|"wild":
                messagebox.showwarning("Notice", "Ciphers not available.")

            case _:
                result = f"ERR: Algorithm '{cipher}' module not loaded."

        self._output_text.delete("1.0", tk.END)
        self._output_text.insert(tk.END, result)


def main() -> None:
    gui = CipherGUI()
    gui.run()


if __name__ == "__main__":
    main()
