#!/bin/bash

# Ubicación del script de Python (mensaje_semanal.py)
script_python = "C:\Users\Natalia\Recursos DN_COM_58\DIGITAL-NAO-RETO_2-TIENES_UN_MENSAJE\mensaje_semanal.py" 

# Comprueba si hoy es lunes (día de la semana 1 en cron)
if [ "$(date +\%u)" == "1" ]; then
    # Comprueba si la hora actual es igual a las 8 a. m. (hora 8 en cron)
    if [ "$(date +\%H)" == "08" ]; then
    # Ejecuta el script de Python para enviar el correo a las 8:00 a. m.
    python3 "$script_python"
    fi
fi