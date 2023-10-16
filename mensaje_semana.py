# %% [markdown]
# ![title](./logo_nao_digital.png)

# %% [markdown]
# # **Tienes un mensaje**

# %% [markdown]
# ## Evidencias ciclo ID1

# %% [markdown]
# *Instrucciones:*
# 
# 
# Atiende las siguientes indicaciones para completar las evidencias de este primer ciclo de investigación y desarrollo de esta experiencia de aprendizaje.
# 
# 1. Lee detenidamente el reto Tienes un mensaje.
# 
# 2. Desarrolla las evidencias solicitadas para este ciclo ID:
# * Crea un script en Python para leer una lista de correos de un CSV y enviar un saludo en un correo electrónico.
# * Crea un script en Bash para invocar cada lunes este correo.
# * Toma como evidencia el enlace al código en GitHub.
# * Envía y recibe un correo electrónico y toma captura de pantalla.
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

# Import the email modules we'll need
from email.message import EmailMessage

import warnings
warnings.filterwarnings('ignore')

# %% [markdown]
# ## Etapa 2: generar una lista de nombres, correos y mensajes CSV

# %%
# Primero generamos una lista de nombres de alguna base de datos de la red
# Se tratan de 500 empleados, elegiremos 250 hombre y 250 mujeres

# Censo nombre de Brasil en formato json
pd.set_option('display.max_rows', None)

nombres_m = pd.read_json("https://servicodados.ibge.gov.br/api/v1/censos/nomes/ranking/?sexo=M&qtd=250")
nombres_f = pd.read_json("https://servicodados.ibge.gov.br/api/v1/censos/nomes/ranking/?sexo=F&qtd=250")

# %%
print("Cantidad de nombres: " + str(len(nombres_m) + len(nombres_f)))

# %%
# La información está almacenada como lista, ahora la pasamos a DataFrame
nombres = [nombres_m, nombres_f]
nombres

# %%
# Vamos a dejar solamente la columna nome (de una vez renombrándola por nombre)
nombres = pd.concat(nombres)['nome'].to_frame()
nombres.columns = ['nombre']
nombres.sample(5)

# %%
# Ahora generamos los servidores de correos y los asignamos de manera aleatoria
dominio = ['@emailbrokenia.com']
nombres['dominio'] = np.random.choice(dominio, len(nombres))
nombres.sample(5)

# %%
# Asignamos e-mails con nombre + dominio, teniendo cuidado con las mayúsculas
nombres['email'] = nombres.nombre.str.cat(nombres.dominio).str.lower()
nombres.sample(5)

# %%
# Asignamos la columna mensaje, el usuario deberá ingresar el mensaje deseado 
mensaje = input('Ingrese mensaje para inicio de la semana: ')
nombres['mensaje'] = mensaje
nombres.sample(5)

# %%
# Eliminamos la columna dominio
nombres = nombres.drop(columns=['dominio'])
nombres.sample(5)

# %%
# Ahora tenemos la base de datos generada, podemos guardarla como CSV
nombres.to_csv('BD_BrokenIA.csv', index = False)

# %% [markdown]
# ## Etapa 3: leer la lista de nombres, correos y mensajes del CSV y enviar email

# %%
# Configuración de la conexión SMTP
smtp_server = 'smtp.gmail.com'
smtp_port = 587
smtp_user = 'nataliahoyos@gmail.com' 
smtp_password = 'iqpb razm awxa taqo'

# Dirección de correo de destino fija
correo_destino = 'nataliahoyos@gmail.com'

# Leer el archivo CSV
with open('BD_BrokenIA.csv', 'r', newline='') as csvfile:
    base_de_datos = csv.reader(csvfile)
    # Salta la primera fila para ignorar los encabezados 
    next(base_de_datos)

    # Contador para enviar a las primeras 10 personas
    contador = 0

    for row in base_de_datos:
        nombre = row[0]
        mensaje = row[2]

        # Crear unmensaje de correo electrónico
        email_message = EmailMessage()
        email_message.set_content(f'Hola, {nombre}: {mensaje}')

        email_message['From'] = smtp_user
        email_message['To'] = correo_destino
        email_message['Subject'] = 'Mensaje semanal'

        # Conectar y autenticar con el servidor SMTP
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Habilitar TLS si es necesario
            server.login(smtp_user, smtp_password)
            server.send_message(email_message)

        print(f'Correo enviado a {correo_destino} para {nombre}')
        
        # Incrementar el contador
        contador += 1

        # Salir del bucle después de enviar a las primeras 10 personas
        if contador >= 10:
            break


# %% [markdown]
# ## Etapa 4: Acerca del código

# %% [markdown]
# El código anterior tiene como objetivo enviar correos electrónicos personalizados a partir de un archivo CSV con los siguientes componentes:
# 
# 1. **Configuración de la conexión SMTP:** Establece la configuración para la conexión al servidor SMTP de Gmail. Incluye el servidor SMTP (`smtp_server`), el puerto SMTP (`smtp_port`), la dirección de correo electrónico del remitente (`smtp_user`), y la contraseña de la aplicación generada para autenticación (`smtp_password`).
# 
# 2. **Dirección de correo de destino fija:** Define la dirección de correo electrónico de destino, que en este caso es constante y se establece en `correo_destino` para efectos de realizar pruebas y asegurar la funcionalidad del código.
# 
# 3. **Lectura del archivo CSV:** Abre y lee el archivo CSV denominado "BD_BrokenIA.csv" utilizando la biblioteca `csv`. El bucle `for` se utiliza para iterar a través de las filas del archivo CSV.
# 
# 4. **Contador para enviar a las primeras 10 personas:** Se utiliza un contador (`contador`) para rastrear cuántos correos se han enviado. La idea es enviar correos personalizados a las primeras 10 personas en la base de datos y luego salir del bucle para probar el código
# 
# 5. **Creación de un objeto de mensaje de correo electrónico:** Para cada persona en la base de datos, se crea un objeto `email_message` de la clase `EmailMessage` para representar el correo electrónico que se va a enviar. El cuerpo del correo electrónico se personaliza utilizando el nombre de la persona (`nombre`) y el mensaje de la fila actual del archivo CSV (`mensaje`).
# 
# 6. **Configuración del correo electrónico:** Se establece el remitente (`From`), el destinatario (`To`), el asunto (`Subject`) y el contenido del mensaje del objeto `email_message`.
# 
# 7. **Conexión y autenticación SMTP:** Se inicia una conexión al servidor SMTP de Gmail y se habilita el uso de TLS para seguridad. Luego, se autentica con la dirección de correo electrónico del remitente (`smtp_user`) y la contraseña de la aplicación generada (`smtp_password`).
# 
# 8. **Envío del correo electrónico:** El correo electrónico se envía al destinatario (`correo_destino`) utilizando el objeto `email_message` configurado previamente.
# 
# 9. **Impresión de un mensaje de confirmación:** Se imprime un mensaje para confirmar que el correo se ha enviado con éxito.
# 
# 10. **Incremento del contador y salida del bucle:** El contador se incrementa en cada iteración. Cuando el contador alcanza 10, se utiliza la instrucción `break` para salir del bucle, lo que asegura que solo se envíen correos a las primeras 10 personas.
# 
# Este código permite automatizar el envío de correos electrónicos personalizados.


