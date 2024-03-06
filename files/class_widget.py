# -*- coding: utf-8 -*-
from tkinter.ttk import*
from tkinter import*

class Combo():
    def __init__(self,name_style,FRAME,VALORES,indicador,width,text,grid) -> None:
        self.__name_style = name_style
        self.__grid = grid
        self.__FRAME = FRAME
        self.__indicador = indicador
        self.__colores,self.__valores = [x for x in VALORES],[VALORES[x] for x in VALORES]
        self.__color_contraste = ["black","maroon","red","darkviolet","dodgerblue","dimgrey"]
        self.__style = Style()
        self.__style.theme_use('alt')
        self.__combo = Combobox(FRAME,values = self.__valores,font =("arial",12,"bold"),cursor="hand2", state = 'readonly',width=width)
        self.__combo.grid(row=grid[0],column=grid[1],padx=5)
        self.__combo.set(text)
        self.__combo.configure(postcommand=lambda: self.__FRAME.after_idle(self.configure_items))
        self.__combo.bind("<<ComboboxSelected>>", lambda event: self.selection_changed(self.__combo.get()))
    def selection_changed(self,color):
        notfocus = "!focus"
        color_select=self.__colores[self.__valores.index(float(color))]
        fg = 'white'if self.__colores[self.__valores.index(float(color))] in self.__color_contraste else "black"
        self.__indicador.config_color(color_select)
        self.__style.map(f'{self.__name_style}.TCombobox', 
                        fieldbackground=[('readonly',self.__colores[self.__valores.index(float(color))])], 
                        foreground=[("readonly",notfocus,fg),
                        ("readonly", "focus", fg)],
                        selectforeground=[("readonly",notfocus, fg),
                                    ("readonly", "focus", fg)],
                        selectbackground=[
                        ("readonly", notfocus, self.__colores[self.__valores.index(float(color))]),
                        ("readonly", "focus", self.__colores[self.__valores.index(float(color))])
                        ])
        self.__combo["style"] = f"{self.__name_style}.TCombobox"
    def configure_items(self):
        lines = [f'set popdown [ttk::combobox::PopdownWindow {self.__combo}]']
        for i in self.__colores:
            lines.append(f'$popdown.f.l itemconfigure {self.__colores.index(i)} -background {i}')
            lines.append(f"$popdown.f.l itemconfigure {self.__colores.index(i)} -foreground {'white' if i in self.__color_contraste else 'black'}")
        self.__FRAME.tk.eval('\n'.join(lines))
    def hide(self):
        self.__combo.grid_forget()
    def show(self):
        self.__combo.grid(row=self.__grid[0],column=self.__grid[1],padx=5)
    def get_select(self):
        return self.__combo.get()
class Banda():
    def __init__(self,frame,row) -> None:
        self.__row = row
        self.__banda = Label(frame,text="?",width=1,highlightthickness=4,highlightcolor="black",highlightbackground="black",borderwidth=4)
        self.__banda.grid(row=0,column=self.__row,ipady=26)
    def hide(self):
        self.__banda.grid_forget()
    def show(self):
        self.__banda.grid(row=0,column=self.__row,ipady=26)
    def config_color(self,color):
        self.__banda.config(bg=color,text="")