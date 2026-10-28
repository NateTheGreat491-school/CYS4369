# File:     Better GUI
# Dev:      Nathan W. Barros
# Origin:   2026-10-26 11:55:22
# Edited:   2026-10-26 11:55:25

import random
import math
import tkinter as tk

import encrypt

class GUI:
    
    def __init__(self):
        self._root   = tk.Tk()
        self._cipher = tk.StringVar(value="Reverse")
        self._mode   = tk.StringVar(value="Encrypt")

        self._cipherkey  = None # Entry
        self._ciphertext = None # Entry
        self._plaintext  = None # Text

        self._format_window()
        self._draw_ciphers()
        self._draw_modes()
        self._draw_fields()

    def run(self) -> None:
        self._root.mainloop()

    def _execute(self) -> None:
        self._ciphertext.delete("1.0", tk.END)

        match self._cipher.get():
            case "reverse":
                result = encrypt.reverse(self._plaintext.get(), self._cipherkey.get())
            case _:
                result = "Encryption Failed"

        self._ciphertext.insert(
            tk.END,
            f"Mode:    {self._mode.get()}\n"
            f"Option:  {self._cipher.get()}\n"
            f"Message: {result}"
        )
    
    def _format_window(self) -> None:
        NORMx, NORMy = (400,800)
        self._root.title("Better GUI")
        self._root.geometry(f"{NORMx}x{NORMy}")
        self._root.minsize(NORMx//2, NORMy//2)
        self._root.maxsize(NORMx*2, NORMy*2)
        self._root.configure(bg="darkgray")

    def _draw_ciphers(self) -> None:
        tk.Label(self._root, text="Cipher:").pack(anchor="w", padx=10, pady=(10,0))

        options = [
            "Affine", "Caesar", "Matrix", "One-Time Pad",
            "Reverse", "Substitution", "Transposition", "Wild"
        ]

        for op in options:
            tk.Radiobutton(
                self._root, text=op, 
                variable=self._cipher, 
                value=op
            ).pack(anchor="w", padx=20)

    def _draw_modes(self) -> None:
        tk.Label(self._root, text="Mode:").pack(anchor="w", padx=10, pady=(10,0))

        for mode in ["Encrypt", "Decrypt"]:
            tk.Radiobutton(
                self._root, text=mode,
                variable=self._mode,
                value=mode
            ).pack(anchor="w", padx=20)
    
    def _draw_fields(self) -> None:        
        tk.Label(self._root, text="Input:").pack(anchor="w", padx=10, pady=(10,0))
        self._plaintext = tk.Entry(self._root, width=40).pack(padx=10, pady=5)

        tk.Label(self._root, text="Key:").pack(anchor="w", padx=10, pady=(10,0))
        self._cipherkey = tk.Entry(self._root, width=40).pack(padx=10, pady=5)

        tk.Button(self._root, text="Submit", command=self._execute).pack(pady=10)

        tk.Label(self._root, text="Output:").pack(anchor="w", padx=10)
        self._ciphertext = tk.Text(self._root, width=50, height=5).pack(padx=10, pady=5)

def main() -> None:
    gui = GUI()
    gui.run()

if __name__ == "__main__":
    main()

# EOF
