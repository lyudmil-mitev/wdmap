# W&D Property Browser

### Introduction 
This is an implementation of the [Full-Stack Challenge](https://github.com/enodoscore/fullstack-challenge).
I have chosen to use FastAPI, SQLite, pytest, Vue.js version 3, vue-router, Vueforms and the Google Maps API

### Authentication
Authentication is implemented and hardcoded server-side via HTTP Basic Authentication. The Vue.js application will store the username and password in SessionStorage.

### Database design and implementation 
I converted the Excel file to CSV and wrote a script that ingests it into a SQLite database file. The backend uses a SQLAlchemy ORM model that includes all fields from the Excel file.

### Backend framework
I have chosen the FastAPI framework, SQLAlchemy and Vue.js version 3 because they apply well to the task and I learned that this is the stack used at B&W. I have implemented endpoint tests via pytest.

### Frontend framework
Frontend is implemented via Vue.js, vue-router, Google Maps Api and Vueform for the filter controls.
NOTE: Please provide your own Google Maps Api key in the ./frontend/.env file:
```VITE_GOOGLE_MAPS_API_KEY="your-key-here"```

### Setup
1. Make sure you have docker and docker-compose installed
2. Create the file `frontend/.env` and set your Google Maps Api key in the variable `VITE_GOOGLE_MAPS_API_KEY`
3. Execute `run.sh`
