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
4. Access the frontend at [http://localhost:8080/](http://localhost:8080/)
5. Access the backend at [http://localhost:8000/](http://localhost:8000/)

### Additional features
1. Implemented marker clustering in Google Maps, because the properties are often grouped very close together
2. Implemented a Vueform design with range sliders for a better user experience when filtering property area and market value
3. Implemented a small pytest suite with 10 tests to validate API endpont functionality such as HTTP authentication and filter pattern validation
4. Implemented a Property Details page that lists all property information and a Google Maps map. Navigation is done via links in the Maps marker tooltip and the Property list table 
5. Implemented a Collapsible component to group the page elements and improve UX on mobile

### Optimization
1. In order to optimize the application performance when the data scales, my intuition is to use Geo database extensions to create a spatial data index
2. This will enable us to create an endpoint that can return properties within a radius of a location, or within the Google Maps viewport. That way we can load property markers on demand
3. We can also add a feature to the Property details view that shows properties that are nearby the currently viewed property
4. To implement this I would use the [GeoAlchemy 2 Extension to SQLAlchemy that uses the SpatiaLite SQLite module](https://geoalchemy-2.readthedocs.io/en/0.14.3/spatialite_tutorial.html)