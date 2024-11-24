# Etapa 1: Construcción de la aplicación
FROM node:lts-alpine AS build-stage

# Configuración del directorio de trabajo
WORKDIR /app

# Copiar los archivos necesarios para instalar dependencias
COPY package*.json ./

# Instalar las dependencias
RUN npm install

RUN npm install axios
# Copiar todo el código fuente de la aplicación al contenedor
COPY . .

# Construir la aplicación para producción
RUN npm run build

# Etapa 2: Configuración del servidor Nginx para producción
FROM nginx:stable-alpine AS production-stage

# Copiar los archivos generados en la etapa de construcción al directorio que Nginx sirve
COPY --from=build-stage /app/dist /usr/share/nginx/html

EXPOSE 80

# Comando para iniciar Nginx
CMD ["nginx", "-g", "daemon off;"]
