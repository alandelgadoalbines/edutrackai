# Instalación en cPanel

Guía rápida para desplegar la aplicación en cPanel utilizando adahost.pe.

## Crear base de datos en phpMyAdmin
1. Ingresa a cPanel y abre **MySQL® Databases** para crear una nueva base de datos y un usuario con contraseña segura.
2. Asocia el usuario a la base de datos con privilegios **All Privileges**.
3. Entra a **phpMyAdmin**, selecciona la base de datos creada y confirma que está vacía antes de importar.

## Importar `schema.sql`
1. En **phpMyAdmin**, elige la base de datos y navega a la pestaña **Importar**.
2. Pulsa **Seleccionar archivo** y sube el archivo `schema.sql` incluido en el proyecto.
3. Ejecuta la importación (UTF-8, formato SQL). Verifica que las tablas se creen sin errores.

## Configurar Python App en cPanel
1. En cPanel, abre **Setup Python App** (Aplicaciones Python).
2. Crea una nueva aplicación con la versión de Python recomendada por el proyecto (por ejemplo, 3.10+).
3. Define la ruta del proyecto (p. ej., `/home/usuario/edutrackai`) y el punto de entrada WSGI según tu framework (por ejemplo, `passenger_wsgi.py`).
4. Agrega los paquetes del archivo `requirements.txt` mediante el botón **Add Import** o ejecuta `pip install -r requirements.txt` desde el terminal de cPanel activando el virtualenv (`source ./venv/bin/activate`).

## Variables de entorno `.env`
1. Crea un archivo `.env` en la raíz del proyecto con las variables necesarias (credenciales de DB, secretos, URLs). Ejemplo:

   ```env
   FLASK_ENV=production
   DATABASE_URL=mysql+pymysql://USER:PASSWORD@HOST:3306/NOMBRE_DB
   SECRET_KEY=tu_clave_segura
   
   # Ajusta según tu proveedor de correo o servicios externos
   MAIL_SERVER=smtp.tu_dominio
   MAIL_PORT=465
   MAIL_USERNAME=usuario
   MAIL_PASSWORD=contraseña
   MAIL_USE_SSL=true
   ```
2. En **Setup Python App**, usa la sección **Environment Variables** para declarar cada variable o apunta el código a cargar el `.env` en el arranque.
3. Protege el `.env` para que no sea accesible públicamente (ej. con reglas `.htaccess` si usas Passenger/Apache).

## Probar URLs finales en adahost.pe
1. Despliega la app y asegúrate de que el dominio o subdominio apunte al directorio de la aplicación.
2. Verifica las rutas principales (ajusta según tu app):
   - `https://adahost.pe/` (página principal)
   - `https://adahost.pe/login` o ruta de autenticación.
   - `https://adahost.pe/api/health` o endpoint de salud si existe.
3. Revisa el **Error Log** y **Access Log** de cPanel para confirmar que no haya errores 500/404.
4. Si usas HTTPS, confirma que el certificado SSL de cPanel esté activo y vigente.
