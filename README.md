# 🐍 Flask MongoDB CRUD App (Dockerized)

This is a simple **CRUD (Create, Read, Update, Delete)** web application built using:

- **Flask** for backend
- **MongoDB** for database
- **Jinja2** for templates
- **Docker & Docker Compose** for containerization

---

## 🔧 Features

✅ Add New Users  
✅ Update Existing Users  
✅ Delete Users  
✅ View All Users  
✅ RESTful JSON API + Jinja Templates  
✅ Passwords are hashed using `werkzeug.security`  
✅ Fully Dockerized  

---

## 📦 Technologies Used

- Python 3
- Flask
- Flask-PyMongo
- MongoDB
- Docker
- Jinja2
- Bootstrap (for styling templates)

---

## 🚀 Getting Started (with Docker)

### Prerequisites

- Docker & Docker Compose installed  
[Install Docker Desktop](https://www.docker.com/products/docker-desktop/)

---

### 📂 Project Structure

crud_flask/
│
├── app/
│ ├── init.py
│ ├── config.py
│ ├── routes/
│ │ └── users.py
│ └── templates/
│ ├── index.html
│ ├── add_user.html
│ └── update_user.html
│
├── run.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── .gitignore