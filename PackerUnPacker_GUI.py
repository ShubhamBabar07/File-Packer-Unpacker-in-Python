import os
import zipfile
import tkinter as tk
from tkinter import filedialog, messagebox
from datetime import datetime

# Clock Label class to handle date, time, and day display
class ClockLabel(tk.Label):
    def __init__(self, parent, type):
        super().__init__(parent)
        self.type = type
        self.configure(fg='green')
        if type == 'date':
            self.sdf = "%B %d %Y"
            self.configure(font=("sans-serif", 12))
            self.pack(anchor='w')
        elif type == 'time':
            self.sdf = "%I:%M:%S %p"
            self.configure(font=("sans-serif", 40))
            self.pack(anchor='center')
        elif type == 'day':
            self.sdf = "%A"
            self.configure(font=("sans-serif", 16))
            self.pack(anchor='e')
        self.update_clock()

    def update_clock(self):
        now = datetime.now().strftime(self.sdf)
        self.configure(text=now)
        self.after(1000, self.update_clock)

# Base template class for the GUI
class Template(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("800x600")
        self.title("Packer-Unpacker")
        
        self._top = tk.Frame(self, bg='lightgray')
        self._top.pack(fill='x')

        self._header = tk.Frame(self, bg='white')
        self._header.pack(fill='x')

        self._content = tk.Frame(self, bg='#003278')
        self._content.pack(expand=True, fill='both')

        self.clock()

        self.minimize_button = tk.Button(self._top, text="-", command=self.iconify)
        self.minimize_button.pack(side='left')

        self.exit_button = tk.Button(self._top, text="X", command=self.quit)
        self.exit_button.pack(side='left')

    def clock(self):
        self.dateLabel = ClockLabel(self._header, "date")
        self.timeLabel = ClockLabel(self._header, "time")
        self.dayLabel = ClockLabel(self._header, "day")

# Login class for handling login functionality
class Login(Template):
    def __init__(self):
        super().__init__()
        self.attempts = 3

        self.TopLabel = tk.Label(self._header, text="Packer Unpacker : Login", fg='blue', font=("Century", 17))
        self.TopLabel.pack(pady=20)

        self.label1 = tk.Label(self._content, text="Username:", fg='gray', font=("Century", 14))
        self.label1.pack(pady=5)
        self.text1 = tk.Entry(self._content, font=("Century", 14))
        self.text1.pack(pady=5)

        self.label2 = tk.Label(self._content, text="Password:", fg='gray', font=("Century", 14))
        self.label2.pack(pady=5)
        self.text2 = tk.Entry(self._content, show='*', font=("Century", 14))
        self.text2.pack(pady=5)

        self.SUBMIT = tk.Button(self._content, text="SUBMIT", command=self.login, font=("Century", 14))
        self.SUBMIT.pack(pady=20)

    def validate(self, username, password):
        return len(username) >= 8 and len(password) >= 8

    def login(self):
        username = self.text1.get()
        password = self.text2.get()

        if not self.validate(username, password):
            messagebox.showerror("Error", "Short username or password")
            self.text1.delete(0, tk.END)
            self.text2.delete(0, tk.END)
            return

        if username == "Admin123" and password == "Admin123":
            self.destroy()
            NextPage(username).mainloop()
        else:
            self.attempts -= 1
            if self.attempts == 0:
                messagebox.showerror("Error", "Number of attempts finished")
                self.quit()
            else:
                messagebox.showerror("Error", "Incorrect login or password")

# Packer class for handling pack and unpack functionality
class Packer:
    def __init__(self, directory):
        self.directory = directory

    def pack(self):
        pack_name = f"packed_{datetime.now().strftime('%Y%m%d%H%M%S')}.zip"
        with zipfile.ZipFile(pack_name, 'w') as zipf:
            for root, dirs, files in os.walk(self.directory):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, self.directory)
                    zipf.write(file_path, arcname)
        print(f"Packed files into {pack_name}")

    def unpack(self, zip_file):
        with zipfile.ZipFile(zip_file, 'r') as zipf:
            zipf.extractall(self.directory)
        print(f"Unpacked {zip_file} into {self.directory}")

# Next page class for post-login functionality
class NextPage(Template):
    def __init__(self, username):
        super().__init__()
        self.label = tk.Label(self._header, text=f"Welcome: {username}", fg='blue', font=("Century", 17))
        self.label.pack(pady=20)

        self.pack_button = tk.Button(self._content, text="Pack Files", command=self.pack_files, font=("Century", 14))
        self.pack_button.pack(pady=10)

        self.unpack_button = tk.Button(self._content, text="Unpack Files", command=self.unpack_files, font=("Century", 14))
        self.unpack_button.pack(pady=10)

    def pack_files(self):
        directory = filedialog.askdirectory(title="Select Directory to Pack")
        if directory:
            packer = Packer(directory)
            packer.pack()
            messagebox.showinfo("Success", "Files packed successfully")

    def unpack_files(self):
        zip_file = filedialog.askopenfilename(title="Select Zip File to Unpack", filetypes=[("Zip files", "*.zip")])
        if zip_file:
            directory = filedialog.askdirectory(title="Select Directory to Unpack Into")
            if directory:
                packer = Packer(directory)
                packer.unpack(zip_file)
                messagebox.showinfo("Success", "Files unpacked successfully")

# Main function to run the application
if __name__ == "__main__":
    app = Login()
    app.mainloop()
