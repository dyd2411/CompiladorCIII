import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
import tkinter.scrolledtext as scrolledtext
from turtle import color
from lex import Lexico
import fitz

class ventana(tk.Tk):
    def __init__(self, title, minSize):
        super().__init__()
        
        self.config(background="#FFB6C1")
        self.title(title)
        self.txt_edit = scrolledtext.ScrolledText(self)
        self.frm_buttons = tk.Frame(self, relief=tk.FLAT, bd=2,background="#FFB6C1")
        self.txt_result = scrolledtext.ScrolledText(self,height=12,state='disabled')
        self.btn_run = tk.Button(self.frm_buttons, text="Inicio", command=self.run, background="#F5DEB3")
        self.btn_table = tk.Button(self.frm_buttons, text="Mostrar", background="#AFEEEE")

        self.frm_buttons.grid(row=1, column=0,rowspan=2, sticky="ns")
        self.txt_edit.grid(row=0, column=0, sticky="nsew", padx=30, pady=1)
        self.txt_result.grid(row=2, column=0, sticky="nsew",pady=35,padx=30), 

        self.btn_run.grid(row=2, column=0, sticky="ew", padx=1, pady=0)
        self.btn_table.grid(row=2, column=4, sticky="ew", padx=1, pady=0)
        self.btn_table.bind("<Button>", lambda e: Table_window())



    
    

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
        self.title("Tabla semantica")
        pdf1 = PDFViewer(self, width=90, height=50, spacing3=3, bg='blue')
        pdf1.grid(row=0, column=2, sticky='nsew')
        pdf1.show('Tabla-1.pdf')

class PDFViewer(scrolledtext.ScrolledText):
    def show(self, pdf_file):
        self.delete('1.0', 'end') 
        pdf = fitz.open(pdf_file) 
        self.images = []   
        for page in pdf:
            pix = page.get_pixmap()
            pix1 = fitz.Pixmap(pix, 0) if pix.alpha else pix
            photo = tk.PhotoImage(data=pix1.tobytes('ppm'))
            self.image_create('end', image=photo)
            self.insert('end', '\n')
            self.images.append(photo)


    
w = ventana("Analizador", 500 )
w.mainloop()
