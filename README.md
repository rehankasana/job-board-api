# Job Board API

A RESTful Job Board API built with Django and Django REST Framework. The platform supports separate Applicant and Recruiter roles, job management, applicant profiles, resume uploads, job applications, and application status management.

## Features

* JWT-based authentication
* Applicant and Recruiter user roles
* Applicant profile management
* Resume upload and validation
* Job creation, updating, and deletion
* Job search by title, company, location, skills, and description
* Job filtering by employment type and location
* Job ordering by creation date, salary, and deadline
* Pagination for job listings and applications
* Job application submission
* Duplicate application prevention
* Resume required before applying
* Applicant application history
* Recruiter received applications
* Application status management
* Role-based permissions
* Django Admin interface
* Automated tests using PyTest

## Technologies

* Python
* Django
* Django REST Framework
* Simple JWT
* django-filter
* PyTest
* SQLite
* Local media storage

## Project Structure

```text
job-board-api/
│
├── accounts/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
│
├── jobs/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
│
├── applications/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
│
├── config/
│   ├── settings.py
│   └── urls.py
│
├── tests/
│   ├── test_accounts.py
│   ├── test_jobs.py
│   └── test_applications.py
│
├── manage.py
├── pytest.ini
├── requirements.txt
└── .gitignore
```

## API Endpoints

### Authentication

| Method | Endpoint              | Description                          |
| ------ | --------------------- | ------------------------------------ |
| POST   | `/api/auth/register/` | Register a new user                  |
| POST   | `/api/auth/login/`    | Obtain JWT access and refresh tokens |
| POST   | `/api/auth/refresh/`  | Refresh an access token              |

### Applicant Profile

| Method    | Endpoint                           | Description              |
| --------- | ---------------------------------- | ------------------------ |
| GET       | `/api/auth/profile/`               | View applicant profile   |
| PUT/PATCH | `/api/auth/profile/`               | Update applicant profile |
| POST      | `/api/auth/profile/resume/`        | Upload resume            |
| GET       | `/api/auth/profile/resume/detail/` | View resume information  |
| DELETE    | `/api/auth/profile/resume/detail/` | Delete resume            |

### Jobs

| Method    | Endpoint          | Description                 |
| --------- | ----------------- | --------------------------- |
| GET       | `/api/jobs/`      | List active jobs            |
| POST      | `/api/jobs/`      | Create a job as a recruiter |
| GET       | `/api/jobs/<id>/` | View a job                  |
| PUT/PATCH | `/api/jobs/<id>/` | Update own job              |
| DELETE    | `/api/jobs/<id>/` | Delete own job              |

### Applications

| Method | Endpoint                         | Description                             |
| ------ | -------------------------------- | --------------------------------------- |
| POST   | `/api/applications/`             | Apply for a job                         |
| GET    | `/api/applications/my/`          | View applicant's applications           |
| GET    | `/api/applications/received/`    | View applications received by recruiter |
| PATCH  | `/api/applications/<id>/status/` | Update application status               |
| GET    | `/api/applications/<id>/`        | View an application                     |
| DELETE | `/api/applications/<id>/`        | Delete an application                   |

## Job Search and Filtering

The job listing endpoint supports search, filtering, ordering, and pagination.

### Search

```text
GET /api/jobs/?search=django
```

Searches across:

* Job title
* Company
* Location
* Skills
* Description

### Filter by employment type

```text
GET /api/jobs/?employment_type=FULL_TIME
```

### Filter by location

```text
GET /api/jobs/?location=Faisalabad
```

### Ordering

```text
GET /api/jobs/?ordering=-created_at
```

Other supported ordering fields include:

```text
created_at
salary_min
salary_max
deadline
```

### Pagination

```text
GET /api/jobs/?page=2&page_size=5
```

## Application Status

Recruiters can manage applications using the following statuses:

* APPLIED
* REVIEWING
* SHORTLISTED
* REJECTED
* HIRED

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/job-board-api.git
cd job-board-api
```

Replace `YOUR-USERNAME` with your GitHub username.

### 2. Create a virtual environment

Windows:

```powershell
python -m venv venv
```

Activate it:

```powershell
venv\Scripts\activate
```

### 3. Install dependencies

```powershell
pip install -r requirements.txt
```

### 4. Apply migrations

```powershell
python manage.py migrate
```

### 5. Run the development server

```powershell
python manage.py runserver
```

The API will be available at:

```text
http://127.0.0.1:8000/
```

## Running Tests

Run the complete test suite:

```powershell
pytest
```

The project currently contains automated tests covering authentication, job management, applications, permissions, and application workflows.

## Authentication

The API uses JWT authentication.

After logging in, the API returns an access token and refresh token.

Use the access token in protected requests:

```text
Authorization: Bearer <access_token>
```

## Example User Roles

### Applicant

Applicants can:

* Create and update their profile
* Upload a resume
* Browse jobs
* Search and filter jobs
* Apply for jobs
* View their applications

### Recruiter

Recruiters can:

* Create jobs
* Update their own jobs
* Delete their own jobs
* View applications received for their jobs
* Update application statuses

## Development

This project was developed as a backend-focused Django REST Framework application to demonstrate REST API development, authentication, authorization, data modeling, file handling, filtering, pagination, and automated testing.

## License

This project is for educational and portfolio purposes.
