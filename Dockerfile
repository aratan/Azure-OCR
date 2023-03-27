# Imagen base
FROM ubuntu

# Directorio de trabajo
WORKDIR /app

# Copiar los archivos necesarios
# COPY requirements.txt .
C# OPY app.py .

# Instalar las dependencias
# RUN pip install --no-cache-dir -r requirements.txt
RUN echo "Hola Mundo"
# Exponer el puerto 5000
# EXPOSE 5000

# Comando para iniciar la aplicación
# CMD ["python", "app.py"]
