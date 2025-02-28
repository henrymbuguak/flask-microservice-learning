
# **User Management Microservice with Flask and SQLAlchemy**  

Welcome to the **User Management Microservice Tutorial Series**! This guide walks you through building a **production-ready microservice** using **Flask** and **SQLAlchemy**. Each part of the series focuses on a different aspect, from setting up the project to deploying it with Docker.  

---

## **1. Features**  
✅ User registration and authentication with JWT  
✅ Full CRUD operations for managing users  
✅ Error handling and input validation  
✅ Logging and monitoring  
✅ Unit testing with `pytest`  
✅ Containerization with Docker  

---

## **2. Prerequisites**  
Ensure you have the following installed before running the project:  

- **Python 3.8+**  
- **pip (Python package manager)**  
- **Docker (optional for containerization)**  

---

## **3. Getting Started**  

### **Clone the Repository**  
```bash
git clone https://github.com/henrymbuguak/flask-microservice-learning.git
cd flask-microservice-learning
```

### **Install Dependencies**  
```bash
pip install -r requirements.txt
```

### **Run the Application**  

```bash
cd user_management_microservice
python run.py
```

By default, the service runs on `http://127.0.0.1:5000/`.  

---

## **4. API Endpoints**  

### **Log in to Get a JWT Token**  
```bash
curl -X POST -H "Content-Type: application/json" -d '{"username": "testuser", "password": "testpass"}' http://127.0.0.1:5000/api/login
```

### **Fetch All Users**  
```bash
curl -H "Authorization: Bearer <your-access-token>" http://127.0.0.1:5000/api/users
```

### **Fetch a Single User**  
```bash
curl -H "Authorization: Bearer <your-access-token>" http://127.0.0.1:5000/api/users/1
```

### **Update a User**  
```bash
curl -X PUT -H "Authorization: Bearer <your-access-token>" -H "Content-Type: application/json" -d '{"username": "updateduser"}' http://127.0.0.1:5000/api/users/1
```

### **Delete a User**  
```bash
curl -X DELETE -H "Authorization: Bearer <your-access-token>" http://127.0.0.1:5000/api/users/1
```

---

## **5. Running with Docker**  

### **Build the Docker Image**  
```bash
docker build -t user_management_microservice .
```

### **Run the Container**  
```bash
docker run -p 8080:5000 user_management_microservice
```

Once running, access the API at `http://127.0.0.1:8080/`.  

---

## **6. Tutorial Series**  

This project is part of a **seven-part tutorial series** that covers everything from setting up the microservice to deploying it.  

1. **[Introduction to the User Management Microservice](https://www.blog.hlab.tech/build-a-production-ready-user-management-microservice-with-flask-and-sqlalchemy-a-step-by-step-guide/)**  
2. **[User Registration & Database Models](https://www.blog.hlab.tech/part-2-user-registration-and-database-models-building-the-foundation-of-your-microservice/)**  
3. **[CRUD Operations & JWT Authentication](https://www.blog.hlab.tech/part-3-completing-crud-operations-with-jwt-authentication-securing-your-microservice/)**  
4. **[Error Handling & Input Validation](https://www.blog.hlab.tech/part-4-error-handling-and-input-validation-making-your-microservice-robust-and-user-friendly/)**  
5. **[Logging & Monitoring](https://www.blog.hlab.tech/part-5-logging-and-monitoring-tracking-requests-and-performance-in-your-microservice/)**  
6. **[Unit Testing with Pytest](https://www.blog.hlab.tech/part-6-unit-testing-your-microservice-ensuring-reliability-and-stability-with-pytest/)**  
7. **[Containerization with Docker](https://www.blog.hlab.tech/part-7-containerizing-your-microservice-with-docker/)**  

---

## **7. Contribution**  

Feel free to **fork the repository** and submit a pull request if you’d like to contribute. For major changes, please open an issue first to discuss them.  

---

## **8. License**  
This project is licensed under the **MIT License**.  

---

### 🔥 **Next Steps**  
Want to learn more? Follow the tutorial series or try deploying the microservice to a **cloud provider**!  

---
