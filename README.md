# Campus Connect – Campus HelpDesk & Lost/Found Portal

Campus Connect is a Django-based university support web application developed for COMP-8347 – Internet Applications and Distributed Systems at the University of Windsor.

The project provides one centralized platform where students can report lost or found items, submit campus helpdesk issues, upload supporting files, search public reports, track status updates, and view announcements.

## Tech Stack

* Python
* Django
* SQLite
* Bootstrap
* HTML
* CSS
* JavaScript
* JSON Fixtures

## Main Features

* Public homepage with live report statistics
* User registration, login, logout, and password recovery
* User profile page and profile update feature
* Helpdesk ticket submission
* Lost and found item reporting
* File, image, and document uploads
* Public report browsing
* Keyword search by title, description, and location
* Dropdown filters by report type, status, item type, and category
* Report detail pages
* My Reports page for registered users
* Edit-own-report functionality
* Permission protection for report editing
* Comments on ticket and lost/found detail pages
* Admin/staff status update workflow
* Status history tracking
* Announcements managed from Django admin
* Recent resolved/claimed updates
* User history using sessions and cookies
* Recently viewed reports
* Recent search keyword tracking
* Minimum API endpoint using Django JsonResponse
* Responsive Bootstrap design with hover effects

## Database

The project uses SQLite, Django’s default relational SQL database.

Main models include:

* UserProfile
* Category
* Ticket
* LostFoundItem
* Comment
* StatusUpdate
* Announcement

## API Endpoint

The project includes a small API endpoint:

```text
/api/report-stats/
```

It returns live report statistics in JSON format, including total reports, tickets, lost/found items, and status counts.

## Installation and Setup

Create and activate a virtual environment:

```powershell
python -m venv .venv
.venv\Scripts\activate
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

Run migrations:

```powershell
python manage.py migrate
```

Load initial data:

```powershell
python manage.py loaddata initial_data
```

Create a superuser:

```powershell
python manage.py createsuperuser
```

Run the development server:

```powershell
python manage.py runserver
```

Open the project:

```text
http://127.0.0.1:8000/
```

## Admin Panel

Django admin is available at:

```text
http://127.0.0.1:8000/admin/
```

Admin/staff can manage categories, tickets, lost/found reports, announcements, comments, and status updates.

## Project Purpose

Students often face issues such as lost belongings, IT problems, classroom issues, or facility requests, but reporting and tracking these problems can be scattered and slow. Campus Connect provides a simple organized system where students can submit reports, upload supporting files, search existing reports, and track progress from one place.

## Developer

Romit Patel
Master of Applied Computing
University of Windsor
