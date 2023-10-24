# %% [markdown]
# ![title](./logo_nao_digital.png)

# %% [markdown]
# # **Tienes un mensaje**

# %% [markdown]
# ## Evidencias ciclo ID3

# %% [markdown]
# *Instrucciones:*
# 
# 
# Atiende las siguientes indicaciones para completar las evidencias de este primer ciclo de investigación y desarrollo de esta experiencia de aprendizaje.
# 
# 1. Lee detenidamente el reto Tienes un mensaje.
# 
# 2. Desarrolla las evidencias solicitadas para este ciclo ID:
# * Envía un PDF personalizado a cada correo del CSV.
# * Automatiza el envío con Bash.
# * Toma como evidencia el enlace al código en GitHub.
# * Envía y recibe un correo con el PDF y toma una captura de pantalla.
# 
# 3. Sube las evidencias a tu espacio en Notion.

# %% [markdown]
# ## Etapa 1: instalar e importar librerías de trabajo

# %% [markdown]
# Primero instalamos e importamos las librerías de trabajo

# %%
%pip install pandas
%pip install reportlab
%pip install fpdf

# %%
import pandas as pd
import os
import numpy as np
import smtplib
import openpyxl
import csv
import random
import datetime

# Import the email modules we'll need
from email.message import EmailMessage
# Para la lista de cumpleaños
from datetime import datetime, timedelta
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from fpdf import FPDF
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image

import warnings
warnings.filterwarnings('ignore')

# %% [markdown]
# ## Etapa 2: generar una lista de ingresos y completar la CSV

# %%
# Crear una lista de 500 fechas de ingreso aleatorias entre 1998-05-12 y hoy
start_date = datetime(1998, 5, 12)
end_date = datetime.now()

ingreso = [start_date + timedelta(days=random.randint(0, (end_date - start_date).days)) for _ in range(500)]

# %%
# Crear un DataFrame de pandas con las fechas de ingreso
fecha_ingreso = pd.DataFrame({'fecha_ingreso': ingreso})
fecha_ingreso.sample(10)

# %%
# Leer el archivo CSV existente
base_de_datos = pd.read_csv('BD_BrokenIA_cumpleanos.csv')

# Agregar la columna de fechas de ingeso al DataFrame existente y convertir a datetime
base_de_datos['fecha_ingreso'] = fecha_ingreso['fecha_ingreso']

# Ahora tenemos la base de datos generada, podemos guardarla como CSV
base_de_datos.to_csv('BD_BrokenIA_ingresos.csv', index=False)

# %%
base_de_datos.sample(10)

# %%
base_de_datos.dtypes

# %% [markdown]
# ## Etapa 3: leer la lista de nombres, correos y fechas del CSV y generar PDF de acuerdo de confidencialidad

# %%
# Función para generar el acuerdo de confidencialidad en PDF
def generate_confidentiality_agreement(nombre, fecha):
    # Crear un documento PDF
    doc = SimpleDocTemplate(f"{nombre}_acuerdo_confidencialidad.pdf", pagesize=letter)
    # Estilo para el título
    estilo_titulo = ParagraphStyle(name='TitleStyle', fontSize=18, alignment=1, spaceAfter=12, leading=20)
    # Estilo para el cuerpo del acuerdo
    estilo_cuerpo = ParagraphStyle(name='CuerpoStyle', fontSize=14, alignment=4, spaceAfter=12)
    # Contenido del acuerdo
    contenido = []

    # Título centrado en el PDF
    titulo = Paragraph("ACUERDO DE CONFIDENCIALIDAD RECÍPROCO SUSCRITO ENTRE BROKEN IA Y EL EMPLEADO", estilo_titulo)
    contenido.append(titulo)

    # Logo de la empresa en la esquina superior izquierda
    logo_path = './logo_BrokenIA_fondo_blanco.png'
    logo = Image(logo_path, width=3*cm, height=3*cm)
    contenido.append(logo)

    # Párrafos del acuerdo
    parrafos = [
        f"Yo {nombre} obrando en mi calidad de empleado de hoy terminóme comprometo a mantener la integridad, reserva y confidencialidad de la información de los Sistemas de Información suministrados con ocasión del desarrollo de las tareas laborales.",
        f"Con la firma del presente documento, me comprometo a abstenerme de revelar la información confidencial de la que tenga conocimiento, siendo consciente de las penas, multas y sanciones derivadas del incumplimiento, al igual de las demás acciones que puedan llegar a derivarse de éste y del Acuerdo de Confidencialidad Recíproco suscrito entre BROKEN IA y {nombre}.",
        "Por lo tanto, me hago responsable de seguir las políticas de seguridad y procedimientos para el uso de acceso a la información, evitando cualquier práctica o uso inapropiado que pudiera poner en peligro la información, integridad y reputación de los Sistemas de Información de BROKEN IA.",
        f"En señal de expresa conformidad y aceptación de los términos recogidos en el presente compromiso se firma en México, a los {fecha}."
    ]

    for parrafo in parrafos:
        contenido.append(Paragraph(parrafo, estilo_cuerpo))
        contenido.append(Spacer(1, 14))  # Espacio entre párrafos

    # Espacio entre el cuerpo y las firmas
    contenido.append(Spacer(1, 30))

    # Información de Nombre y Firma
    contenido.append(Paragraph(f"Nombre: {nombre}", estilo_cuerpo))
    contenido.append(Paragraph("Firma: _______________________________", estilo_cuerpo))

    # Espacio entre las firmas y la fecha
    contenido.append(Spacer(1, 30))

    # Fecha actual
    fecha_actual = fecha.strftime("%d/%m/%Y")
    contenido.append(Paragraph(f"Fecha de firma: {fecha_actual}", estilo_cuerpo))

    # Generar el PDF
    doc.build(contenido)

# Función para enviar correos electrónicos
def send_email(to_email, subject, message, filename):
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_user = 'nataliahoyos@gmail.com' 
    smtp_password = 'iqpb razm awxa taqo'

    # Dirección de correo de destino fija
    correo_destino = 'nataliahoyos@gmail.com'

    email_message = MIMEMultipart()
    email_message['From'] = smtp_user
    email_message['To'] = correo_destino
    email_message['Subject'] = f'Contrato de confidencialidad'

    email_message.attach(MIMEText('Te hacemos llegar el nuevo contrato de confidencialidad para que por favor lo regreses firmado, ¡feliz día!', 'plain'))

    with open(filename, 'rb') as pdf_file:
        pdf_attach = MIMEApplication(pdf_file.read(), _subtype="pdf")
        pdf_attach.add_header('Content-Disposition', f'attachment; filename={filename}')
        email_message.attach(pdf_attach)

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.sendmail(smtp_user, correo_destino, email_message.as_string())

# Leer la base de datos desde el archivo CSV
base_datos_ingresos = pd.read_csv("BD_BrokenIA_ingresos.csv")

# Calcular la fecha actual
fecha_actual = datetime.now()

# Iterar a través de los empleados
for index, row in base_datos_ingresos.iterrows():
    fecha_ingreso = datetime.strptime(row['fecha_ingreso'], '%Y-%m-%d')  # Asumiendo un formato de fecha adecuado

    # Calcular la diferencia de días desde la fecha de ingreso
    dias_transcurridos = (fecha_actual - fecha_ingreso).days

    # Verificar si han pasado 180 días (o múltiplos) desde la fecha de ingreso
    if dias_transcurridos % 180 == 0:
        nombre_empleado = row['nombre']
        email = row['email']
        mensaje = row['mensaje']

        # Generar el acuerdo de confidencialidad en PDF
        generate_confidentiality_agreement(nombre_empleado, fecha_actual)

        # Enviar el correo electrónico con el contrato adjunto
        send_email(email, "Acuerdo de Confidencialidad", mensaje, f"{nombre_empleado}_acuerdo_confidencialidad.pdf")

        print(f"Acuerdo de confidencialidad generado y correo enviado a {nombre_empleado}")


# %% [markdown]
# ## Etapa 4: Acerca del funcionamiento del código principal: envío de acuerdo de confidencialidad

# %% [markdown]
# El código anterior  es una implementación de generación de acuerdos de confidencialidad en formato PDF y su envío por correo electrónico a los empleados de la empresa "BROKEN IA" cuyos contratos cumplen 180 días o múltiplos de 180 días:
# 
# 1. **`generate_confidentiality_agreement` Function**:
#    Esta función se encarga de crear un acuerdo de confidencialidad en formato PDF para un empleado específico. Aquí están los detalles:
# 
#    - **Creación de PDF**: La función crea un documento PDF con el nombre del empleado y un título centrado que describe el acuerdo de confidencialidad.
# 
#    - **Estilos de Texto**: Define dos estilos de texto: uno para el título (`estilo_titulo`) y otro para el cuerpo del acuerdo (`estilo_cuerpo`). Estos estilos especifican el tamaño de fuente, alineación, espacio después del párrafo y el interlineado.
# 
#    - **Contenido del PDF**:
#      - Agrega el título centrado en el PDF.
#      - Inserta el logotipo de la empresa en la esquina superior izquierda del PDF.
#      - Define una serie de párrafos que componen el contenido del acuerdo, incluyendo el nombre del empleado y los detalles del compromiso de confidencialidad.
#      - Agrega cada párrafo al contenido del PDF con espacio adicional entre ellos para mejorar la legibilidad.
#      - Inserta información sobre el nombre y la firma del empleado.
#      - Agrega la fecha actual en el formato día/mes/año, como se especificó.
# 
#    - **Generación del PDF**: Finalmente, la función genera el PDF con todo el contenido definido y lo guarda con el nombre del empleado.
# 
# 2. **`send_email` Function**:
#    Esta función se encarga de enviar un correo electrónico que incluye el acuerdo de confidencialidad como archivo adjunto. Aquí están los detalles:
# 
#    - **Configuración del Servidor SMTP**: Se establecen las configuraciones del servidor SMTP para enviar correos electrónicos. Esto incluye el servidor SMTP (Gmail en este caso), el puerto y las credenciales de inicio de sesión.
# 
#    - **Creación del Correo Electrónico**: La función crea un correo electrónico utilizando la biblioteca `email.mime`. Se establece el remitente, el destinatario, el asunto del correo electrónico y un mensaje de texto plano.
# 
#    - **Archivo Adjunto**: Se adjunta el acuerdo de confidencialidad (PDF) al correo electrónico. El archivo se carga desde el sistema de archivos y se adjunta al mensaje de correo electrónico.
# 
#    - **Envío del Correo Electrónico**: La función inicia una conexión con el servidor SMTP, inicia una sesión segura y envía el correo electrónico a la dirección de destino.
# 
# 3. **Main Loop**:
#    En el bucle principal, el código realiza las siguientes acciones:
# 
#    - Lee una base de datos de empleados desde un archivo CSV llamado "BD_BrokenIA_ingresos.csv" y la almacena en un DataFrame de pandas llamado `base_datos_ingresos`.
# 
#    - Calcula la fecha actual utilizando la función `datetime.now()`.
# 
#    - Itera a través de cada fila (empleado) en el DataFrame `base_datos_ingresos`.
# 
#    - Calcula la diferencia en días entre la fecha de ingreso del empleado y la fecha actual.
# 
#    - Verifica si han pasado 180 días o un múltiplo de 180 días desde la fecha de ingreso. Si es así, genera un acuerdo de confidencialidad en PDF y lo envía al empleado por correo electrónico.
# 
#    - El acuerdo de confidencialidad se genera utilizando la función `generate_confidentiality_agreement`, y se envía por correo electrónico utilizando la función `send_email`. El correo electrónico contiene un mensaje fijo y el acuerdo de confidencialidad como archivo adjunto.
# 
#    - Se muestra un mensaje en la consola indicando que el acuerdo de confidencialidad ha sido generado y enviado al empleado correspondiente.


