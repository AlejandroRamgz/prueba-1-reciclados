from flask import Flask, request, render_template
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from email.mime.base import MIMEBase
from email.encoders import encode_base64

#ESTO ES DE CREATOR
from fpdf import FPDF
from datetime import datetime
from referencias import *

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/crear_informe', methods=['GET', 'POST'])
def crear_informe():
    if request.method == 'POST':
        # Obtener los datos del formulario
        nombre_equipo = request.form['nombre_equipo']
        horometro = request.form['horometro']
        tipo_mantenimiento = request.form['tipo_mantenimiento']
        sede = request.form['sede']
        descripcion_falla = request.form['descripcion_falla']
        conclusiones = request.form['conclusiones']
        num_personas = int(request.form['num_personas'])

        # Obtener los datos de cada persona
        personas = []
        q = 1
        for i in range(num_personas):
            personanumero = q
            nombre = request.form[f'nombre_persona_{i}']
            cargo = request.form[f'cargo_persona_{i}']
            tareaarealizar = request.form[f'tarea_a_realizar_{i}']
            personas.append((personanumero, nombre, cargo, tareaarealizar))
            q += 1

        # Obtener las imágenes desde la página web
        imagenes = []
        for i in range(4):
            imagen = request.files.get(f'imagen_{i}')
            if imagen:
                # Obtén la ruta de archivo donde se guardará la imagen
                ruta_imagen = f"static/imagenes/imagen_{i}.jpg" # TENER EN CUENTA SI ES JPG O PNG
                imagen.save(ruta_imagen)
                imagenes.append(ruta_imagen)

        pdf = FPDF(orientation='P', unit='mm', format='A4')
        pdf.add_page()
        url = 'https://recicladosindustriales.co/'

        pdf.image('images.png', x= 13, y= 12, w = 40, h = 0, link = url)
        
        pdf.set_font('Times','B',18)
        bcol_set(pdf, "grisintermedio")   
        #CUADRO PARA ENCABEZADO IMAGEN Y texto
        pdf.cell( w=45, h=16, border = 1, align = 'C', fill = 0)
        pdf.multi_cell( w=0, h=16, txt = 'Reciclados Industriales De Colombia', border = 1, align = 'C', fill = 1)
        #ESPACION ENTRE TABLAS
        pdf.ln(3)
        pdf.set_font('Times','B',14)
        pdf.multi_cell( w=0, h=10, txt = 'Informe de Mantenimiento', border = 1, align = 'C', fill = 1)
        bcol_set(pdf, "grisclaro") 
        pdf.set_font('Times','B',10)
        pdf.cell( w=20, h=4, txt = 'Fecha: ', border = 1, align = 'L', fill = 1)
        pdf.set_font('Times','',10)
        pdf.cell( w=36, h=4, txt = datetime.today().strftime("%d %b, %Y"), border = 1, align = 'C', fill = 0)
        pdf.set_font('Times','B',10)
        pdf.cell( w=20, h=4, txt = 'Hora: ', border = 1, align = 'L', fill = 1)
        pdf.set_font('Times','',10)
        pdf.cell( w=36, h=4, txt = datetime.now().strftime("%I:%M %p"), border = 1, align = 'C', fill = 0)
        pdf.set_font('Times','B',10)
        pdf.cell( w=20, h=4, txt = "Sede: ", border = 1, align = 'L', fill = 1)
        pdf.set_font('Times','',10)
        pdf.multi_cell( w=58, h=4, txt = sede, border = 1, align = 'C', fill = 0)                                 #ACA TOCA CON LOS DATOS DE LA PAGINA LA SEDE
        #ESPACION ENTRE TABLAS
        pdf.ln(2)
        bcol_set(pdf, "grisintermedio")  
        pdf.set_font('Times','B',12)
        pdf.multi_cell( w=0, h=5, txt = 'Personal encargado de realizar mantenimiento', border = 1, align = 'C', fill = 1)

        #for i, (nombre, cargo) in enumerate(zip(nombres_personas, cargos_personas), start=1):                 3333333333333333333333333333333333333
        #    pdf.drawString(50, 610 - i*20, f'Persona {i}: {nombre}, Cargo: {cargo}')

        #COLUMNAS PARA PERSONAL ENCARGADO
        bcol_set(pdf, "grisclaro") 
        pdf.set_font('Times','B',10)
        # encabezado
        pdf.cell(w = 14, h = 5, txt = 'Número', border = 1, align = 'C', fill = 1)
        pdf.cell(w = 40, h = 5, txt = 'Nombre', border = 1, align = 'C', fill = 1)
        pdf.cell(w = 55, h = 5, txt = 'Cargo', border = 1, align = 'C', fill = 1)
        pdf.multi_cell(w = 0, h = 5, txt = 'Tarea a realizar', border = 1, align = 'C', fill = 1)


        pdf.set_font('Times','',10)

        for personanumero, nombre, cargo, tareaarealizar in personas:
            pdf.cell(w = 14, h = 5, txt = str(personanumero), border = 1, align = 'C', fill = 0)
            pdf.cell(w = 40, h = 5, txt = str(nombre), border = 1, align = 'C', fill = 0)
            pdf.cell(w = 55, h = 5, txt = str(cargo), border = 1, align = 'C', fill = 0)
            pdf.multi_cell(w = 0, h = 5, txt = str(tareaarealizar), border = 1, align = 'L', fill = 0)
        

        pdf.ln(2)
        bcol_set(pdf, "grisintermedio") 
        pdf.set_font('Times','B',12)
        pdf.multi_cell( w=0, h=5, txt = 'Nombre del equipo', border = 1, align = 'C', fill = 1)
        bcol_set(pdf, "grisclaro") 
        pdf.set_font('Times','',10)
        pdf.cell( w=0, h=4, txt = nombre_equipo, border = 1, align = 'C', fill = 1)
        pdf.ln(6)
        bcol_set(pdf, "grisintermedio") 
        pdf.set_font('Times','B',12)
        pdf.multi_cell( w=0, h=5, txt = 'Datos de tarea a realizar', border = 1, align = 'C', fill = 1)
        bcol_set(pdf, "grisclaro") 
        pdf.set_font('Times','B',10)
        pdf.cell( w=45, h=4, txt = 'Tipo de Mantenimiento:', border = 1, align = 'L', fill = 1)
        pdf.set_font('Times','',10)
        pdf.cell( w=50, h=4, txt = tipo_mantenimiento, border = 1, align = 'C', fill = 0)
        pdf.set_font('Times','B',10)
        pdf.cell( w=45, h=4, txt = 'Horómetro: ', border = 1, align = 'L', fill = 1)
        pdf.set_font('Times','',10)
        pdf.multi_cell( w=50, h=4, txt = horometro, border = 1, align = 'C', fill = 0)
        pdf.set_font('Times','B',10)
        pdf.multi_cell( w=0, h=4, txt = "Actividad a realizar: ", border = 1, align = 'C', fill = 1)
        pdf.set_font('Times','',10)
        pdf.multi_cell( w=0, h=4, txt = "", border = 1, align = 'L', fill = 0)                              
        pdf.ln(2)
        bcol_set(pdf, "grisintermedio") 
        pdf.set_font('Times','B',12)
        pdf.multi_cell( w=0, h=5, txt = 'Fotos iniciales del equipo', border = 1, align = 'C', fill = 1)
        pdf.set_font('Times','',10)

        pdf.multi_cell( w=0, h=80, txt = "", border = 1, align = 'C', fill = 0)

        x=12
        for imagen in imagenes:
            
            pdf.image(imagen, x=x, y=130, w=40, h=0)
            x+=45

        pdf.ln(2)
        bcol_set(pdf, "grisintermedio") 
        pdf.set_font('Times','B',12)
        pdf.multi_cell( w=0, h=5, txt = 'Descripción de las fallas', border = 1, align = 'C', fill = 1)
        bcol_set(pdf, "grismasclaro") 
        pdf.set_font('Times','',10)
        fallas ="El tamaño A4, como los demás formatos de la serie A, está regulado por la norma ISO 216. Se trata del formato de papel más utilizado en Europa y Japón. Las dimensiones del tamaño A4 se expresan en centímetros en la mayoría de países europeos y en pulgadas («inches») en los países anglófonos. "
        pdf.multi_cell( w=0, h=4, txt = descripcion_falla, border = 1, align = 'L', fill = 1)
        pdf.ln(2)
        bcol_set(pdf, "grisintermedio") 
        pdf.set_font('Times','B',12)
        pdf.multi_cell( w=0, h=5, txt = 'Mantenimiento realizado (descripción actividades)', border = 1, align = 'C', fill = 1)
        bcol_set(pdf, "grismasclaro") 
        pdf.set_font('Times','',10)
        pdf.multi_cell( w=0, h=4, txt = fallas, border = 1, align = 'L', fill = 1)
        pdf.ln(2)
        bcol_set(pdf, "grisintermedio") 
        pdf.set_font('Times','B',12)
        pdf.multi_cell( w=0, h=5, txt = 'Observaciones y/o recomendaciones', border = 1, align = 'C', fill = 1)
        bcol_set(pdf, "grismasclaro") 
        pdf.set_font('Times','',10)
        pdf.multi_cell( w=0, h=4, txt = conclusiones, border = 1, align = 'L', fill = 1)
        pdf.ln(2)
                        #OTRA HOJAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
        pdf.add_page()

        bcol_set(pdf, "grisintermedio") 
        pdf.set_font('Times','B',12)
        pdf.multi_cell( w=0, h=5, txt = 'Fotos finales del equipo', border = 1, align = 'C', fill = 1)
        pdf.set_font('Times','',10)
        pdf.multi_cell( w=0, h=80, txt = "", border = 1, align = 'C', fill = 0)
        pdf.ln(2)
        bcol_set(pdf, "grisintermedio") 
        pdf.set_font('Times','B',12)
        pdf.multi_cell( w=0, h=5, txt = 'Repuestos instalados', border = 1, align = 'C', fill = 1)     #TOCA PREGUNTAR EL NUMERO DE REPUESTOS (IGUAL A LO QUE SE HACE CON EL NUMERO DE PERSONAS)
        bcol_set(pdf, "grisclaro") 
        pdf.set_font('Times','B',10)
        pdf.cell( w=26, h=4, txt = 'Numero parte:', border = 1, align = 'L', fill = 1)
        pdf.set_font('Times','',10)
        pdf.cell( w=24, h=4, txt = "", border = 1, align = 'C', fill = 0)
        pdf.set_font('Times','B',10)
        pdf.cell( w=24, h=4, txt = 'Descripción: ', border = 1, align = 'L', fill = 1)
        pdf.set_font('Times','',10)
        pdf.cell( w=72, h=4, txt = "", border = 1, align = 'C', fill = 0)
        pdf.set_font('Times','B',10)
        pdf.cell( w=20, h=4, txt = "Cantidad: ", border = 1, align = 'L', fill = 1)           #TENER CUIDADO PORQUE EL DATO DE AHI ES NUMERO
        pdf.set_font('Times','',10)
        pdf.multi_cell( w=24, h=4, txt = "", border = 1, align = 'C', fill = 0)                           
        pdf.ln(2)
        bcol_set(pdf, "grisintermedio") 
        pdf.set_font('Times','B',12)
        pdf.multi_cell( w=0, h=5, txt = 'Repuestos sugeridos para próxima interveción', border = 1, align = 'C', fill = 1)     #TOCA PREGUNTAR EL NUMERO DE REPUESTOS (IGUAL A LO QUE SE HACE CON EL NUMERO DE PERSONAS)
        bcol_set(pdf, "grisclaro") 
        pdf.set_font('Times','B',10)
        pdf.cell( w=26, h=4, txt = 'Numero parte:', border = 1, align = 'L', fill = 1)
        pdf.set_font('Times','',10)
        pdf.cell( w=24, h=4, txt = "", border = 1, align = 'C', fill = 0)
        pdf.set_font('Times','B',10)
        pdf.cell( w=24, h=4, txt = 'Descripción: ', border = 1, align = 'L', fill = 1)
        pdf.set_font('Times','',10)
        pdf.cell( w=72, h=4, txt = "", border = 1, align = 'C', fill = 0)
        pdf.set_font('Times','B',10)
        pdf.cell( w=20, h=4, txt = "Cantidad: ", border = 1, align = 'L', fill = 1)           #TENER CUIDADO PORQUE EL DATO DE AHI ES NUMERO
        pdf.set_font('Times','',10)
        pdf.multi_cell( w=24, h=4, txt = "", border = 1, align = 'C', fill = 0) 
        pdf.ln(2)
        pdf.output('hoja.pdf')

        # Configurar los detalles del correo electrónico
        de = "jaramirez9562@misena.edu.co"
        para = "jaramirez9562@misena.edu.co"
        asunto = "Adjuntando PDF desde FPDF"
        mensaje = "¡Hola! Adjunto el archivo PDF que creé con FPDF."

        # Crear el objeto MIMEMultipart y establecer los campos del correo electrónico
        msg = MIMEMultipart()
        msg["From"] = de
        msg["To"] = para
        msg["Subject"] = asunto

        # Adjuntar el archivo PDF al correo electrónico
        archivo_adjunto = "hoja.pdf"
        parte = MIMEBase("application", "octet-stream")
        parte.set_payload(open(archivo_adjunto, "rb").read())
        encode_base64(parte)
        parte.add_header("Content-Disposition", f"attachment; filename= {archivo_adjunto}")
        msg.attach(parte)

        # Agregar el cuerpo del mensaje al correo electrónico
        msg.attach(MIMEText(mensaje, "plain"))

        # Establecer conexión con el servidor SMTP y enviar el correo electrónico
        servidor_smtp = "smtp.gmail.com"
        puerto_smtp = 587
        usuario_smtp = "jaramirez9562@misena.edu.co"
        contrasena_smtp = "qekifshlutsdeacy"

        with smtplib.SMTP(servidor_smtp, puerto_smtp) as servidor:
            servidor.starttls()
            servidor.login(usuario_smtp, contrasena_smtp)
            servidor.send_message(msg)


        return 'PDF generado correctamente'
    
    elif request.method == 'GET':
        #return render_template('crear_informe.html')
        return 'PDF generado correctamente'

if __name__ == '__main__':
    app.run(debug=True)