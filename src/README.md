
# Backend and Frontend Project

This project consists of two main parts: the **backend** developed with **FastAPI** and the **frontend** developed with **Vue.js**.

---

### **Backend Setup and Execution (FastAPI)**

1. **Clone the repository**:

   Clone this project to your local machine:
   ```bash
   git clone https://github.com/your-username/your-repository.git
   cd your-repository
   ```

2. **Create and activate a Python virtual environment**:

    For Windows:
   ```bash
   python -m venv venv
   venv\Scripts\activate 
   ```
    For Mac:
   ```bash
   python3 -m venv venv
   source venv\bin\activate 
   ```

3. **Install backend dependencies**:

    ```bash
    pip install fastapi uvicorn
    pip install pytest httpx
    pip install sqlalchemy databases[sqlite]
    pip install fastapi[all]
    pip install sqlmodel
    pip install alembic
    pip install passlib
    pip install bcrypt
    ```

4. **Navigate to the backend folder**:

    ```bash
    cd backend
    ````

5. **Run backend tests (optional, but recommended to ensure everything is working correctly)**:

    ```bash
    pytest
    ```
    or
    ```bash
    python -m pytest
    ```

6. **Sep up for Alembic (databases)**:

    - To create a migration based on model changes, run:
    ```bash
    alembic revision --autogenerate -m "the reason or changes"
    ```
    For example:
    ```bash
    alembic revision --autogenerate -m "updated user table"
    ```

    - Once you've reviewed the migration script and are confident it's correct, you can apply it to the database with:
    ```bash
    alembic upgrade head
    ```
    Now, you should have a sqlite file called: src/filmhub_database.db

    - If something goes wrong, you can roll back to a previous migration using the downgrade command. For example, to revert to the migration just before the most recent one:
    ```bash
    alembic downgrade -1
    ```
    Now you need to eliminate the last alembic version file, and run again this command:
    ```bash
    alembic upgrade head
    ```

7. **Run the backend server**:

    Start the FastAPI server:
    ```bash
    uvicorn app.main:app --reload
    ```
    The backend will be available at http://localhost:8000.


8. **Deactivate the virtual environment when you're done working on the backend**:

    ```bash
    deactivate
    ```



### **Frontend Setup and Execution (Vue.js)**

1. **Install Vue CLI globally** (if you haven't installed it yet):

   ```bash
   npm install -g @vue/cli
   ````

2. **Navigate to the frontend folder**:

    ```bash
    cd frontend
    ```

3. **Install frontend dependencies**:

    ```bash
    npm install
    npm install axios
    ```

4. **Run the frontend server**:

    Start the Vue.js development server:
    ```bash
    npm run serve
    ```
    The frontend will be available at http://localhost:8080.



### **Final Instructions**

To run the full project:

1. **Start the backend** with FastAPI:
   ```bash
    uvicorn backend.main:app --reload
    ```

2. **Start the frontend with Vue.js**:
    ```bash
    npm run serve
    ```

Now, you should have both the backend running at http://localhost:8000 and the frontend running at http://localhost:8080 on your local machine.