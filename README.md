# Library Management System

This is a Library Management System built using **Django** and **Django REST Framework**. It allows users to browse and review books and see their borrowing, while **librarians** manage borrowing and books inventory. **Admins** have full control over the system including changing user roles.

## Features
- Browse books and post reviews
- Admin and Librarian roles to manage the system
- Secure API access with role-based control
- Dockerized for easy setup and deployment

## Roles and Permissions
### Admin
- Full control over the system
- Can update the user details and assign roles

### Librarian
- Manage books and authors
- Borrow books on the behalf of users (for security purpose)

### User
- Register/Login
- Browse books and reviews
- Submit reviews on books

> Users **cannot** borrow books themselves. Only librarians can borrow books for them.


## Setup and Instructions

### 1. Clone the Repository

To get started, first clone the repository to your local machine:

```bash
https://github.com/pratima-dawadi/library-management-system.git
cd library-management-system
```

### 2. Add environment variables
Create a .env file based on the provided sample-env file:

```bash
cp sample-env .env
```
Then edit `.env` accordingly


### 3. Build and start the container

To build and run the container run following command:

```bash
docker compose up --build
```
> **Note**: Use docker-compose (with hyphen) if you're using an older version of Docker.

Access the api documentation on [localhost:8050/api-docs/](http://localhost:8050/api-docs/)

### 4. Seed initial data
Once docker container is started, open new terminal and run following command to seed the data:
```bash
docker compose exec web python manage.py seed_data
```
> This will populate:
>- An Admin account
>- A Librarian account
>- List of books and authors

## Login Credentials

| Role      | Email                 | Password   |
|-----------|-----------------------|------------|
| Admin     | `admin@gmail.com`     | `admin123` |
| Librarian | `librarian@gmail.com` | `lib123`   |

> To create your own superuser (admin), run the following command and follow the prompts:
```bash
docker compose exec web python manage.py createsuperuser
```
> You can register yourself as a **user** and later change role to librarian via admin login.

To be a normal user, register first and then log in. After logging in, you can access protected endpoints using your access token.