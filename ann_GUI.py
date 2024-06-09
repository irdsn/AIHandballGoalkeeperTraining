#!/usr/bin/env python
# -*- coding: utf-8 -*-

#LIBRERIAS
from tkinter import *
from tkinter import messagebox
import sys
import pylab as plt
import random
import copy
import ann_LOGIC

def ventanaSTATS(estadisticas):

    VENTANA_STATS=Toplevel()                                                 #Generamos ventana SECUNDARIA
    
    '''VENTANA_STATS: CARACTERISTICAS'''
    VENTANA_STATS.geometry("500x500+450+0")                                  #Tamaño ventana
    VENTANA_STATS.iconbitmap("goalkeeper.ico")                               #Icono ventana
    VENTANA_STATS.resizable(0,0)                                             #Tamaño ventana FIJO
    VENTANA_STATS.title("ESTADÍSTICAS DE LAS PREDICCIONES REALIZADAS")       #Titulo ventana
    
    '''VENTANA_STATS: LABELS'''
    Label(VENTANA_STATS, text=" \nESTADÍSTICAS DEL ENTRENAMIENTO\n", font=('Helvetica', 15, 'bold')).pack(fill=BOTH)
    
    '''VENTANA_STATS: SCROLLBAR'''
    scrollbarVS = Scrollbar(VENTANA_STATS)
    scrollbarVS.pack(side=RIGHT, fill=Y)
    
    listascrollVS=Listbox(VENTANA_STATS, font=('Helvetica', 12, 'bold'), yscrollcommand=scrollbarVS.set, bg="#000", fg="#fff", selectborderwidth=2)

    '''INSERTAMOS LAS PREDICCIONES DEL FICHERO LEIDO y ALMACENADO EN estadisticas[] EN LA LISTA listascrollVS[] DEL SCROLLBAR scrollbarVS'''
    for i in range(len(estadisticas)):
        if estadisticas[i]=='RESULTADOS FINALES:\n':
            continue
        else:
            listascrollVS.insert(END, "\n")
            listascrollVS.insert(END, estadisticas[i])
            
    listascrollVS.pack(fill=BOTH, expand=True)
    scrollbarVS.config(command=listascrollVS.yview)


    VENTANA_STATS.mainloop()

# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- #

def ventanaPREDICCIONES(predicciones,estadisticas):

    VENTANA_PREDICCIONES=Toplevel()                                          	#Generamos ventana SECUNDARIA
    
    '''VENTANA_PREDICCIONES: CARACTERISTICAS'''
    VENTANA_PREDICCIONES.geometry("800x600+400+0")                           	#Tamaño ventana
    VENTANA_PREDICCIONES.iconbitmap("goalkeeper.ico")                        	#Icono ventana
    VENTANA_PREDICCIONES.resizable(1,1)                                      	#Tamaño ventana FIJO
    VENTANA_PREDICCIONES.title("5.1. RESULTADOS ENTRENAMIENTO: PREDICCIONES")   #Titulo ventana
    
    '''VENTANA_PREDICCIONES: LABELS'''
    Label(VENTANA_PREDICCIONES, text=" \nPREDICCIONES REALIZADAS POR LA RED NEURONAL\n", font=('Helvetica', 15, 'bold')).pack(fill=BOTH)
    
    '''VENTANA_PREDICCIONES: SCROLLBAR'''
    scrollbarVPR = Scrollbar(VENTANA_PREDICCIONES)
    scrollbarVPR.pack(side=RIGHT, fill=Y)
    
    listascrollVPR=Listbox(VENTANA_PREDICCIONES, font=('Helvetica', 10), yscrollcommand=scrollbarVPR.set,selectborderwidth=2)

    '''INSERTAMOS LAS PREDICCIONES DEL FICHERO LEIDO y ALMACENADO EN predicciones[] EN LA LISTA listascrollVPR[] DEL SCROLLBAR scrollbarVPR'''
    for i in range(len(predicciones)):
        if predicciones[i]=='PREDICCIONES REALIZADAS POR LA RED:\n':
            continue
        else:
            listascrollVPR.insert(END, predicciones[i])
            
    listascrollVPR.pack(fill=BOTH, expand=True)
    scrollbarVPR.config(command=listascrollVPR.yview)

    Button(VENTANA_PREDICCIONES, text="Estadísticas", command=lambda:ventanaSTATS(estadisticas), font=('Helvetica', 15), width=15).pack(padx=60, pady=20, side=LEFT)
    Button(VENTANA_PREDICCIONES, text="Atrás", command=lambda:VENTANA_PREDICCIONES.destroy(), width=14, font=('Helvetica', 15)).pack(padx=60, pady=20, side=RIGHT)    
    VENTANA_PREDICCIONES.mainloop()

# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- #

def ventanaTERMERR(termino_err):

    VENTANA_TERMERR=Toplevel()                                                 #Generamos ventana SECUNDARIA
    
    '''VENTANA_TERMERR: CARACTERISTICAS'''
    VENTANA_TERMERR.geometry("800x600+350+0")                                  #Tamaño ventana
    VENTANA_TERMERR.iconbitmap("goalkeeper.ico")                               #Icono ventana
    VENTANA_TERMERR.resizable(1,1)                                             #Tamaño ventana FIJO
    VENTANA_TERMERR.title("5.3. RESULTADOS ENTRENAMIENTO: TÉRMINO DE ERROR")   #Titulo ventana
    
    '''VENTANA_TERMERR: LABELS'''
    Label(VENTANA_TERMERR, text=" \nEVOLUCION DEL TÉRMINO DE ERROR COMETIDO A LA SALIDA DE LA RED\n", font=('Helvetica', 15, 'bold')).pack(fill=BOTH)
    
    Label(VENTANA_TERMERR, text=" # Término de error: variación entre el resultado obtenido a la salida de la Red Neuronal Artificial y el que se deseaba obtener.", font=('Helvetica', 10), anchor=W).pack(fill=BOTH)
    Label(VENTANA_TERMERR, text=" # Número de epochs: cantidad de veces que ajustamos los pesos de las conexiones entre neuronas a partir del término de error obtenido.", font=('Helvetica', 10), anchor=W).pack(padx=1,fill=BOTH)
    
    '''VENTANA_TERMERR: SCROLLBAR'''
    scrollbarVTE = Scrollbar(VENTANA_TERMERR)
    scrollbarVTE.pack(side=RIGHT, fill=Y)
    
    listascrollVTE=Listbox(VENTANA_TERMERR, font=('Helvetica', 10), yscrollcommand=scrollbarVTE.set,selectborderwidth=2)

    '''INSERTAMOS EL TERMINO DE ERROR DEL FICHERO LEIDO y ALMACENADO EN termino_err[] EN LA LISTA listascrollVTE[] DEL SCROLLBAR scrollbarVTE'''
    for i in range(len(termino_err)):
        if termino_err[i]=='EVOLUCION DEL TÉRMINO DE ERROR COMETIDO A LA SALIDA DE LA RED\n':
            continue
        else:
            listascrollVTE.insert(END, termino_err[i])
            
    listascrollVTE.pack(fill=BOTH, expand=True)
    scrollbarVTE.config(command=listascrollVTE.yview)
    
    
    '''GENERAMOS GRAFICA DE LA EVOLUCION DEL TERMINO DE ERROR CONTENIDA EN termino_err[]'''
    figureVTE = plt.figure("REPRESENTACIÓN DE LA EVOLUCIÓN DEL TÉRMINO DE ERROR", figsize=(9,7))    #Ajustamos tamaño de la figura (ventana) donde se encuentra la gráfica

    #Debemos filtrar el string y extraer los términos de error obtenidos
    terminos=[]
    for i in range(len(termino_err)):
        evo=termino_err[i]
        if evo=='EVOLUCION DEL TÉRMINO DE ERROR COMETIDO A LA SALIDA DE LA RED\n':
            continue
        else:
            for t in evo.split('='):
                try:
                    terminos.append(float(t))               #Terminos de error filtrados y almacenados en terminos[]
                except ValueError:
                    pass

    x = plt.linspace(0, len(terminos), len(terminos))
    plt.plot(x, terminos[:])
    
    plt.xlabel('nº Epoch', fontsize=12)                      #Titulo eje x
    plt.ylabel('Término de error', fontsize=12)              #Titulo eje y
    plt.title('EVOLUCIÓN TÉRMINO DE ERROR\n', fontsize=15)   #Titulo de la grafica
    
    Button(VENTANA_TERMERR, text="Evolución", command=figureVTE.show, width=14, font=('Helvetica', 15)).pack(padx=60, pady=20, side=LEFT)
    Button(VENTANA_TERMERR, text="Atrás", command=lambda:VENTANA_TERMERR.destroy(), width=14, font=('Helvetica', 15)).pack(padx=60, pady=20, side=RIGHT)

    VENTANA_TERMERR.mainloop()

# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- #

def ventanaRESULTADOS(n_hidden,l_rate,n_epoch,datasetVP):

    VENTANA_RESULTADOS=Toplevel()                                             #Generamos ventana SECUNDARIA
    
    dataset_figureVR=copy.deepcopy(datasetVP)                                 #Realizamos deepcopy del datasetVP de entrada
    
    '''VENTANA_RESULTADOS: CARACTERISTICAS'''
    VENTANA_RESULTADOS.geometry("900x800+300+0")                              #Tamaño ventana
    VENTANA_RESULTADOS.iconbitmap("goalkeeper.ico")                           #Icono ventana
    VENTANA_RESULTADOS.resizable(1,1)                                         #Tamaño ventana FIJO
    VENTANA_RESULTADOS.title("5. RESULTADOS DEL ENTRENAMIENTO")   			  #Titulo ventana
    
    '''VENTANA_RESULTADOS: LABELS'''
    Label(VENTANA_RESULTADOS, text=" \nRESULTADOS DEL ENTRENAMIENTO\n", font=('Helvetica', 15, 'bold')).pack(fill=BOTH)
    Label(VENTANA_RESULTADOS, text=" # A continuación se muestra el resultado del entrenamiento realizado (información contenida en el fichero resultado_entrenamiento.txt):", font=('Helvetica', 10), anchor=W).pack(fill=BOTH)
     
    '''¡ENTRENAMOS!'''
    ann_LOGIC.complete_training(n_hidden,l_rate,n_epoch,datasetVP)   		  #Ejecutamos codigo de la Red Neuronal Artificial
    
    '''LEEMOS FICHERO ESPECIFICADO COMO SALIDA EN EL CODIGO DE LA RED NEURONAL, ALMACENAMOS EN LA LISTA linesVR[], termino_err=[], predicciones=[] LA PARTE CORRESPONDIENTE y CERRAMOS FICHERO'''
    #opf=open('resultado_entrenamiento.txt','r')
    outputfile=ann_LOGIC.getOutputFile()
    opf=open(outputfile,'r')

    linesVR=[]
    termino_err=[]
    predicciones=[]
    estadisticas=[]
    
    for line in opf:
        if '---------' in line:
            continue
        elif line=='EVOLUCION DEL TÉRMINO DE ERROR COMETIDO A LA SALIDA DE LA RED\n' or '>>epoch' in line:
            termino_err.append(line)
        elif line=='PREDICCIONES REALIZADAS POR LA RED:\n' or line=='**VALORES NORMALIZADOS ENTRE 0 Y 1\n' or '--[x,y]:' in line:
            predicciones.append(line)
        elif line=='RESULTADOS FINALES:\n' or '~' in line:
            estadisticas.append(line)
        else:   
            linesVR.append(line)
    opf.close()
    
    '''VENTANA_RESULTADOS: SCROLLBAR'''
    scrollbarVR = Scrollbar(VENTANA_RESULTADOS)
    scrollbarVR.pack(side=RIGHT, fill=Y)
    
    listascrollVR=Listbox(VENTANA_RESULTADOS, font=('Helvetica', 10), yscrollcommand=scrollbarVR.set,selectborderwidth=2)

    '''INSERTAMOS EL FICHERO LEIDO y ALMACENADO EN linesVR[] EN LA LISTA listascrollVR[] DEL SCROLLBAR'''
    for i in range(len(linesVR)):
        listascrollVR.insert(END, linesVR[i])
            
    listascrollVR.pack(fill=BOTH, expand=True)
    scrollbarVR.config(command=listascrollVR.yview)

    '''GENERAMOS GRAFICA CON LAS COORDENADAS (x,y) ALMACENADAS EN patrones_dataset[]'''
    figureVR = plt.figure("5.2. REPRESENTACIÓN LANZAMIENTOS REALIZADOS", figsize=(9,7))             #Ajustamos tamaño de la figura (ventana) donde se encuentra la gráfica
    img = plt.imread("goal_axes.png")                       #Leemos imagen de la porteria para usarla de fondo en la grafica a generar
    ax = plt.axes([0.08, 0.05, 0.9, 0.9])                   #Ajustamos la grafica en la figura (ventana)
    for i in range(len(dataset_figureVR)):
            patrones_dataset=dataset_figureVR[i]            #Sacamos cada patron del dataset_figureVR de entrada y extraemos los parametros de lanzamiento (x,y) en las posiciones [2] y [3] de cada patron
            x_coord=float(patrones_dataset[2])              #Extraemos la coordenada x de patrones_dataset[] y la almacenamos en x_coord
            y_coord=float(patrones_dataset[3])              #Extraemos la coordenada y de patrones_dataset[] y la almacenamos en y_coord
            plt.scatter(x_coord, y_coord, c="Blue", marker='o', s=75, alpha=0.7)
    
    ax.imshow(img, extent=[0, 3.16, 0, 2.08])
    
    plt.xlim(0, 3.16)                                       #Ajustamos limite del eje x al ancho de la porteria (3.16m)
    plt.ylim(0, 2.08)                                       #Ajustamos limite del eje y al alto de la porteria (2.08m)
    
    plt.xlabel('x (m)', fontsize=12)                        #Titulo eje x
    plt.ylabel('y (m)', fontsize=12)                        #Titulo eje y
    plt.title('LANZAMIENTOS REALIZADOS\n', fontsize=15)     #Titulo de la grafica

    '''VENTANA_RESULTADOS: BOTONES''' 
    Button(VENTANA_RESULTADOS, text="Predicciones", command=lambda:ventanaPREDICCIONES(predicciones,estadisticas), font=('Helvetica', 15), width=15).pack(padx=10, pady=20, side=LEFT)
    Button(VENTANA_RESULTADOS, text="Lanzamientos", command=figureVR.show, font=('Helvetica', 15), width=15).pack(padx=10, pady=20, side=LEFT)
    Button(VENTANA_RESULTADOS, text="Término de error", command=lambda:ventanaTERMERR(termino_err), font=('Helvetica', 15), width=15).pack(padx=10, pady=20, side=LEFT)
    Button(VENTANA_RESULTADOS, text="Salir", command=lambda:sys.exit(), width=14, font=('Helvetica', 15)).pack(padx=10, pady=20, side=RIGHT)


    VENTANA_RESULTADOS.mainloop()

# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- #

def ventanaPARAMETROS(datasetVD):

    VENTANA_PARAMETROS=Toplevel()                                      #Generamos ventana SECUNDARIA
    
    '''VENTANA_PARAMETROS: CARACTERISTICAS'''
    #VENTANA_PARAMETROS.geometry("1000x1000+300+0")                    #Tamaño ventana
    VENTANA_PARAMETROS.iconbitmap("goalkeeper.ico")                    #Icono ventana
    VENTANA_PARAMETROS.resizable(0,0)                                  #Tamaño ventana FIJO
    VENTANA_PARAMETROS.title("4. PARÁMETROS RED NEURONAL ARTIFICIAL")  #Titulo ventana
    
    '''VENTANA_PARAMETROS: LABELS y ENTRYS'''
    Label(VENTANA_PARAMETROS, text="PARÁMETROS DE LA RED NEURONAL ARTIFICIAL", font=('Helvetica', 15, 'bold')).grid(row=0, column=0, sticky=E, pady=15)
    Label(VENTANA_PARAMETROS, text=" # Es necesario especificar los siguientes parámetros para comenzar el entrenamiento:", font=('Helvetica', 10), anchor=W).grid(row=1, column=0, sticky=W)

    
    '''Nº Neuronas en la capa oculta'''
    Label(VENTANA_PARAMETROS, text=" · Número de neuronas en la capa oculta: ", font=('Helvetica', 10, 'bold'), anchor=W).grid(row=2, column=0, sticky=W)
    Label(VENTANA_PARAMETROS, text="    *Valor numérico entero y positivo, p.e.: 2, 3, 4.", font=('Helvetica', 8), anchor=W).grid(row=3, column=0, sticky=W)
    entryVP_1 = Entry(VENTANA_PARAMETROS, font=('Helvetica', 12, 'bold'), justify=CENTER)
    entryVP_1.grid(row=2, column=1, padx=20, pady=5)

    '''Coeficiente de aprendizaje'''
    Label(VENTANA_PARAMETROS, text=" · Coeficiente de aprendizaje: ", font=('Helvetica', 10, 'bold'), anchor=W).grid(row=4, column=0, sticky=W)
    Label(VENTANA_PARAMETROS, text="    *Valor numérico decimal y positivo entre 0 y 1, p.e.: 0.3, 0.5, 0.8.", font=('Helvetica', 8), anchor=W).grid(row=5, column=0, sticky=W)
    entryVP_2 = Entry(VENTANA_PARAMETROS, font=('Helvetica', 12, 'bold'), justify=CENTER)
    entryVP_2.grid(row=4, column=1, padx=20, pady=5)
    
    '''Nº Epochs'''
    Label(VENTANA_PARAMETROS, text=" · Número de epochs: ", font=('Helvetica', 10, 'bold'), anchor=W).grid(row=6, column=0, sticky=W)
    Label(VENTANA_PARAMETROS, text="    *Valor numérico entero y positivo, p.e.: 100, 1000, 10000.", font=('Helvetica', 8), anchor=W).grid(row=7, column=0, sticky=W)
    entryVP_3 = Entry(VENTANA_PARAMETROS, font=('Helvetica', 12, 'bold'), justify=CENTER)
    entryVP_3.grid(row=6, column=1, padx=20, pady=5)
    
    
    Label(VENTANA_PARAMETROS, text="\n\n # Los siguientes parámetros son constantes:", font=('Helvetica', 10), anchor=W).grid(row=8, column=0, sticky=W)
    '''Nº Neuronas en la capa de entrada'''
    Label(VENTANA_PARAMETROS, text=" · Número de neuronas en la capa de entrada:", font=('Helvetica', 10, 'bold'), anchor=W).grid(row=9, column=0, sticky=W, pady=5)
    n_inputs = StringVar()
    n_inputs.set('5')
    entryVP_4 = Entry(VENTANA_PARAMETROS, textvariable=n_inputs, font=('Helvetica', 12, 'bold'), justify=CENTER, state="readonly")
    entryVP_4.grid(row=9, column=1, padx=20, pady=5)
    
    '''Nº Neuronas en la capa de salida'''
    Label(VENTANA_PARAMETROS, text=" · Número de neuronas en la capa de salida:", font=('Helvetica', 10, 'bold'), anchor=W).grid(row=10, column=0, sticky=W, pady=5)
    n_outputs = StringVar()
    n_outputs.set('2')
    entryVP_5 = Entry(VENTANA_PARAMETROS, textvariable=n_outputs, font=('Helvetica', 12, 'bold'), justify=CENTER, state="readonly")
    entryVP_5.grid(row=10, column=1, padx=20, pady=5)

    '''VALIDACION DE LOS DATOS INTRODUCIDOS'''
    def datos():
        #CONTROL DE ERRORES AL INTRODUCIR LOS DATOS
        if len(entryVP_1.get())==0 or len(entryVP_2.get())==0 or len(entryVP_3.get())==0:
            #CAMPOS VACIOS
            messagebox.showerror("ERROR: FALTAN CAMPOS POR RELLENAR", "¡DATOS INTRODUCIDOS INCORRECTOS!\n\n*Es necesario rellenar todos los campos.\n*Vuelva a la ventana anterior para realizarlo.")
        else:
            if int(entryVP_1.get())<=0 or float(entryVP_2.get())<0 or float(entryVP_2.get())>1 or int(entryVP_3.get())<0 :
                #ALGUN PARAMETRO ESPECIFICO INCORRECTO
                messagebox.showerror("ERROR: PARÁMETROS INCORRECTOS", "¡DATOS INTRODUCIDOS INCORRECTOS!\n\n*Se deben introducir valores numéricos enteros y positivos, excepto para el coeficiente de aprendizaje.\n*El coeficiente de aprendizaje debe ser un valor númerico decimal y positivo entre 0 y 1. Por externo: 0.5")            
            else:
                #TODOS LOS PARAMETROS CORRECTOS
                messagebox.showinfo("PARÁMETROS ESPECIFICADOS", "· Número de neuronas en la capa de entrada:    5"+"\n· Número de neuronas en la capa oculta:    "+entryVP_1.get()+"\n· Número de neuronas en la capa de salida:    2"+"\n· Coeficiente de aprendizaje:    "+entryVP_2.get()+"\n· Número de epochs:    "+entryVP_3.get())
            
                inserted = StringVar()
                
                '''n_hidden'''
                inserted.set(entryVP_1.get())
                n_hidden=int(inserted.get())
                
                '''l_rate'''
                inserted.set(entryVP_2.get())
                l_rate=float(inserted.get())
                
                '''n_epoch'''
                inserted.set(entryVP_3.get())
                n_epoch=int(inserted.get())
                
                ventanaRESULTADOS(n_hidden,l_rate,n_epoch,datasetVD)   #Llamamos a la funcion ventanaRESULTADOS() y le pasamos los parametros introducidos por el usuario para que pueda ejecutar la función de complete_training()
                
    '''VENTANA_PARAMETROS: BOTONES'''
    Button(VENTANA_PARAMETROS, text="Continuar", command=datos, width=14, font=15).grid(row=11, column=1, sticky=NSEW, padx=20, pady=20)

    #VENTANA_PARAMETROS.mainloop()

# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- #

def ventanaDATASET(datasetVE):

    VENTANA_DATASET=Toplevel()                                                               #Generamos ventana SECUNDARIA

    '''VENTANA_DATASET: CARACTERISTICAS'''
    VENTANA_DATASET.geometry("900x800+200+0")                                                #Tamaño ventana
    VENTANA_DATASET.iconbitmap("goalkeeper.ico")                                             #Icono ventana
    VENTANA_DATASET.resizable(1,1)                                                           #Tamaño ventana FIJO
    VENTANA_DATASET.title("3. PATRONES DE ENTRADA A LA RED NEURONAL ARTIFICIAL: DATASET")    #Titulo ventana
    
    '''VENTANA_DATASET: LABEL'''
    Label(VENTANA_DATASET, text=" \nPATRONES DE ENTRADA\n", font=('Helvetica', 15, 'bold')).pack(fill=BOTH)
    Label(VENTANA_DATASET, text=" # El patrón de entrada tiene la siguiente estructura:\n", font=('Helvetica', 10), anchor=W).pack(fill=BOTH)
    Label(VENTANA_DATASET, text=" [Distancia(m),  Velocidad(km/h),  x(m),  y(m),  Salida deseada(0,1)]\n", font=('Helvetica', 12, 'bold')).pack(fill=BOTH)
    
    '''OBTENEMOS DATASET LEÍDO (OPCIONES 'General' Y 'Ejemplo') O GENERADO (OPCION 'Personalizado') FILTRANDO POR EL TIPO DE LA VARIABLE DE ENTRADA A NUESTRA FUNCION ventanaDATASET()'''
    if type(datasetVE) == list:
        #Dataset PERSONALIZADO
        datasetVD=datasetVE[:]
    else:
        #Dataset GENERAL o EJEMPLO
        datasetVD=ann_LOGIC.load_csv(datasetVE)
        
    
    '''VENTANA_DATASET: SCROLLBAR'''
    scrollbarVD = Scrollbar(VENTANA_DATASET)
    scrollbarVD.pack(side=RIGHT, fill=Y)
    
    listascrollVD=Listbox(VENTANA_DATASET, font=('Helvetica', 12), yscrollcommand=scrollbarVD.set,selectborderwidth=2)

    '''INSERTAMOS EL FICHERO LEIDO y ALMACENADO EN datasetVP EN LA LISTA listascrollVD[] DEL SCROLLBAR'''
    for i in range(len(datasetVD)):
        listascrollVD.insert(END, str(datasetVD[i]))
        
    listascrollVD.pack(fill=BOTH, expand=True)
    scrollbarVD.config(command=listascrollVD.yview)
    
    '''VENTANA_DATASET: BOTONES''' 
    Button(VENTANA_DATASET, text="Continuar", command=lambda:ventanaPARAMETROS(datasetVD), width=16, font=('Helvetica', 15)).pack(padx=100, pady=20, side=LEFT)
    Button(VENTANA_DATASET, text="Atrás", command=lambda:VENTANA_DATASET.destroy(), width=16, font=('Helvetica', 15)).pack(padx=100, pady=20, side=RIGHT)
    
    #VENTANA_DATASET.mainloop()
    
# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- #

def ventanaEPERSONALIZADO():

    VENTANA_EPERSONALIZADO=Toplevel()                               #Generamos ventana SECUNDARIA
    
    '''VENTANA_EPERSONALIZADO: CARACTERISTICAS'''
    VENTANA_EPERSONALIZADO.geometry("690x650+200+0")                #Tamaño ventana especifico para ajustarse al tamaño de la imagen de fondo a utilizar
    VENTANA_EPERSONALIZADO.iconbitmap("goalkeeper.ico")             #Icono ventana
    VENTANA_EPERSONALIZADO.resizable(0,0)                           #Tamaño ventana FIJO
    VENTANA_EPERSONALIZADO.title("2. ENTRENAMIENTO PERSONALIZADO")  #Titulo ventana
    
    '''VENTANA_EPERSONALIZADO: FONDO PORTERIA'''
    imagenVEP = PhotoImage(file="goal_axes.png")
    Label(VENTANA_EPERSONALIZADO, image=imagenVEP).place(x=0, y=-20, relwidth=1, relheight=1)
    
    '''VENTANA_EPERSONALIZADO: LABELS'''
    Label(VENTANA_EPERSONALIZADO, text="¡LANZA A PORTERÍA!", font=('Helvetica', 15, 'bold')).grid(row=0, column=1, sticky=NSEW, pady=15)
    
    lblVEP_1 = Label(VENTANA_EPERSONALIZADO, font=('Helvetica', 10),width=26)
    lblVEP_1.config(text="Lanzamiento")
    lblVEP_2 = Label(VENTANA_EPERSONALIZADO, font=('Helvetica', 12, 'bold'),width=25)
    lblVEP_2.config(text='Patrón')

    
    datasetEP=[]
    
    def add_tiro(lugar):
        #Lanzamiento a la esquina SUP_IZDA
        if lugar==1:
            
            distancia = round(random.uniform(6.90,10.50),2)                             #Generamos para la distancia un numero aleatorio decimal (funcion random.uniform()) entre 6.90m y 10.50m y redondeamos a 2 decimales mediante la funcion round()
            velocidad = round(random.uniform(85,110),2)                                 #Generamos para la velocidad un numero aleatorio decimal (funcion random.uniform()) entre 85km/h y 110km/h y redondeamos a 2 decimales mediante la funcion round()
            x = round(random.uniform(0.00,1.05),2)                                      #Generamos para la coordenada x un numero aleatorio decimal (funcion random.uniform()) entre 0.00m y 1.05m - Para lanzamiento a la esquina SUP_IZDA
            y = round(random.uniform(1.39,2.08),2)                                      #Generamos para la coordenada y un numero aleatorio decimal (funcion random.uniform()) entre 1.39m y 2.08m - Para lanzamiento a la esquina SUP_IZDA
            esperado = random.choice((0,1))                                             #Realizamos para el resultado esperado una eleccion aleatoria (funcion random.choice()) entre 0 y 1
            patron = [str(distancia), str(velocidad), str(x), str(y), str(esperado)]    #Formamos el patron de entrada a la Red Neuronal Artificial
            datasetEP.append(patron)                                                    #Lo añadimos al dataset de entrada a la Red Neuronal Artificial
            
            #Mostramos resultado del patrón generado
            #messagebox.showinfo("LANZAMIENTO REALIZADO", "¡Se lanzó a la ESQUINA SUPERIOR IZQUIERDA de la portería!\n\n Patrón añadido al dataset de entrada de la Red Neuronal:\n["+patron[0]+" "+patron[1]+" "+patron[2]+" "+patron[3]+" "+patron[4]+"]")
            lblVEP_1.config(text="¡Se lanzó a la ESQUINA SUPERIOR\n IZQUIERDA de la portería!")
            lblVEP_2.config(text=str(patron))

            
        #Lanzamiento al SUP_CNTR
        if lugar==2:
            distancia = round(random.uniform(6.90,10.50),2)                             #Generamos para la distancia un numero aleatorio decimal (funcion random.uniform()) entre 6.90m y 10.50m y redondeamos a 2 decimales mediante la funcion round()
            velocidad = round(random.uniform(85,110),2)                                 #Generamos para la velocidad un numero aleatorio decimal (funcion random.uniform()) entre 85km/h y 110km/h y redondeamos a 2 decimales mediante la funcion round()
            x = round(random.uniform(1.05,2.11),2)                                      #Generamos para la coordenada x un numero aleatorio decimal (funcion random.uniform()) entre 1.05m y 2.11m - Para lanzamiento al SUP_CNTR
            y = round(random.uniform(1.39,2.08),2)                                      #Generamos para la coordenada y un numero aleatorio decimal (funcion random.uniform()) entre 1.39m y 2.08m - Para lanzamiento al SUP_CNTR
            esperado = random.choice((0,1))                                             #Realizamos para el resultado esperado una eleccion aleatoria (funcion random.choice()) entre 0 y 1
            patron = [str(distancia), str(velocidad), str(x), str(y), str(esperado)]    #Formamos el patron de entrada a la Red Neuronal Artificial
            datasetEP.append(patron)                                                    #Lo añadimos al dataset de entrada a la Red Neuronal Artificial
            
            #Mostramos resultado del patrón generado
            #messagebox.showinfo("LANZAMIENTO REALIZADO", "¡Se lanzó al CENTRO SUPERIOR de la portería!\n\n Patrón añadido al dataset de entrada de la Red Neuronal:\n["+patron[0]+" "+patron[1]+" "+patron[2]+" "+patron[3]+" "+patron[4]+"]")
            lblVEP_1.config(text="¡Se lanzó al CENTRO\n SUPERIOR de la portería!")
            lblVEP_2.config(text=str(patron))
            
        #Lanzamiento a la esquina SUP_DCHA
        if lugar==3:
            distancia = round(random.uniform(6.90,10.50),2)                             #Generamos para la distancia un numero aleatorio decimal (funcion random.uniform()) entre 6.90m y 10.50m y redondeamos a 2 decimales mediante la funcion round()
            velocidad = round(random.uniform(85,110),2)                                 #Generamos para la velocidad un numero aleatorio decimal (funcion random.uniform()) entre 85km/h y 110km/h y redondeamos a 2 decimales mediante la funcion round()
            x = round(random.uniform(2.11,3.16),2)                                      #Generamos para la coordenada x un numero aleatorio decimal (funcion random.uniform()) entre 2.11m y 3.16m - Para lanzamiento a la esquina SUP_DCHA
            y = round(random.uniform(1.39,2.08),2)                                      #Generamos para la coordenada y un numero aleatorio decimal (funcion random.uniform()) entre 1.39m y 2.08m - Para lanzamiento a la esquina SUP_DCHA
            esperado = random.choice((0,1))                                             #Realizamos para el resultado esperado una eleccion aleatoria (funcion random.choice()) entre 0 y 1
            patron = [str(distancia), str(velocidad), str(x), str(y), str(esperado)]    #Formamos el patron de entrada a la Red Neuronal Artificial
            datasetEP.append(patron)                                                    #Lo añadimos al dataset de entrada a la Red Neuronal Artificial
            
            #Mostramos resultado del patrón generado
            #messagebox.showinfo("LANZAMIENTO REALIZADO", "¡Se lanzó a la ESQUINA SUPERIOR DERECHA de la portería!!\n\n Patrón añadido al dataset de entrada de la Red Neuronal:\n["+patron[0]+" "+patron[1]+" "+patron[2]+" "+patron[3]+" "+patron[4]+"]")
            lblVEP_1.config(text="¡Se lanzó a la ESQUINA SUPERIOR\n DERECHA de la portería!")
            lblVEP_2.config(text=str(patron))
            
        #Lanzamiento a la IZQUIERDA
        if lugar==4:
            distancia = round(random.uniform(6.90,10.50),2)                             #Generamos para la distancia un numero aleatorio decimal (funcion random.uniform()) entre 6.90m y 10.50m y redondeamos a 2 decimales mediante la funcion round()
            velocidad = round(random.uniform(85,110),2)                                 #Generamos para la velocidad un numero aleatorio decimal (funcion random.uniform()) entre 85km/h y 110km/h y redondeamos a 2 decimales mediante la funcion round()
            x = round(random.uniform(0.00,1.05),2)                                      #Generamos para la coordenada x un numero aleatorio decimal (funcion random.uniform()) entre 0.00m y 1.05m - Para lanzamiento a la IZQUIERDA
            y = round(random.uniform(0.70,1.39),2)                                      #Generamos para la coordenada y un numero aleatorio decimal (funcion random.uniform()) entre 0.70m y 1.39m - Para lanzamiento a la IZQUIERDA
            esperado = random.choice((0,1))                                             #Realizamos para el resultado esperado una eleccion aleatoria (funcion random.choice()) entre 0 y 1
            patron = [str(distancia), str(velocidad), str(x), str(y), str(esperado)]    #Formamos el patron de entrada a la Red Neuronal Artificial
            datasetEP.append(patron)                                                    #Lo añadimos al dataset de entrada a la Red Neuronal Artificial
            
            #Mostramos resultado del patrón generado
            #messagebox.showinfo("LANZAMIENTO REALIZADO", "¡Se lanzó a la IZQUIERDA de la portería!!\n\n Patrón añadido al dataset de entrada de la Red Neuronal:\n["+patron[0]+" "+patron[1]+" "+patron[2]+" "+patron[3]+" "+patron[4]+"]")
            lblVEP_1.config(text="¡Se lanzó a la IZQUIERDA\n de la portería!")
            lblVEP_2.config(text=str(patron))
            
        #Lanzamiento al CENTRO
        if lugar==5:
            distancia = round(random.uniform(6.90,10.50),2)                             #Generamos para la distancia un numero aleatorio decimal (funcion random.uniform()) entre 6.90m y 10.50m y redondeamos a 2 decimales mediante la funcion round()
            velocidad = round(random.uniform(85,110),2)                                 #Generamos para la velocidad un numero aleatorio decimal (funcion random.uniform()) entre 85km/h y 110km/h y redondeamos a 2 decimales mediante la funcion round()
            x = round(random.uniform(1.05,2.11),2)                                      #Generamos para la coordenada x un numero aleatorio decimal (funcion random.uniform()) entre 1.05m y 2.11m - Para lanzamiento al CENTRO
            y = round(random.uniform(0.70,1.39),2)                                      #Generamos para la coordenada y un numero aleatorio decimal (funcion random.uniform()) entre 0.70m y 1.39m - Para lanzamiento al CENTRO
            esperado = random.choice((0,1))                                             #Realizamos para el resultado esperado una eleccion aleatoria (funcion random.choice()) entre 0 y 1
            patron = [str(distancia), str(velocidad), str(x), str(y), str(esperado)]    #Formamos el patron de entrada a la Red Neuronal Artificial
            datasetEP.append(patron)                                                    #Lo añadimos al dataset de entrada a la Red Neuronal Artificial
           
            #Mostramos resultado del patrón generado
            #messagebox.showinfo("LANZAMIENTO REALIZADO", "¡Se lanzó al CENTRO de la portería!!\n\n Patrón añadido al dataset de entrada de la Red Neuronal:\n["+patron[0]+" "+patron[1]+" "+patron[2]+" "+patron[3]+" "+patron[4]+"]")
            lblVEP_1.config(text="¡Se lanzó al CENTRO de la portería!")
            lblVEP_2.config(text=str(patron))

        #Lanzamiento a la DERECHA
        if lugar==6:
            distancia = round(random.uniform(6.90,10.50),2)                             #Generamos para la distancia un numero aleatorio decimal (funcion random.uniform()) entre 6.90m y 10.50m y redondeamos a 2 decimales mediante la funcion round()
            velocidad = round(random.uniform(85,110),2)                                 #Generamos para la velocidad un numero aleatorio decimal (funcion random.uniform()) entre 85km/h y 110km/h y redondeamos a 2 decimales mediante la funcion round()
            x = round(random.uniform(2.11,3.16),2)                                      #Generamos para la coordenada x un numero aleatorio decimal (funcion random.uniform()) entre 2.11m y 3.16m - Para lanzamiento a la DERECHA
            y = round(random.uniform(0.70,1.39),2)                                      #Generamos para la coordenada y un numero aleatorio decimal (funcion random.uniform()) entre 0.70m y 1.39m - Para lanzamiento a la DERECHA
            esperado = random.choice((0,1))                                             #Realizamos para el resultado esperado una eleccion aleatoria (funcion random.choice()) entre 0 y 1
            patron = [str(distancia), str(velocidad), str(x), str(y), str(esperado)]    #Formamos el patron de entrada a la Red Neuronal Artificial
            datasetEP.append(patron)                                                    #Lo añadimos al dataset de entrada a la Red Neuronal Artificial
            
            #Mostramos resultado del patrón generado
            #messagebox.showinfo("LANZAMIENTO REALIZADO", "¡Se lanzó a la DERECHA de la portería!!\n\n Patrón añadido al dataset de entrada de la Red Neuronal:\n["+patron[0]+" "+patron[1]+" "+patron[2]+" "+patron[3]+" "+patron[4]+"]")
            lblVEP_1.config(text="¡Se lanzó a la DERECHA\n de la portería!")
            lblVEP_2.config(text=str(patron))

        #Lanzamiento a la esquina INF_IZDA
        if lugar==7:
            distancia = round(random.uniform(6.90,10.50),2)                             #Generamos para la distancia un numero aleatorio decimal (funcion random.uniform()) entre 6.90m y 10.50m y redondeamos a 2 decimales mediante la funcion round()
            velocidad = round(random.uniform(85,110),2)                                 #Generamos para la velocidad un numero aleatorio decimal (funcion random.uniform()) entre 85km/h y 110km/h y redondeamos a 2 decimales mediante la funcion round()
            x = round(random.uniform(0.00,1.05),2)                                      #Generamos para la coordenada x un numero aleatorio decimal (funcion random.uniform()) entre 0.00m y 1.05m - Para lanzamiento a la esquina INF_IZDA
            y = round(random.uniform(0.00,0.70),2)                                      #Generamos para la coordenada y un numero aleatorio decimal (funcion random.uniform()) entre 0.00m y 0.70m - Para lanzamiento a la esquina INF_IZDA
            esperado = random.choice((0,1))                                             #Realizamos para el resultado esperado una eleccion aleatoria (funcion random.choice()) entre 0 y 1
            patron = [str(distancia), str(velocidad), str(x), str(y), str(esperado)]    #Formamos el patron de entrada a la Red Neuronal Artificial
            datasetEP.append(patron)                                                    #Lo añadimos al dataset de entrada a la Red Neuronal Artificial
            
            #Mostramos resultado del patrón generado
            #messagebox.showinfo("LANZAMIENTO REALIZADO", "¡Se lanzó a la ESQUINA INFERIOR IZQUIERDA de la portería!!\n\n Patrón añadido al dataset de entrada de la Red Neuronal:\n["+patron[0]+" "+patron[1]+" "+patron[2]+" "+patron[3]+" "+patron[4]+"]")
            lblVEP_1.config(text="¡Se lanzó a la ESQUINA INFERIOR\n IZQUIERDA de la portería!")
            lblVEP_2.config(text=str(patron))

        #Lanzamiento al INF_CNTR
        if lugar==8:
            distancia = round(random.uniform(6.90,10.50),2)                             #Generamos para la distancia un numero aleatorio decimal (funcion random.uniform()) entre 6.90m y 10.50m y redondeamos a 2 decimales mediante la funcion round()
            velocidad = round(random.uniform(85,110),2)                                 #Generamos para la velocidad un numero aleatorio decimal (funcion random.uniform()) entre 85km/h y 110km/h y redondeamos a 2 decimales mediante la funcion round()
            x = round(random.uniform(1.05,2.11),2)                                      #Generamos para la coordenada x un numero aleatorio decimal (funcion random.uniform()) entre 1.05m y 2.11m - Para lanzamiento al INF_CNTR
            y = round(random.uniform(0.00,0.70),2)                                      #Generamos para la coordenada y un numero aleatorio decimal (funcion random.uniform()) entre 0.00m y 0.70m - Para lanzamiento al INF_CNTR
            esperado = random.choice((0,1))                                             #Realizamos para el resultado esperado una eleccion aleatoria (funcion random.choice()) entre 0 y 1
            patron = [str(distancia), str(velocidad), str(x), str(y), str(esperado)]    #Formamos el patron de entrada a la Red Neuronal Artificial
            datasetEP.append(patron)                                                    #Lo añadimos al dataset de entrada a la Red Neuronal Artificial
        
            #Mostramos resultado del patrón generado
            #messagebox.showinfo("LANZAMIENTO REALIZADO", "¡Se lanzó al CENTRO INFERIOR de la portería!!\n\n Patrón añadido al dataset de entrada de la Red Neuronal:\n["+patron[0]+" "+patron[1]+" "+patron[2]+" "+patron[3]+" "+patron[4]+"]")
            lblVEP_1.config(text="¡Se lanzó al CENTRO\n INFERIOR de la portería!")
            lblVEP_2.config(text=str(patron))

        #Lanzamiento a la esquina INF_DCHA
        if lugar==9:
            distancia = round(random.uniform(6.90,10.50),2)                             #Generamos para la distancia un numero aleatorio decimal (funcion random.uniform()) entre 6.90m y 10.50m y redondeamos a 2 decimales mediante la funcion round()
            velocidad = round(random.uniform(85,110),2)                                 #Generamos para la velocidad un numero aleatorio decimal (funcion random.uniform()) entre 85km/h y 110km/h y redondeamos a 2 decimales mediante la funcion round()
            x = round(random.uniform(2.11,3.16),2)                                      #Generamos para la coordenada x un numero aleatorio decimal (funcion random.uniform()) entre 2.11m y 3.16m - Para lanzamiento a la esquina INF_DCHA
            y = round(random.uniform(0.00,0.70),2)                                      #Generamos para la coordenada y un numero aleatorio decimal (funcion random.uniform()) entre 0.00m y 0.70m - Para lanzamiento a la esquina INF_DCHA
            esperado = random.choice((0,1))                                             #Realizamos para el resultado esperado una eleccion aleatoria (funcion random.choice()) entre 0 y 1
            patron = [str(distancia), str(velocidad), str(x), str(y), str(esperado)]    #Formamos el patron de entrada a la Red Neuronal Artificial
            datasetEP.append(patron)                                                    #Lo añadimos al dataset de entrada a la Red Neuronal Artificial
            
            #Mostramos resultado del patrón generado
            #messagebox.showinfo("LANZAMIENTO REALIZADO", "¡Se lanzó a la ESQUINA INFERIOR DERECHA de la portería!!\n\n Patrón añadido al dataset de entrada de la Red Neuronal:\n["+patron[0]+" "+patron[1]+" "+patron[2]+" "+patron[3]+" "+patron[4]+"]")
            lblVEP_1.config(text="¡Se lanzó a la ESQUINA INFERIOR\n DERECHA de la portería!")
            lblVEP_2.config(text=str(patron))

    def continuar():
        if len(datasetEP)<2:
            messagebox.showerror("ERROR: FALTAN LANZAMIENTOS", "Debe realizar al menos 2 lanzamientos.")            
        else:
            ventanaDATASET(datasetEP)
        
    '''VENTANA_EPERSONALIZADO: BOTONES'''
    Button(VENTANA_EPERSONALIZADO, text="SUP_IZD", command=lambda:add_tiro(1), width=14, font=('Helvetica', 12, 'bold')).grid(row=1, column=0, sticky=NSEW, padx=30, pady=70)
    Button(VENTANA_EPERSONALIZADO, text="SUP_CNTR", command=lambda:add_tiro(2), width=14, font=('Helvetica', 12, 'bold')).grid(row=1, column=1, sticky=NSEW, padx=30, pady=70)
    Button(VENTANA_EPERSONALIZADO, text="SUP_DCHA", command=lambda:add_tiro(3), width=14, font=('Helvetica', 12, 'bold')).grid(row=1, column=2, sticky=NSEW, padx=30, pady=70)
    
    Button(VENTANA_EPERSONALIZADO, text="IZQUIERDA", command=lambda:add_tiro(4), width=14, font=('Helvetica', 12, 'bold')).grid(row=2, column=0, sticky=NSEW, padx=30, pady=70)
    Button(VENTANA_EPERSONALIZADO, text="CENTRO", command=lambda:add_tiro(5), width=14, font=('Helvetica', 12, 'bold')).grid(row=2, column=1, sticky=NSEW, padx=30, pady=70)
    Button(VENTANA_EPERSONALIZADO, text="DERECHA", command=lambda:add_tiro(6), width=14, font=('Helvetica', 12, 'bold')).grid(row=2, column=2, sticky=NSEW, padx=30, pady=70) 
     
    Button(VENTANA_EPERSONALIZADO, text="INF_IZD", command=lambda:add_tiro(7), width=14, font=('Helvetica', 12, 'bold')).grid(row=3, column=0, sticky=NSEW, padx=30, pady=70)
    Button(VENTANA_EPERSONALIZADO, text="INF_CNTR", command=lambda:add_tiro(8), width=14, font=('Helvetica', 12, 'bold')).grid(row=3, column=1, sticky=NSEW, padx=30, pady=70)
    Button(VENTANA_EPERSONALIZADO, text="INF_DCHA", command=lambda:add_tiro(9), width=14, font=('Helvetica', 12, 'bold')).grid(row=3, column=2, sticky=NSEW, padx=30, pady=70)

    lblVEP_1.grid(row=4, column=0, sticky=NSEW)
    lblVEP_2.grid(row=4, column=1, sticky=NSEW)

    Button(VENTANA_EPERSONALIZADO, text="Continuar", command=continuar, width=14, font=15).grid(row=4, column=2, sticky=NSEW, padx=40)

    VENTANA_EPERSONALIZADO.mainloop()

# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- #

def ventanaENTRENAMIENTOS():
    
    VENTANA_ENTRENAMIENTOS=Toplevel()                            #Generamos ventana SECUNDARIA
    
    '''VENTANA_ENTRENAMIENTOS: CARACTERISTICAS'''
    #VENTANA_ENTRENAMIENTOS.geometry("900x800+300+0")            #Tamaño ventana
    VENTANA_ENTRENAMIENTOS.iconbitmap("goalkeeper.ico")          #Icono ventana
    VENTANA_ENTRENAMIENTOS.resizable(0,0)                        #Tamaño ventana FIJO
    VENTANA_ENTRENAMIENTOS.title("2. TIPO DE ENTRENAMIENTO")     #Titulo ventana
    
    '''VENTANA_ENTRENAMIENTOS: LABELS'''
    Label(VENTANA_ENTRENAMIENTOS, text="\nSELECCIONE EL TIPO DE ENTRENAMIENTO A REALIZAR\n", font=('Helvetica', 15, 'bold')).grid(row=0, column=0, sticky=E, pady=15)
    Label(VENTANA_ENTRENAMIENTOS, text=" *Los lanzamientos se realizan siempre desde una posición frontal a la portería.", font=('Helvetica', 10), anchor=W).grid(row=1, column=0, sticky=W)

    '''Entrenamiento GENERAL'''
    Label(VENTANA_ENTRENAMIENTOS, text=" · Entrenamiento GENERAL", font=('Helvetica', 12, 'bold'), anchor=W).grid(row=2, column=0, sticky=W)
    Label(VENTANA_ENTRENAMIENTOS, text=" Entrenamiento diseñado para conocer los puntos débiles y fuertes del jugador. Está compuesto de 84 lanzamientos que abarcan toda la\n superficie de la portería inluyendo los palos para garantizar un entrenamiento completo.\n - Distancia media: 7 (metros)    - Velocidad media: 90 (km/h)", font=('Helvetica', 10), anchor=W, justify=LEFT).grid(row=3, column=0, sticky=W, pady=10)

    '''Entrenamiento EXTERNO'''
    Label(VENTANA_ENTRENAMIENTOS, text=" · Entrenamiento EXTERNO", font=('Helvetica', 12, 'bold'), anchor=W).grid(row=4, column=0, sticky=W)
    Label(VENTANA_ENTRENAMIENTOS, text=" Este entrenamiento usa como patrones de entrada los contenidos en el fichero dataset_externo.csv incluido en la carpeta del programa.\n Modificando este fichero permitimos al usuario escoger personalmente los patrones de entrada a la Red Neuronal Artificial parámetro\n a parámetro. Se recomiendan los siguientes intervalos para establecer los valores de cada parámetro del patrón:\n - Coordenada x: valor entre 0-3.16 (metros)    - Coordenada y: valor entre 0-2.08 (metros)\n - Distancia: valor entre 7-10 (metros)             - Velocidad: valor entre 85-110 (km/h)\n *En caso de introducir valores fuera de estos intervalos se pueden obtener resultados incorrectos e irreales.", font=('Helvetica', 10), anchor=W, justify=LEFT).grid(row=5, column=0, sticky=W, pady=10)

    '''Entrenamiento PERSONALIZADO'''
    Label(VENTANA_ENTRENAMIENTOS, text=" · Entrenamiento PERSONALIZADO", font=('Helvetica', 12, 'bold'), anchor=W).grid(row=7, column=0, sticky=W)
    Label(VENTANA_ENTRENAMIENTOS, text=" Este tipo de entrenamiento permite al usuario escoger las zonas de la portería donde desee realizar los sucesivos lanzamientos.\n De esta forma generamos una base de datos de patrones con la ubicación del lanzamiento escogida por el usuario con el\n objetivo de realizar un entrenamiento por zona adecuado a los objetivos de cada entrenador.\n - Distancia media: valor aleatorio entre 6.90-10.50 (metros)    - Velocidad media: valor aleatorio entre 85-110 (km/h)", font=('Helvetica', 10), anchor=W, justify=LEFT).grid(row=8, column=0, sticky=W, pady=10)

    #Si pulsamos el boton 'General'
    def general():
        messagebox.showinfo("ENTRENAMIENTO", "Ha seleccionado entrenamiento GENERAL")
        datasetVE='dataset_general.csv'
        ventanaDATASET(datasetVE)
        
    #Si pulsamos el boton 'Ejemplo'
    def externo():
        messagebox.showinfo("ENTRENAMIENTO", "Ha seleccionado entrenamiento EXTERNO")
        datasetVE='dataset_externo.csv'
        ventanaDATASET(datasetVE)
    
    #Si pulsamos el boton 'Personalizado'
    def personalizado():
        messagebox.showinfo("ENTRENAMIENTO", "Ha seleccionado entrenamiento PERSONALIZADO")
        ventanaEPERSONALIZADO()
      
    '''VENTANA_ENTRENAMIENTOS: BOTONES'''
    Button(VENTANA_ENTRENAMIENTOS, text="General", command=general, width=14, font=15).grid(row=2, column=1, sticky=NSEW, padx=20, pady=5)
    '''VENTANA_ENTRENAMIENTOS: BOTONES'''
    Button(VENTANA_ENTRENAMIENTOS, text="Externo", command=externo, width=14, font=15).grid(row=4, column=1, sticky=NSEW, padx=20, pady=5)
    '''VENTANA_ENTRENAMIENTOS: BOTONES'''
    Button(VENTANA_ENTRENAMIENTOS, text="Personalizado", command=personalizado, width=14, font=15).grid(row=7, column=1, sticky=NSEW, padx=20, pady=5)

    VENTANA_ENTRENAMIENTOS.mainloop() 
   
# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- #

def ventanaINICIO():
    
    VENTANA_INICIO = Tk()                           #Generamos ventana PRINCIPAL
    
    '''VENTANA_INICIO: CARACTERISTICAS'''
    #VENTANA_INICIO.geometry("900x800+0+0")         #Tamaño ventana
    VENTANA_INICIO.iconbitmap("goalkeeper.ico")     #Icono ventana
    VENTANA_INICIO.resizable(1,1)                   #Tamaño ventana FIJO
    VENTANA_INICIO.title("1. INICIO")               #Titulo ventana

    '''VENTANA_INICIO: LABELS TEXTO INICIAL'''
    Label(VENTANA_INICIO, text=" \nPROYECTO FIN DE GRADO\n", font=('Helvetica', 15, 'bold')).pack(fill=BOTH, expand=True)
    
    Label(VENTANA_INICIO, text=" ~ Autor: Íñigo Rodríguez Sánchez", font=('Helvetica', 13, 'bold'), anchor=W).pack(fill=BOTH)
    Label(VENTANA_INICIO, text=" ~ Escuela Técnica Superior de Ingeniería y Sistemas de Telecomunicación (ETSIST)", font=('Helvetica', 12, 'bold'), anchor=W).pack(fill=BOTH)
    Label(VENTANA_INICIO, text=" ~ Universidad Politécnica de Madrid, España 2019\n", font=('Helvetica', 12, 'bold'), anchor=W).pack(fill=BOTH)
    
    Label(VENTANA_INICIO, text=" # Este programa simula el aprendizaje de un sistema diseñado para el entrenamiento de porteros de balonmano.", font=('Helvetica', 10), anchor=W).pack(fill=BOTH)
    Label(VENTANA_INICIO, text=" # Para ello utiliza una Red Neuronal Artificial que aprende de las capacidades del portero a través de los lanzamientos realizados a portería.", font=('Helvetica', 10), anchor=W).pack(fill=BOTH)
    Label(VENTANA_INICIO, text=" # La arquitectura de la red es:", font=('Helvetica', 10), anchor=W).pack(fill=BOTH)
    
    '''VENTANA_INICIO: IMAGEN ARQUITECTURA RED'''
    imagenVI = PhotoImage(file="ann_structure.gif")
    Label(VENTANA_INICIO, image=imagenVI).pack(fill=BOTH, expand=True)
    
    '''VENTANA_INICIO: BOTONES'''
    Button(VENTANA_INICIO, text="¡Comenzar entrenamiento!", command=ventanaENTRENAMIENTOS, width=28, font=('Helvetica', 15, 'bold')).pack(padx=40, pady=20, expand=True)
    
    VENTANA_INICIO.mainloop()
    
# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- #

def run_program():
    ventanaINICIO()

# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- #
#PARA EJECUTAR EL PROGRAMA DESCOMENTAR LA SIGUIENTE LINEA
#run_program()

