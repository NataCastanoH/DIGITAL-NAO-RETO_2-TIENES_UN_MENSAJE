#!/bin/bash

# Ubicación del script de Python (tarjeta_felicitacion.py)
script_python = "C:\Users\Natalia\Recursos DN_COM_58\DIGITAL-NAO-RETO_2-TIENES_UN_MENSAJE\acuerdo_confidencialidad.py" 

# Comprueba si hoy es lunes (día de la semana 1 en cron)
if [ "$(date +\%H)" == "09" ]; then
    # Ejecuta el script de Python para enviar la tarjeta de felicitación a las 9:00 a. m.
    python3 "$script_python"
fi
