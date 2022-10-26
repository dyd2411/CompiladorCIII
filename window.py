import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
import tkinter.scrolledtext as scrolledtext
from lex import Lexico
import fitz

class window(tk.Tk):
    def __init__(self, title, minSize):
        super().__init__()

        self.title(title)
        self.rowconfigure(0, minsize=minSize, weight=1)
        self.columnconfigure(1, minsize=minSize, weight=1)
        self.txt_edit = scrolledtext.ScrolledText(self)
        self.frm_buttons = tk.Frame(self, relief=tk.RAISED, bd=2)
        self.txt_result = scrolledtext.ScrolledText(self,height=12,state='disabled')
        self.btn_open = tk.Button(self.frm_buttons, text="Open", command=self.open_file)
        self.btn_save = tk.Button(self.frm_buttons, text="Save As...", command=self.save_file)
        self.btn_run = tk.Button(self.frm_buttons, text="Run", command=self.run)
        self.btn_table = tk.Button(self.frm_buttons, text="Show table")

        self.btn_open.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        self.btn_save.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
        self.btn_run.grid(row=2, column=0, sticky="ew", padx=5, pady=5)
        self.btn_table.grid(row=3, column=0, sticky="ew", padx=5, pady=5)
        self.btn_table.bind("<Button>", lambda e: Table_window())

        self.frm_buttons.grid(row=0, column=0,rowspan=2, sticky="ns")
        self.txt_edit.grid(row=0, column=1, sticky="nsew")
        self.txt_result.grid(row=1, column=1, sticky="nsew",pady=15)

    def open_file(self):
        """Open a file for editing."""
        filepath = askopenfilename(
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if not filepath:
            return
        self.txt_edit.delete("1.0", tk.END)
        with open(filepath, mode="r", encoding="utf-8") as input_file:
            text = input_file.read()
            self.txt_edit.insert(tk.END, text)
        self.title(f"Simple Text Editor - {filepath}")

    def save_file(self):
        """Save the current file as a new file."""
        filepath = asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
        )
        if not filepath:
            return
        with open(filepath, mode="w", encoding="utf-8") as output_file:
            text = self.txt_edit.get("1.0", tk.END)
            output_file.write(text)
        self.title(f"Simple Text Editor - {filepath}")

    def run(self):
        self.txt_result.configure(state='normal')
        self.txt_result.delete("1.0","end")
        input = self.txt_edit.get("1.0","end")
        lex = Lexico()
        res = lex.get_lex(input, self.txt_edit)
        message = lex.get_message()
        self.txt_result.insert(tk.END, message)
        self.txt_result.configure(state='disabled')

class Table_window(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master=master)
        self.title("Tabla de Símbolos")
        pdf1 = PDFViewer(self, width=70, height=30, spacing3=2, bg='blue')
        pdf1.grid(row=0, column=0, sticky='nsew')
        pdf1.show('Tabla-1.pdf')

class PDFViewer(scrolledtext.ScrolledText):
    def show(self, pdf_file):
        self.delete('1.0', 'end') # clear current content
        pdf = fitz.open(pdf_file) # open the PDF file
        self.images = []   # for storing the page images
        for page in pdf:
            pix = page.get_pixmap()
            pix1 = fitz.Pixmap(pix, 0) if pix.alpha else pix
            photo = tk.PhotoImage(data=pix1.tobytes('ppm'))
            # insert into the text box
            self.image_create('end', image=photo)
            self.insert('end', '\n')
            # save the image to avoid garbage collected
            self.images.append(photo)


    
w = window("Analizador léxico", 450)
w.mainloop()
