# %% [markdown]
# ![title](./logo_nao_digital.png)

# %% [markdown]
# # **Tienes un mensaje**

# %% [markdown]
# ## Evidencias ciclo ID2

# %% [markdown]
# *Instrucciones:*
# 
# 
# Atiende las siguientes indicaciones para completar las evidencias de este primer ciclo de investigación y desarrollo de esta experiencia de aprendizaje.
# 
# 1. Lee detenidamente el reto Tienes un mensaje.
# 
# 2. Desarrolla las evidencias solicitadas para este ciclo ID:
# * Crea un template de HTML para una tarjeta de felicitación.
# * Automatiza el envío de correo de cumpleaños con Bash.
# * Toma como evidencia el enlace al código en GitHub.
# * Envía y recibe un correo con la tarjeta de felicitación y toma captura de pantalla como evidencia.
# 
# 3. Sube las evidencias a tu espacio en Notion.

# %% [markdown]
# ## Etapa 1: instalar e importar librerías de trabajo

# %% [markdown]
# Primero instalamos e importamos las librerías de trabajo

# %%
%pip install pandas

# %%
import os
import numpy as np
import pandas as pd
import smtplib
import openpyxl
import csv
import random

# Import the email modules we'll need
from email.message import EmailMessage
# Para la lista de cumpleaños
from datetime import datetime, timedelta

import warnings
warnings.filterwarnings('ignore')

# %% [markdown]
# ## Etapa 2: generar una lista de cumpleaños y completar la CSV

# %%
# Crear una lista de 500 fechas de nacimiento aleatorias entre 1950-01-01 y 2000-12-31
start_date = datetime(1950, 1, 1)
end_date = datetime(2006, 12, 31)

cumpleanos = [start_date + timedelta(days=random.randint(0, (end_date - start_date).days)) for _ in range(500)]

# %%
# Crear un DataFrame de pandas con las fechas de nacimiento
fecha_nacimiento = pd.DataFrame({'fecha_nacimiento': cumpleanos})
fecha_nacimiento.sample(10)

# %%
# Leer el archivo CSV existente
base_de_datos = pd.read_csv('BD_BrokenIA.csv')

# Agregar la columna de fechas de nacimiento al DataFrame existente y convertir a datetime
# base_de_datos['fecha_nacimiento'] = fecha_nacimiento['fecha_nacimiento']
base_de_datos['fecha_nacimiento'] = fecha_nacimiento['fecha_nacimiento']

# Ahora tenemos la base de datos generada, podemos guardarla como CSV
base_de_datos.to_csv('BD_BrokenIA_cumpleanos.csv', index=False)

# %%
base_de_datos.sample(10)

# %%
base_de_datos.dtypes

# %% [markdown]
# ## Etapa 3: leer la lista de nombres, correos y fechas del CSV y generar html de felicitación

# %%
# Configuración de la conexión SMTP
smtp_server = 'smtp.gmail.com'
smtp_port = 587
smtp_user = 'nataliahoyos@gmail.com' 
smtp_password = 'iqpb razm awxa taqo'

# Dirección de correo de destino fija
correo_destino = 'nataliahoyos@gmail.com'

# Leer el archivo CSV
fechas_cumpleanos = pd.read_csv('BD_BrokenIA_cumpleanos.csv', parse_dates=['fecha_nacimiento'], date_parser=lambda x: datetime.strptime(x, '%Y-%m-%d'))

# Obtener la fecha actual
hoy = datetime.now()

# Cargar el contenido HTML de la felicitación
with open('template_tarjeta_felicitacion.html', 'r') as html_file:
    contenido_html = html_file.read()

# Bucle for para enviar correos electrónicos
for index, row in fechas_cumpleanos.iterrows():
    nombre = row['nombre']
    fecha_nacimiento = row['fecha_nacimiento']

    # Obtén el nombre de la persona desde el CSV
    nombre_persona = row['nombre'] 

    # Obtener el mes y el día de la fecha de nacimiento
    mes_nacimiento = fecha_nacimiento.month
    dia_nacimiento = fecha_nacimiento.day
    
    # Comparar la fecha actual con la fecha de nacimiento
    if hoy.month == mes_nacimiento and hoy.day == dia_nacimiento:
        # Crear un mensaje de correo electrónico personalizado
        email_message = EmailMessage()

        # Realizar el reemplazo del marcador de posición con el nombre de la persona dentro del bucle
        contenido_html_personalizado = contenido_html.replace('{nombre}', nombre_persona)

        email_message.set_content(f'¡Feliz cumpleaños, {nombre}!')

        email_message['From'] = smtp_user
        email_message['To'] = correo_destino
        email_message['Subject'] = f'¡Feliz cumpleaños, {nombre}!'

        # Agregar el contenido HTML personalizado al mensaje
        email_message.add_alternative(contenido_html_personalizado, subtype='html')

        # Conectar y autenticar con el servidor SMTP
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Habilitar TLS si es necesario
            server.login(smtp_user, smtp_password)
            server.send_message(email_message)

        print(f'Correo enviado a {correo_destino} para {nombre}')


# %% [markdown]
# ## Etapa 4: Acerca del funcionamiento del código principal: envío de tarjeta de felicitación

# %% [markdown]
# El código anterior tiene como objetivo enviar correos electrónicos con una felicitación de cumpleaños partir de un archivo CSV y un template en HTML con los siguientes componentes:
# 
# 1. **Configuración de la conexión SMTP**: Aquí se definen las configuraciones necesarias para establecer la conexión con el servidor SMTP. Estos valores son específicos de tu proveedor de correo. En este caso, se configura para Gmail.
# 
#     - `smtp_server`: La dirección del servidor SMTP de Gmail.
#     - `smtp_port`: El puerto utilizado para la conexión al servidor SMTP de Gmail.
#     - `smtp_user`: Tu dirección de correo electrónico desde la cual se enviarán los mensajes.
#     - `smtp_password`: La contraseña de tu cuenta de correo.
# 
# 2. **Dirección de correo de destino fija**: Esto establece la dirección de correo de destino, que en este caso se mantiene fija como `'nataliahoyos@gmail.com'`. Sin embargo, esto podría cambiarse para enviar correos a diferentes destinatarios.
# 
# 3. **Leer el archivo CSV**: Aquí se lee el archivo CSV llamado `'BD_BrokenIA_cumpleanos.csv'` utilizando pandas. Se utiliza `parse_dates` para convertir la columna 'fecha_nacimiento' en objetos de fecha y hora. También se especifica un `date_parser` para analizar las fechas en el formato correcto.
# 
# 4. **Obtener la fecha actual**: Se utiliza `datetime.now()` para obtener la fecha y hora actual.
# 
# 5. **Cargar el contenido HTML de la felicitación**: Abre y lee el contenido del archivo HTML de la tarjeta de felicitación desde `'template_tarjeta_felicitacion.html'`. El contenido se almacena en la variable `contenido_html`.
# 
# 6. **Obtener el nombre de la persona desde el CSV**: Esto es donde ocurre un error en el código original. El intento de obtener el nombre de la persona está fuera del bucle `for`. La variable `row` no está definida en este punto y, por lo tanto, no se puede acceder al nombre de la persona en este lugar. Esto debería estar dentro del bucle `for` para obtener el nombre de cada persona desde el archivo CSV en cada iteración.
# 
# 7. **Reemplazar el marcador de posición con el nombre de la persona**: Aquí, se reemplaza el marcador de posición `{nombre}` en el contenido HTML con el nombre de la persona. Sin embargo, esto debería realizarse dentro del bucle `for` para cada persona individualmente, pero en el código proporcionado, se hace fuera del bucle, por lo que solo se toma el nombre de una persona (la última en el archivo CSV).
# 
# 8. **Guardar los cambios en el archivo HTML**: Después de reemplazar el marcador de posición por el nombre de la persona, el contenido HTML se guarda en un nuevo archivo llamado `'tarjeta_felicitacion.html'`. Este paso no es necesario para enviar correos electrónicos, ya que solo estás guardando el contenido HTML en un archivo.
# 
# 9. **Bucle `for` para enviar correos electrónicos**: Este bucle `for` itera a través de las filas del DataFrame `fechas_cumpleanos`, que contiene la información de las personas cuyo cumpleaños se celebra. Para cada persona, se verifica si la fecha de nacimiento coincide con la fecha actual.
# 
# 10. **Crear un mensaje de correo electrónico personalizado**: Si la fecha de cumpleaños coincide, se crea un mensaje de correo electrónico personalizado utilizando la biblioteca `EmailMessage`. El contenido del correo electrónico se establece con un saludo de cumpleaños y se especifica la dirección del remitente y del destinatario.
# 
# 11. **Agregar el contenido HTML al mensaje**: Aquí es donde se adjunta el contenido HTML de la tarjeta de felicitación al mensaje de correo electrónico. Sin embargo, dado que se ha reemplazado el marcador de posición por el nombre de la persona fuera del bucle, el nombre en el correo electrónico será el mismo para todos los destinatarios.
# 
# 12. **Conectar y enviar el correo electrónico**: Finalmente, se establece una conexión con el servidor SMTP de Gmail, se inicia la sesión, y se envía el correo electrónico a la dirección de correo de destino. Luego, se muestra un mensaje indicando que se ha enviado el correo.


