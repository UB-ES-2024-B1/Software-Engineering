
# Software Engineering - Group B1 (2024)
Created by Matthew Ayete Corrales, Daniel González Braza, Albert Digon Quintillà, Wenwen Yang, Raquel Nuñez Padial, Guillem Vera Pérez.

Welcome to the repository of FilmHub, application for the **Software Engineering** course, Group B1, for the academic year 2024. This repository contains all files and documentation related to the development of projects and activities for this course.

## Description

In this repository, we will manage and develop the assignments for the **Software Engineering** course, focusing on the planning, design, implementation, and testing of software. Throughout the course, we will use agile development tools and methodologies to manage project progress.

## Tools Used

Several tools will be utilized to help us organize and develop the projects efficiently:

- **Trello**: We will use Trello for project and task management, implementing Kanban boards to plan activities.
- **GitHub**: This repository will serve as version control and for collaborative development of the projects. Each student is required to submit pull requests and perform code reviews.
- **Programming Languages**: Depending on the project, various programming languages will be used (e.g., Python, Java, etc.).

## Repository Structure

The repository will be organized as follows:

```
/docs
    - Project documentation, including requirements analysis, designs, and user manuals.
    
/src
    - Project source code.
    
/tests
    - Unit and functional tests.
    
/backlog
    - Archive of tasks and features that have not been implemented yet.
    
/meeting-notes
    - Summaries and minutes of team meetings.
```

## Contributions

Each group member is expected to contribute actively to the project, both in code development and in the planning and execution of tasks. The following guidelines are recommended:

1. **Fork the repository**: Each student should fork the repository and work in their own branch.
2. **Pull Requests**: After completing a task, create a pull request for the team to review and approve the changes.
3. **Task Assignment**: Tasks will be assigned via Trello or GitHub Issues. Each student must track progress and update the status of tasks as they advance.

## Methodology

We will use **agile methodologies**, such as Scrum or Kanban, to organize the team's work. This includes:

- **Sprints**: Each sprint will last 1 or 2 weeks. During the sprint, assigned tasks will be worked on, and progress will be reviewed.
- **Daily meetings**: Short meetings to track task progress and address any blockers.
- **Sprint reviews**: At the end of each sprint, a review of the completed work will be done, and the objectives for the next sprint will be adjusted.


## How to use

### Documentación del Proyecto

Este proyecto es una aplicación Fullstack con un **backend** construido con **FastAPI** y una **base de datos SQLite**, y un **frontend** simple creado con **Vue.js**. A continuación, se describe cómo configurar y ejecutar el proyecto en tu máquina local.

---

### **Requisitos**

Asegúrate de tener instalados los siguientes programas antes de comenzar:
- **Python 3.10+**
- **Node.js y npm**
- **Vue CLI** (si no lo tienes instalado globalmente, sigue las instrucciones más abajo)

---

### **Configuración y Ejecución del Backend (FastAPI)**

1. **Clonar el repositorio**:
   
   Clona este proyecto en tu máquina local:
   ```bash
   git clone https://github.com/tu-usuario/tu-repositorio.git
   cd tu-repositorio
   ```

2. **Crear y activar un entorno virtual de Python**:
   
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Instalar dependencias del backend**:

   ```bash
   pip install fastapi uvicorn
   pip install pytest httpx
   pip install sqlalchemy databases[sqlite]
   pip install fastapi[all]
   ```

4. **Navegar a la carpeta del backend**:
   
   ```bash
   cd backend
   ```

5. **Ejecutar las pruebas del backend** (opcional, pero recomendado para asegurarte de que todo esté funcionando correctamente):

   ```bash
   pytest
   ```
   o
   ```bash
   python -m pytest
   ```
   
6. **Ejecutar el servidor del backend**:
   
   Inicia el servidor FastAPI:
   ```bash
   uvicorn backend.main:app --reload
   ```

   El backend estará disponible en `http://localhost:8000`.

7. **Desactivar el entorno virtual** cuando termines de trabajar en el backend:
   
   ```bash
   deactivate
   ```

---

### **Configuración y Ejecución del Frontend (Vue.js)**

1. **Instalar Vue CLI globalmente** (si aún no lo tienes):

   ```bash
   npm install -g @vue/cli
   ```

2. **Navegar a la carpeta del frontend**:

   ```bash
   cd frontend
   ```

3. **Instalar dependencias del frontend**:
   
   ```bash
   npm install
   npm install axios
   ```

4. **Ejecutar el servidor del frontend**:

   Inicia el servidor de desarrollo de Vue.js:
   ```bash
   npm run serve
   ```

   El frontend estará disponible en `http://localhost:8080`.

---

### **Instrucciones Finales**

Para ejecutar el proyecto completo:

1. **Iniciar el backend** con FastAPI:
   ```bash
   uvicorn backend.main:app --reload
   ```

2. **Iniciar el frontend** con Vue.js:
   ```bash
   npm run serve
   ```

Ahora, deberías tener tanto el **backend** en `http://localhost:8000` como el **frontend** en `http://localhost:8080` funcionando en tu máquina local.


## License

This project is licensed under the MIT License. For more details, see the `LICENSE` file.
