import tkinter as tk

keys = [
    ['`', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '=', 'Backspace'],
    ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '[', ']', '\\'],
    ['Caps Lock', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ';', "'", 'Enter'],
    ['Shift', 'z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '/'],
    ['Space']
]

class VirtualKeyboard(tk.Tk):
    """
    Class utama untuk aplikasi Virtual Keyboard.
    Mewarisi dari tk.Tk untuk menjadi window utama.
    """
    def __init__(self):
        super().__init__()
        self.title("Python Virtual Keyboard")
        self.configure(bg='#333333')
        self.caps_lock_on = False        
        self.entry = tk.Entry(self, width=100, font=('Arial', 14), bd=2, relief='solid')
        self.entry.grid(row=0, column=0, columnspan=15, padx=10, pady=10, ipady=5)
        self.entry.focus_set()

        keys_frame = tk.Frame(self, bg='#333333')
        keys_frame.grid(row=1, column=0, padx=10, pady=5)

        for i, row in enumerate(keys):
            for j, key in enumerate(row):
                if key == 'Space':
                    width = 40
                elif key in ['Backspace', 'Caps Lock', 'Shift', 'Enter']:
                    width = 10
                else:
                    width = 4
                
                button = tk.Button(
                    keys_frame, 
                    text=key, 
                    width=width, 
                    height=2,
                    font=('Arial', 10, 'bold'),
                    bg='#4f4f4f', 
                    fg='white',    
                    activebackground='#6a6a6a', 
                    relief='raised',
                    bd=3,
                    command=lambda k=key: self.button_click(k)
                )
                
                if key == 'Space':
                    button.grid(row=i, column=j, columnspan=8, padx=2, pady=3)
                else:
                    button.grid(row=i, column=j, padx=2, pady=3)

    def button_click(self, key):
        """
        Fungsi yang dieksekusi setiap kali tombol keyboard virtual ditekan.
        """
        current_text = self.entry.get()

        if key == 'Caps Lock':
            self.caps_lock_on = not self.caps_lock_on

        elif key == 'Backspace':
            self.entry.delete(len(current_text) - 1, 'end')

        elif key == 'Space':
            self.entry.insert('end', ' ')
        
        elif key in ['Shift', 'Enter']:
            pass

        else:
            char = key
            if self.caps_lock_on:
                char = key.upper()
            else:
                char = key.lower()
            
            self.entry.insert('end', char)

# --- FUNGSI UTAMA UNTUK MENJALANKAN APLIKASI ---
if __name__ == "__main__":
    app = VirtualKeyboard()
    app.mainloop()