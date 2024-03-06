###########################################################################
from tkinter.ttk import *
from tkinter import messagebox
from tkinter import*
from files.class_widget import Combo,Banda

#######################  MESSI   ####################################################
main = Tk()
widht,height = int(main.winfo_screenwidth()/2),int(main.winfo_screenheight()/2)
main.title("R calculator by Orellana Matias y Vazquez Joaquin")
main.resizable(0,0)
main.iconbitmap("files/logo.ico")
main.geometry(f"{widht-int(widht/3)}x{height+100}+{widht-int(widht/2)}+{height-int(height/2)}")
Label(main, text="CALCULADORA DE RESISTENCIA",font=("arial",15,"bold")).pack(pady=(10,0))
FRAME_CONT = Frame(main)
FRAME_CONT.pack(fill=BOTH,expand=TRUE,pady=10,padx=10)
Boton_Select = StringVar()
F_RES = Frame(FRAME_CONT)
F_RES.pack()
file = PhotoImage(file="files/resistencia.png")
Label(F_RES,image=file,bg="violet",highlightthickness=4,highlightbackground="black").grid(row=0,column=0,columnspan=12)

b1 = Banda(F_RES,3);b2 = Banda(F_RES,4)
b3 = Banda(F_RES,5);b4 = Banda(F_RES,6)
b5 = Banda(F_RES,7);b6 = Banda(F_RES,8)
LABELS = [b1,b2,b3,b4,b5,b6]

F_banda = Frame(FRAME_CONT)
F_banda.pack(pady=10)

############################   19/02/24    ###############################################
VALORES = [{"black":0,"maroon":1,"red":2,"orange":3,"yellow":4,"limegreen":5,"dodgerblue":6,"darkviolet":7,"darkgrey":8,"white":9},
           {"black":1,"maroon":10,"red":100,"orange":1000,"yellow":10000,"limegreen":100000,"dodgerblue":1000000,"darkviolet":10000000, "darkgrey":100000000,"white":1000000000,"gold":0.1,"lightgrey":0.01},
           {"maroon":1,"red":2,"lawngreen":0.5,"dodgerblue":0.25,"darkviolet":0.1,"dimgrey":0.05,"gold":5,"lightgrey":10},
           {"black":250,"maroon":100,"red":50,"orange":15,"yellow":25,"lawngreen":20,"dodgerblue":10,"darkviolet":5,"dimgrey":1}]
c1 = Combo("custom1" ,F_banda,VALORES[0],b1,7,"Banda 1",[0,0])
c2 = Combo("custom2",F_banda,VALORES[0],b2,7,"Banda 2",[0,1])
c3 = Combo("custom3",F_banda,VALORES[0],b3,7,"Banda 3",[0,2])
c4 = Combo("custom4",F_banda,VALORES[1],b4,12,"Multiplicador",[0,3])
c5 = Combo("custom5",F_banda,VALORES[2],b5,9,"Tolerancia",[0,4])
c6 = Combo("custom6",F_banda,VALORES[3],b6,4,"TCR",[0,5])

###########################################################################
F_variacion = Frame(FRAME_CONT)
F_variacion.pack(pady=(0,5))
Label(F_variacion,text="VARIACIÓN DE TEMPERATURA +/- :").pack(side=LEFT)
Temperatura=Entry(F_variacion,width=6)
Temperatura.pack(side=LEFT)
Label(F_variacion,text="°C").pack(side=LEFT)

###########################################################################
###########################     RESULTADO      ############################
###########################################################################
F_respuesta = LabelFrame(FRAME_CONT,text="RESULTADO")
lbl = ["NÚMERO DE BANDAS :","DÍGITOS DE BANDAS:",
       "TOLERANCIA +/- :","V. NOMINAL MÁXIMO :",
       "VALOR NOMINAL :","V. NOMINAL MÍNIMO :",
       "TEMPERATURA :","TOLERANCIA CON Temp.  +/-:","VALOR NOMINAL CON Temp. :","% DE VARIACIÓN CON Temp.  +/-:"]
resultado = Text(F_respuesta,width=60,height=13)
resultado.grid(row=1,column=0,padx=10,pady=10)

###########################################################################
###########################################################################
###########################################################################

def calculate(n_bandas):
    try: 
        num_resistencia = IntVar()
        valor_nominal = 0
        minimo,maximo= 0,0
        tolerancia = 0
        tolerancia_temp = 0
        valor_nominal_temp = StringVar()
        porcentaje_tolerancia = 0
        if n_bandas in "34":
            num_resistencia.set(int(c1.get_select()+c2.get_select()))
            valor_nominal = num_resistencia.get()*float(c4.get_select())
        match n_bandas:
            case "3":
                tolerancia = valor_nominal*(20/100)
                minimo,maximo= valor_nominal-tolerancia,valor_nominal+tolerancia
            case "4":
                tolerancia = valor_nominal*(float(c5.get_select())/100)
                minimo,maximo= valor_nominal-tolerancia,valor_nominal+tolerancia
            case "5":
                num_resistencia.set(int(c1.get_select()+c2.get_select()+c3.get_select()))
                valor_nominal = num_resistencia.get()*float(c4.get_select())
                tolerancia = valor_nominal*(float(c5.get_select())/100)
                minimo,maximo= valor_nominal-tolerancia,valor_nominal+tolerancia
            case "6":
                num_resistencia.set(int(c1.get_select()+c2.get_select()+c3.get_select()))
                valor_nominal = num_resistencia.get()*float(c4.get_select())
                tolerancia = valor_nominal*(float(c5.get_select())/100)
                minimo,maximo= valor_nominal-tolerancia,valor_nominal+tolerancia
                # TOLERANCIA CON TEMPERATURA            
                # PORCENTAJE DE TOLERANCIA CON VARIACION DE TEMPERATURA XDDDDD
                if Temperatura.get()[0] in "+-":
                    tolerancia_temp =  round(valor_nominal*(int(c6.get_select())/1000000)*int(Temperatura.get()[1:]),4)
                    valor_nominal_temp.set((valor_nominal-tolerancia_temp)if Temperatura.get()[0] == "-" else (valor_nominal+tolerancia_temp))
                else:
                    messagebox.showinfo(message="LA TEMPERATURA DEBE CONTENER UN CARACTER + o - DE INCREMENTO O DECREMENTO", title="ADVERTENCIA", icon = "warning")
                porcentaje_tolerancia = round((tolerancia_temp/valor_nominal)*100,4)
        datos_resultado = [n_bandas,num_resistencia.get(),tolerancia,maximo,valor_nominal,minimo,Temperatura.get(),tolerancia_temp,valor_nominal_temp.get(),porcentaje_tolerancia]
        resultado.insert('end',"%50s"%('='*60)+"\n")
        for i in range(10):
            if i == 6: resultado.insert('end',"%50s\n"%('-'*40))
            simbolo = ("\n" if i in [0,1,9] else " Ω\n") if i in [0,1,2,3,4,5,7,8] else ("%\n" if i == 9 else "°C\n")
            resultado.insert('end',f"%30s {datos_resultado[i]}"%(lbl[i])+simbolo)
        resultado.insert('end',"%50s"%('='*60)+"\n")
    
    except(Exception):
        messagebox.showinfo(message="EXISTEN DATOS SELECCIONADOS\nQUE NO SON VÁLIDOS.", title="Advertencia", icon = "warning")
Button(FRAME_CONT,text="CALCULAR",bg="lightskyblue",font=("arial",11,"bold"),cursor="hand2",command=lambda:calculate(Boton_Select.get())).pack(side=TOP,ipady=10,ipadx=10,padx=20)
F_respuesta.pack()

#############################  BOTONES INFERIORES  ########################################
F_BOTONES = Frame(FRAME_CONT); F_BOTONES.pack(side=BOTTOM)
font_btn = ("Arial",12,"bold")
def function_button(number):
    Boton_Select.set(number)
    botones = F_BOTONES.winfo_children() # BOTONES QUE PERTENECEN AL FRAME BOTONES
    c_select = [c1,c2,c3,c4,c5,c6]
    b_select = [b1,b2,b3,b4,b5,b6]
    for x in botones:
        if x['text'][0] == number:
            x.configure(bg="green",fg="white")
            for i in range(6):
                match number:
                    case "3":
                        Temperatura.config(state=DISABLED)
                        c_select[i].hide() if c_select.index(c_select[i]) in [2,4,5] else c_select[i].show()
                        b_select[i].hide() if b_select.index(b_select[i]) in [2,4,5] else b_select[i].show()
                    case "4":
                        Temperatura.config(state=DISABLED)
                        c_select[i].show() if c_select.index(c_select[i]) not in [2,5] else c_select[i].hide()
                        b_select[i].show() if b_select.index(b_select[i]) not in [2,5] else b_select[i].hide()
                    case "5":
                        Temperatura.config(state=DISABLED)
                        c_select[i].hide() if c_select.index(c_select[i]) == 5 else c_select[i].show()
                        b_select[i].hide() if b_select.index(b_select[i]) == 5 else b_select[i].show()
                    case "6":
                        Temperatura.config(state=NORMAL)
                        c_select[i].show()
                        b_select[i].show()
        else:
            x.configure(bg="white",fg="green")

            #######  Arregala este coso  ######
def function_create(number):return lambda:function_button(number)
TXT_b=["3 BANDAS","4 BANDAS","5 BANDAS","6 BANDAS"]
for i in range(4):
    Button(F_BOTONES,text=TXT_b[i],bg="green"if i==3 else"white",fg="white"if i==3 else"green",font=font_btn,cursor="hand2",
           command=function_create(TXT_b[i][0])).pack(side=LEFT,padx=10)
Boton_Select.set("6")
main.mainloop()
