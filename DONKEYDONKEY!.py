
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
import os
from bs4 import BeautifulSoup
from keras import models
import numpy as np
import cv2
import re
from fuzzywuzzy import fuzz
import easyocr
from PIL import Image, ImageTk



NPH="Inserta tu nombre completo"
NCPH= "Inserta tu numero de control"
GPH= "Selecciona tu grupo"

operacion= ["Proyectos","C. & R."]
grupos=["3AVP","4AMP","4AVP","5AMP","5AVP","6AMP","6AVP"]
proyectos= ["P001","P002","P003","P004","P005","P006","P007","P008","P009",
            "P010","P011","P012","P013","P014","P015","P016","P017","P018","P019",
            "P020","P021","P022","P023","P024","P025","P026","P027","P028","P029",
            "P030"]
NumeroDeDocumento= []

# Diccionario de correcciones de caracteres similares
correcciones_comunes = {
    "O": "0",
    "Q": "0",
    "o": "0",
    "l": "/",
    "W": "/",
    "I": "1",
    "i":"1",
    "Z": "2",
    "z":"2",
    "_":" ",
    "(":"c",
    "|":"/",
    "'":"/",
    "%":"/",
    "*":"1"
}

correcciones_comunesN = {
    "9": "4",
    "Q": "0",
    "o": "0",
    "l": "/",
    "I": "1",
    "i":"1",
    "Z": "2",
    "z":"2",
    "_":" ",
    "(":"c",
    "|":"/"
}

coincidencias=False

#Patrones posibles en el OCR
patrones= [ r'(\d{4,})+(.+?)\s+(\d{3})',          #1. Busca: "/" seguido de al menos tres números (1), lo que sea (2) hasta que encuentra tres números (3). 
            r'(\d{4,}\s*)+([A-Za-z])+(\d{3})',    #2. Busca: "/" seguido de al menos tres números (1), una letra (2) hasta que encuentra tres números (3).  
            r"(\d{4,}\s*)+(\S+)+("")",]           #3. Busca: "/" seguido de al menos tres números (1), caracteres hasta que encuentre un espacio (2).


patronNP=r"(\d{1,})+(/)+(\d{1,})"

#Ventana del menú principal
window = Tk()
window.title("DONKEY DONKEY!")
window.geometry("500x500")
window.config(bg="black", cursor="dotbox")
ico = Image.open('icon.png')
photo = ImageTk.PhotoImage(ico)
window.wm_iconphoto(False, photo)
x = IntVar()
y = IntVar()
w = StringVar()
g= StringVar()

combostyle = ttk.Style()

combostyle.theme_create('combostyle', parent='alt',
                         settings = {'TCombobox':
                                     {'configure':
                                      {'selectbackground': 'black',
                                       'fieldbackground': 'black',
                                       'background': 'gray'
                                       }}}
                         )

combostyle.theme_use('combostyle') 

def corregir_ocr(texto):
    for caracter_erroneo, caracter_correcto in correcciones_comunes.items():
        texto = texto.replace(caracter_erroneo, caracter_correcto)
        
        #Busca y borra espacios que proceden y anteceden a una diagonal ("/")
        if  re.search(r"/\s", texto) or re.search(r"\s/", texto):
            texto=texto.replace("/ ","/")
            texto=texto.replace(" /","/")    
            
    return texto

def limpia_clasifica(texto):
    corrections = {'onccpto': 'concepto', 'concpto': 'concepto', 'onccpt': 'concepto'}
    for incorrect, correct in corrections.items():
        texto = re.sub(incorrect, correct, texto.lower())

    work_type = tipo_de_trabajo(texto)

    return work_type

def tipo_de_trabajo(texto):
    concept_match = fuzz.partial_ratio(texto, "concepto")
    resumen_match = fuzz.partial_ratio(texto, "resumen")
    
    if concept_match > resumen_match:
        return "C"
    else:
        return "R"
    
def corregir_NP(texto):
    coincidenciasNP= re.search(patronNP, texto)
    if coincidenciasNP:
        NPi=coincidenciasNP.group(1)
        NPf=coincidenciasNP.group(3)
        if NPi>NPf:
           for caracter_erroneo, caracter_correcto in correcciones_comunesN.items():
             texto = texto.replace(caracter_erroneo, caracter_correcto)  

def process_image(image_path, output_path):
    # Leer la imagen
    img = cv2.imread(image_path)
    denoised_img = cv2.bilateralFilter(img, d=2, sigmaColor=75, sigmaSpace=75)
    gray_img = cv2.cvtColor(denoised_img, cv2.COLOR_BGR2GRAY)
    _, bw_img = cv2.threshold(gray_img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    cv2.imwrite(output_path, gray_img)
    print(f"Procesando '"+image_path+"'...")
    return gray_img

def extract_text(image):
    reader = easyocr.Reader(['es'])  # Cargar el lector para español
    results = reader.readtext(image)
    extracted_text = " ".join([res[1] for res in results])
    return extracted_text

def buscaPatron(text):
 c=0
 
 for p in patrones:
    c+=1
    
    if re.search(p,text): 
       # print("El patrón #"+str(c)+" encontró: '"+re.search(p,text).group(0)+"' ['"+p+"']") 
        coincidencias=re.search(p,text)
        return coincidencias
        break

def on_entry_click(event):
   if txtN.get() == NPH:
      txtN.delete(0, END)
      txtN.configure(foreground="white")

def on_focus_out(event):

   if txtN.get() == "":
      txtN.insert(0, NPH)
      txtN.configure(foreground="gray")
      
def on_entry_click2(event):
   
   if txtNC.get() == NCPH:
      txtNC.delete(0, END)
      txtNC.configure(foreground="white",validate="key",validatecommand=(validate_cmd, "%P"))

def on_focus_out2(event):
   
   if txtNC.get() == "":
      
      txtNC.configure(foreground="gray",validate="key",validatecommand=(validate_cmd2, "%P"))
      txtNC.insert(0, NCPH) 
     
      
      
def limit_characters_input(P):
    # Limitar el número de caracteres a 14
    if len(P) > 14:
        return False
    return True

def limit_characters_input2(P):
    # Limitar el número de caracteres a 14
    if len(P) > 100:
        return False
    return True
cont=1 


def carpetasP():
    if w.get() != "":
        print("Seleccionaste: " + w.get())
        N = txtN.get().title()
        Nc = txtNC.get()
        G = g.get()
        P = w.get()

        #Parámetros para Burro(red neuronal)
        width = 300
        height = 300
        ruta_train = "train"
        labels = os.listdir(ruta_train)
        model = models.load_model("burro.keras")

        folder = filedialog.askdirectory()
        contador_img_codigo = 0  
        contador_img_navegador = 0 
        contador_img_libreta = 0  
        NumeroDeDocumento = []
        archivos_css_pendientes = []
        archivos_img_codigo_pendientes = []
        archivos_img_navegador_pendientes = []
        archivos_img_libreta_pendientes = []
        
        hay_html = False
        cD=0 #Contador de documentos desconocidos
        
        for item in os.listdir(folder):
            
            if item.endswith(".html")==False and item.endswith(".jpg")==False and item.endswith(".png")==False and item.endswith(".PNG")==False and item.endswith(".JPG")==False and item.endswith(".css")==False and item.endswith(".ini")==False:
                file_path = os.path.join(folder, item)
                print(f"'{item}' no es un tipo de archivo habitual, se le asignará '00' como su enumeración. ")
                split_fl = os.path.splitext(item)
                file_ext = split_fl[1]
                nuevo_nombre_gral= f"{Nc} {P} 00 {N} {G}({str(cD)}){file_ext}"
                cD+=1
                
                os.rename(file_path, os.path.join(folder, nuevo_nombre_gral))
                
        #Comprueba si hay algun .html en la carpeta
        for item in os.listdir(folder):
            if item.endswith(".html"):
                hay_html = True
                break
            


        if hay_html:
          print("Proyecto con .html detectado") 

          for item in os.listdir(folder):
            file_path = os.path.join(folder, item)

            # Procesar archivos HTML
            if item.endswith(".html"):
                with open(file_path, 'r', encoding="utf-8") as file:
                    soup = BeautifulSoup(file, 'html.parser')
                    id2 = soup.find("div", class_="id")
                    id = id2.text.strip() if id2 else "00"
                                    
                if id=="00":
                  print("No se encontro la enumeración en '"+item+"', recuerda anidarlo en la clase id")
                  cD+=1  
                  nuevo_nombre_html = f"{Nc} {P} {id} {N} {G}({str(cD)}).html"                 
                  os.rename(file_path, os.path.join(folder, nuevo_nombre_html)) 
                    

                else:
                    NumeroDeDocumento.append(id)
                    nuevo_nombre_html = f"{Nc} {P} {id} {N} {G}.html"
                    os.rename(file_path, os.path.join(folder, nuevo_nombre_html))


          # Renombrar los archivos CSS
          for item in os.listdir(folder):
            if item.endswith(".css"):
                file_path = os.path.join(folder, item)
                if NumeroDeDocumento:
                    NumeroDeDocumento.sort(reverse=True) 
                    Nt_css = int(NumeroDeDocumento[0]) + 1
                    NumeroDeDocumento.append("0"+str(Nt_css))
                    nuevo_nombre_css = f"{Nc} {P} 0{Nt_css} {N} {G}.css"
                    os.rename(file_path, os.path.join(folder, nuevo_nombre_css))
                else:
                    archivos_css_pendientes.append(item)

         # Clasificar las imágenes primero en "código" o "navegador"
          for item in os.listdir(folder):
            if item.endswith((".png", ".PNG", ".jpg", ".JPG")):
                file_path = os.path.join(folder, item)
                imagen = cv2.imread(file_path)
                imagen_resized = cv2.resize(imagen, (width, height))
                result = model.predict(np.array([imagen_resized]))[0]
                porcentaje = max(result)*100
                grupo = labels[result.argmax()]

                if grupo == "vista de navegador":  # Vista de navegador
                    print("Burro cree que '"+item+"' es vista de navegador. "+"("+str(round(porcentaje))+"%)")
                    archivos_img_navegador_pendientes.append(item)
                elif grupo == "código":  # Imágenes de código
                    print("Burro cree que '"+item+"' es código. "+"("+str(round(porcentaje))+"%)")
                    archivos_img_codigo_pendientes.append(item)
                elif grupo == "libreta": #Imágenes de la libreta
                    print("Burro cree que '"+item+"' es libreta. "+"("+str(round(porcentaje))+"%)")
                    archivos_img_libreta_pendientes.append(item)    

          # Renombrar imágenes de tipo "código" primero
          for item in archivos_img_codigo_pendientes:
            file_path = os.path.join(folder, item)
            if NumeroDeDocumento:
                NumeroDeDocumento.sort(reverse=True) 
                contador_img_codigo += 1
                Nt_img = int(NumeroDeDocumento[0]) + contador_img_codigo
                nuevo_nombre_codigo = f"{Nc} {P} 0{Nt_img} {N} {G}.png"
                os.rename(file_path, os.path.join(folder, nuevo_nombre_codigo))

         # Renombrar imágenes de tipo "navegador" después
          for item in archivos_img_navegador_pendientes:
            file_path = os.path.join(folder, item)
            if NumeroDeDocumento:
                NumeroDeDocumento.sort(reverse=True) 
                contador_img_navegador += 1
                Nt_img = int(NumeroDeDocumento[0]) + contador_img_codigo + contador_img_navegador
                nuevo_nombre_navegador = f"{Nc} {P} 0{Nt_img} {N} {G}.png"
                os.rename(file_path, os.path.join(folder, nuevo_nombre_navegador))
                
                
          for item in archivos_img_libreta_pendientes:
            file_path = os.path.join(folder, item)
            if NumeroDeDocumento:
                NumeroDeDocumento.sort(reverse=True) 
                contador_img_libreta += 1
                Nt_img = int(NumeroDeDocumento[0]) + contador_img_codigo + contador_img_navegador + contador_img_libreta
                nuevo_nombre_libreta = f"{Nc} {P} 0{Nt_img} {N} {G}.jpg"
                os.rename(file_path, os.path.join(folder, nuevo_nombre_libreta))   
          print("Burro terminó de renombrar")     
                
        else:
            print("Proyecto sin .html detectado")
            # No hay archivos .html, procesamos solo imágenes en el orden correcto
            for item in os.listdir(folder):
                file_path = os.path.join(folder, item)
                if item.endswith((".png", ".PNG", ".jpg", ".JPG")):
                    imagen = cv2.imread(file_path)
                    imagen_resized = cv2.resize(imagen, (width, height))
                    result = model.predict(np.array([imagen_resized]))[0]
                    porcentaje = max(result) * 100
                    grupo = labels[result.argmax()]

                    if grupo == "vista de navegador":
                        archivos_img_navegador_pendientes.append(item)
                    elif grupo == "código":
                        archivos_img_codigo_pendientes.append(item)
                    elif grupo == "libreta":
                        archivos_img_libreta_pendientes.append(item)

            # Renombrar imágenes de código
            for item in archivos_img_codigo_pendientes:
                contador_img_codigo += 1
                nuevo_nombre_codigo = f"{Nc} {P} 0{contador_img_codigo} {N} {G}.png"
                os.rename(os.path.join(folder, item), os.path.join(folder, nuevo_nombre_codigo))

            # Renombrar imágenes de navegador
            for item in archivos_img_navegador_pendientes:
                contador_img_navegador += 1
                nuevo_nombre_navegador = f"{Nc} {P} 0{contador_img_codigo + contador_img_navegador} {N} {G}.png"
                os.rename(os.path.join(folder, item), os.path.join(folder, nuevo_nombre_navegador))

            # Renombrar imágenes de libreta
            for item in archivos_img_libreta_pendientes:
                contador_img_libreta += 1
                nuevo_nombre_libreta = f"{Nc} {P} 0{contador_img_codigo + contador_img_navegador + contador_img_libreta} {N} {G}.jpg"
                os.rename(os.path.join(folder, item), os.path.join(folder, nuevo_nombre_libreta))

            print("Burro terminó de renombrar.")

def carpetasCR():
    N = txtN.get().title()
    Nc = txtNC.get()
    G = g.get()
    cT=0
    cP=0
    
    folder = filedialog.askdirectory()
    for item in os.listdir(folder):
        image_path = os.path.join(folder, item)
        process_image(image_path, 'imagen_procesada.jpg')
        texto_ocr = extract_text('imagen_procesada.jpg')
        
        texto_corregido = corregir_ocr(texto_ocr)
        coincidenciasNP= re.search(patronNP, texto_corregido)
        coincidencias=buscaPatron(texto_corregido)

        if coincidencias:
         TT=limpia_clasifica(coincidencias.group(2)) 
         NT=coincidencias.group(3)
         
         if coincidencias.group(3)=="":
           print("No se encontró el número de trabajo, se remplazara con 'xx'")  
           NT="xx"+"("+str(cT)+")"
           cT+=1
      
        if coincidenciasNP:
         if int(coincidenciasNP.group(1))>9:
          NP=coincidenciasNP.group(1)  
         else: NP="0"+coincidenciasNP.group(1)   
             
        else:
         print("No se encontró el número de página, se remplazara con 'xx'")
         NP="xx"+"("+str(cP)+")" 
         cP+=1   
         
        nuevo_nombre= Nc+" "+TT+NT+" "+NP+" "+N+" "+G+".jpg"
        print("Renombrando '"+image_path+"' a '"+nuevo_nombre+"'... \n")
        os.rename(image_path, os.path.join(folder, nuevo_nombre))      
   
      
validate_cmd = window.register(limit_characters_input)
validate_cmd2 = window.register(limit_characters_input2)

#Boton
def submit():
    Nc=txtNC.get()
    if txtN.get() and txtNC.get() and g.get() != "" and txtN.get() and txtNC.get() != NCPH and Nc.isnumeric()==True and g.get() != "Selecciona tu grupo" and len(Nc)==14:
       
        N= txtN.get().title()
        G= g.get()
        
   
        print("Hola, "+N+" del "+G+", tu numero de control es "+Nc)
        
        if x.get()==0:
         print("Seleccionaste: Proyectos")
         wP= Toplevel()
         center_screen(wP)
         
         
         wP.title("DONKEY DONKEY!: Proyectos")
         wP.geometry("500x500")
         wP.config(bg="black", cursor="dotbox")
         wP.config(bg="black", cursor="dotbox")
         ico = Image.open('icon.png')
         photo = ImageTk.PhotoImage(ico)
         wP.wm_iconphoto(False, photo)
         frame=Frame(wP,bg="black")
         
         frame.pack(anchor=CENTER)
         
         frame2=Frame(wP,bg="black")
         Label(frame2,text="¿Qué proyecto vas a documentar?",fg="white",bg="black").pack()        
         frame2.pack(before=frame,pady=15)
         
         
         btnCarpeta=Button(wP, text="Seleccionar Carpeta",command=carpetasP, bg="black", fg="white", cursor="target")



         btnCarpeta.pack(after=frame, pady=10)
         
         c=0
         p=0
         z=0
         l=0
         k=0
         h=0
         
         for index in range(len(proyectos)):
            
            
             rbProyectos=Radiobutton(frame,text=proyectos[index],variable=w,value=proyectos[index],bg="black", fg="gray",indicatoron=0,width=7)
             c+=1
             
             rbProyectos.grid(row=c-index, column=c)
             if c>=6:
                p+=1
                rbProyectos.grid(row=c-index+1, column=p,padx=5,pady=5)
                
             if c>=11:
                 z+=1
                 rbProyectos.grid(row=c-index+2, column=z)  
                 
             if c>=16:
                 l+=1
                 rbProyectos.grid(row=c-index+3, column=l) 
                         
             if c>=21:
                 k+=1
                 rbProyectos.grid(row=c-index+4, column=k)
                 
             if c>=26:
                 h+=1
                 rbProyectos.grid(row=c-index+5, column=h)  
    
        elif x.get()==1:
          print("Seleccionaste: Conceptos y Resumenes") 
          carpetasCR()
          
     
    elif txtN.get()=="" or txtNC.get()=="" or g.get() == "" or txtN.get()==NPH or txtNC.get() == NCPH or g.get() == GPH :  
       print("Llena todos los campos antes de empezar, we")  
       
    elif Nc.isnumeric()==False and Nc!=NCPH and Nc!="" or len(Nc)!=14:
       print("El número de control se compone de 14 números, checa bien, burro")          
        


#Encabezado
title = Label(master=window, text="DONKEY DONKEY!", font=("Small Fonts", 30), fg="white", bg="black")
title.pack(padx=30)

#Entrada del No. de Control y del Nombre
txtN = Entry(master=window, bg="black", fg="gray", justify=LEFT, width=26, cursor="target" )
txtN.insert(0,NPH)
txtN.bind("<FocusIn>", on_entry_click)
txtN.bind("<FocusOut>", on_focus_out)

txtNC  = Entry(master=window, bg="black", fg="gray", justify=LEFT, width=26, cursor="target")
txtNC.configure(foreground="gray",validate=None,validatecommand=None)
txtNC.insert(0,NCPH)
txtNC.bind("<FocusIn>", on_entry_click2)
txtNC.bind("<FocusOut>", on_focus_out2)




txtN.pack(pady = 10, padx=0)
txtNC.pack(pady=10, padx=0)




for index in range(len(operacion)):
   rbOperacion=Radiobutton(window,text=operacion[index],variable=x,value=index,bg="black", fg="gray",indicatoron=0,width=9,cursor="man")
   
   
   rbOperacion.pack()
   
ldGrupos= ttk.Combobox(window,values=grupos,state="readonly",textvariable=g,background="black",foreground="white",cursor="target")
ldGrupos.config(foreground="gray")
ldGrupos.set("Selecciona tu grupo")
ldGrupos.pack(after=txtNC, pady=10)

btnAceptar=Button(window, text="Aceptar",command=submit, bg="black", fg="white", cursor="target")

Label(window,text="¿Qué vas a documentar?",bg="black",fg="white",cursor="target").pack(after=ldGrupos,pady=5)

btnAceptar.pack(pady=10)

def center_screen(window):
    """ gets the coordinates of the center of the screen """
    global screen_height, screen_width, x_cordinate, y_cordinate
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
        # Coordinates of the upper left corner of the window to make the window appear in the center
    x_cordinate = int((screen_width/2) - (500/2))
    y_cordinate = int((screen_height/2) - (500/2))
    window.geometry("{}x{}+{}+{}".format(500, 500, x_cordinate, y_cordinate))


center_screen(window)


window.mainloop()