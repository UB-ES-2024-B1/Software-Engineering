
### **Frontend Setup and Execution (Vue.js)**

1. **Install Vue CLI globally** (if you haven't installed it yet):

   ```bash
   cd src
   npm install -g @vue/cli
   ````

2. **Navigate to the frontend folder**:

    ```bash
    cd filmHub
    ```

3. **Install frontend dependencies**:

    For Windows:
    ```bash
    npm install
    npm install axios
    npm install flatpickr
    ```

    For Mac:
    ```bash
    sudo npm install
    sudo npm install axios
    sudo npm install flatpickr
    ```

4. **Run the frontend server**:

    Start the Vue.js development server:

    For Windows:
    ```bash
    npm run serve
    ```

    For Mac:
    ```bash
    sudo npm run serve
    ```
    The frontend will be available at http://localhost:8080.


### Frontend quick start 

    For Windows:
    ```bash
    cd src/filmHub
    npm run serve
    ```

    For Mac:
    ```bash
    cd src/filmHub
    sudo npm run serve
    ```

### Compiles and minifies for production
```
npm run build
```

### Lints and fixes files
```
npm run lint
```

### Customize configuration
See [Configuration Reference](https://cli.vuejs.org/config/).

### **About docker**
Start frontend:
    Delete dist/
    cd src/filmHub
    npm run build
    docker buildx build --platform linux/amd64 -t mayeteco7/filmhub-frontend:latest .
    docker push mayeteco7/filmhub-frontend
    Deploy in Azure


Start backend:
    cd src/backend
    docker buildx build --platform linux/amd64 -t mayeteco7/filmhub-backend:latest .
    docker push mayeteco7/filmhub-backend
    Deploy in Azure