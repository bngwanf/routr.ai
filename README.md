# 🖥  Routr.ai


## Project Overview
RoutrProject is a Django-based web application designed to manage trip data, fuel purchase records, and other logistic tasks for truck drivers. It integrates GPT-4 for advanced functionality such as trip report generation based on user inputs.


## Project Structure
The project consists of multiple modules and configurations to handle server operations, API integrations, and application logic. Below is a breakdown of the key components:


### Main Files and Directories
- `manage.py`: Django’s administrative utility to run the application, manage databases, and handle server operations.
- `RoutrProject/`: Main project directory containing configuration and global settings.
  - `asgi.py`: ASGI (Asynchronous Server Gateway Interface) entry-point for asynchronous support.
  - `settings.py`: Django project settings (e.g., database configuration, installed apps, middleware).
  - `urls.py`: URL routing configuration for the entire project.
  - `wsgi.py`: WSGI (Web Server Gateway Interface) entry-point for synchronous applications.
- `RoutrApp/`: Main application module encapsulating the core logic.
  - `admin.py`: Django admin customization for managing project-specific data.
  - `apps.py`: Application configuration details.
  - `models.py`: Data models defining application-specific entities.
  - `tests.py`: Unit tests for application validation.
  - `views.py`: Functions and classes that handle incoming requests and responses.
  - `forms.py`: Custom forms that structure and validate user inputs.
  - `gpt_utils.py`: Utility file for GPT-4 model interactions.
  - `migrations/`: Directory storing Django migrations files for database schema evolution.
- `requirements.txt`: List of dependencies required to run the project.



## 🌐  Django: Framework Overview


### Django Functionality
Django is an MVC-based web framework providing tools to build robust applications.
- **Model**: Handles database abstraction and querying via ORM.
- **View**: Defines response logic and processing user input.
- **Template**: Combines HTML with Django template language for rendering views.

### Django Request-Response Cycle
1. **User Request**: Initiated when a user visits a URL mapped in `urls.py`.
2. **URL Routing**: `urls.py` routes the request to the relevant view.
3. **View Processing**: The view handles processing, using logic or querying models.
4. **Template Rendering**: The view then uses templates to render responses.
5. **Response Sent**: Rendered content is sent as an HTTP response.

### Django Project Settings Highlights
- **INSTALLED_APPS**: Lists modules used by the project, including RoutrApp.
- **MIDDLEWARE**: Includes security and session handling.
- **DATABASES**: Configuration of the database (SQLite in this case).
- **STATIC_URL and STATIC_ROOT**: Manages static files for deployment.


## ⚙ Nginx: Reverse Proxy and Load Balancer


### Nginx Overview
Nginx serves as a high-performance HTTP server, reverse proxy, and load balancer.
- **Reverse Proxy**: Routes client requests to backend services (Gunicorn in this case).
- **Load Balancing**: Distributes incoming traffic to prevent bottlenecks.
- **Static Files**: Efficiently serves static files, reducing load on Django.


### Nginx Configuration
1. **Install Nginx**: `sudo apt install nginx`.
2. **Config File**: Located in `/etc/nginx/sites-available/yourproject`. Point `server_name` to your domain or IP and proxy requests to Gunicorn (`proxy_pass http://127.0.0.1:8000;`).
3. **SSL Configuration**: Use certbot for SSL certificates (required for HTTPS).



## 🐍  Gunicorn: Python Application Server


### Gunicorn Overview
Gunicorn (“Green Unicorn”) is a WSGI-compatible server for Python.
- Efficiently handles Django requests and integrates well with Nginx.
- Scales Django by managing multiple worker processes.

### Gunicorn Setup
1. **Install Gunicorn**: `pip install gunicorn`.
2. **Run Gunicorn**: Start with `gunicorn --workers 3 RoutrProject.wsgi:application`.
3. **Systemd Service**: Create a systemd service file (`/etc/systemd/system/yourproject.service`) and configure Gunicorn to start automatically and restart on failure.



## 🚀  Deployment on DigitalOcean Ubuntu 22.04


### Server Setup
1. **Create Droplet**: Select Ubuntu 22.04 on DigitalOcean.
2. **SSH Access**: `ssh root@your_droplet_ip`.
3. **Update Packages**: `sudo apt update && sudo apt upgrade`.

### Configuring Python and Django
1. **Install Python**: Install Python 3.10 or latest supported.
2. **Create Virtual Environment**: `python3 -m venv venv`.
3. **Install Dependencies**: `pip install -r requirements.txt`.

### Configuring Gunicorn and Nginx
1. **Setup Gunicorn**: Configure Gunicorn as a system service and start it on boot.
2. **Setup Nginx**: Configure Nginx to reverse-proxy requests to Gunicorn and use SSL for secure connections (`sudo certbot --nginx` for HTTPS setup).



## 🧠  GPT Integration (GPT-4 API Calls)


### GPT-4 Utility (gpt_utils.py)
- **Purpose**: Encapsulates interactions with the GPT-4 model for journey data.
- **Client Initialization**: `OpenAICompletionClient` initializes the API client.
- **API Key**: Stored securely (use environment variables for security).
- **send_request Method**: Takes input data, prepares a prompt, and calls GPT-4 API.

### Steps for GPT API Calls in Views
1. **Collect Data**: Extract journey details (e.g., locations, mileage).
2. **API Call**: `client.send_request(data=journey_detail, start_location=start_location, ending_location=ending_location)`.
3. **Parse Response**: Parse JSON to populate the journey and route data.
4. **Render Data**: Send data to templates to display route information.


## 📄  RoutrApp Views and URL Mapping


### Views Overview (views.py)
- **Index**: Renders the main page.
- **driver_trip_record**: Handles driver trip form submissions.
- **fuel_purchase_record**: Manages fuel purchase record creation.
- **report**: Collects journey data and sends it to GPT-4 API.

### URL Patterns (urls.py)
- `/login/`: Login page.
- `/driver_trip_form/`: Form for new driver trip records.
- `/fuel_purchase_form/`: Fuel purchase record form.
- `/report/<trip_id>/`: Generate report with GPT-4 details for a specific trip.


## 📝  Models: Data Representation


### DriverTripRecord Model
- **Attributes**: Date, company, driver name, start/end location, mileage, etc.
- **Functionality**: Stores individual trip details, serving as the main data model.

### FuelPurchaseRecord Model
- **Attributes**: State, gallons, dollar amount, invoice number.
- **Functionality**: Manages fuel purchase records linked to each trip.

### Stop Model
- **Attributes**: Customer name, address, pallets in/out, comments.
- **Functionality**: Tracks each stop within a trip and links back to DriverTripRecord.



## 📊  Forms for Data Input (forms.py)


### DriverTripRecordForm
- **Fields**: Date, company, mileage, start/end time.
- **Validation**: Enforces constraints (e.g., positive mileage).

### FuelPurchaseRecordForm
- **Fields**: State, gallons, dollar amount, invoice number.
- **Validation**: Checks gallons and dollar amount are positive.



## 💻  Testing and Debugging


### Testing Suite (tests.py)
- **Framework**: Django’s `TestCase` for unit tests.
- **Scope**: Test model validation, views, and integration points with GPT API.
- **Goal**: Ensure data integrity and correct API responses.



## 🔒  Security Considerations

### Key Security Features
1. **API Key Management**: Store sensitive keys securely using environment variables.
2. **HTTPS**: Use HTTPS to encrypt data in transit.
3. **Authentication**: CustomUser model with email-based login for added security.


## 🏁  Summary and Key Takeaways


### Summary
RoutrProject is a Django-based web application designed to streamline trip management and fuel purchase tracking for truck drivers. The project utilizes multiple modern technologies to enhance functionality, including GPT-4 integration for automatic report generation, deployment on DigitalOcean using Nginx as a reverse proxy, and Gunicorn for managing application requests. The application captures essential trip and fuel data, organizes it efficiently, and delivers user-friendly outputs, such as PDF reports.


### Key Takeaways
- **Django**: Efficiently manages application logic, routing, and data handling via its MVC architecture.
- **Gunicorn**: Functions as a robust Python application server, efficiently handling user requests.
- **Nginx**: Acts as a reverse proxy, offering enhanced security and scalability by distributing traffic and managing static files.
- **DigitalOcean Deployment**: Setting up a DigitalOcean droplet with Nginx and Gunicorn provides a scalable, secure environment for application hosting.
- **GPT Integration**: The application integrates GPT-4 via API calls in `gpt_utils.py` to automate the generation of trip reports, enhancing the user experience with AI-powered functionality.

---



# MIT License

## Copyright (c) 2024 Brendan Ngwa Nforbi

### Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

- The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

### THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.