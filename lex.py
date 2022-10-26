from table import tabla_simbolos
import tkinter as tk
import re 

class Lexico():
    def __init__(self):
        self.ctx = []
        self.estado = False
        self.tabla = tabla_simbolos

    def get_lex(self, ctx, text):
        temp = ctx.split(' ')
        temp = [lex.strip() for lex in temp]
        while '' in temp:
            temp.remove('')
        for lex in temp:
            encontrado = False
            for w in self.tabla:
                if lex == w['token']:
                    encontrado = True
                    break
            if not encontrado:
                valid = re.search("^[_a-zA-z]\\w*$", lex)
                if valid:
                    self.ctx.append({'token':lex,'descrip':'Identificador'})
                else:
                    valid = re.search("[-+]?\d+$|[-+]?\d+$\.|^\'.{1}\'|^\".+\"", lex)
                    if valid:
                        self.ctx.append({'token':lex,'descrip':'Valor'})
                    else:
                        self.ctx = list()
                        countVar = tk.StringVar()
                        pos = text.search(lex,"1.0",stopindex="end", count = countVar)
                        self.ctx.append((lex,pos))
                        self.estado = True
                        text.tag_configure("search", background="red")
                        text.tag_add("search", pos, "%s + %sc" % (pos, countVar.get()))
                        break
            else:
                self.ctx.append(w)


    def get_message(self):
        message = ''
        print(self.ctx)
        if self.estado:
            for e in self.ctx:
                message+= "Error token no reconocido: "+e[0]+ " en posicion: "+str(e[1])+"\n"
        else:
            for e in self.ctx:
                message+= "Token: "+e['token']+" - Descripcion: "+ e["descrip"]+"\n"
        ctx = list()
        return message