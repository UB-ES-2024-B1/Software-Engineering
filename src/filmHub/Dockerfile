FROM nginx:stable

# Copiar los archivos construidos de Vue (dist/) al directorio predeterminado de nginx
COPY dist /usr/share/nginx/html

# Copiar el archivo nginx.conf
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Exponer el puerto para nginx
EXPOSE 80

# Comando por defecto para iniciar nginx
CMD ["nginx", "-g", "daemon off;"]
