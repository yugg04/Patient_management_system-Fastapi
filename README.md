# 🏥 Carelytics

**Patient Health Intelligence Platform**

Carelytics is a **full-stack healthcare dashboard** built with **FastAPI** that serves both:

* a **modern frontend UI**
* a **RESTful backend API**

from a **single Render deployment**.

This project demonstrates **real-world backend + UI integration**, not a static demo.

---

## 🚀 Live Demo

Try the deployed Carelytics application here:

👉 https://patient-management-system-fastapi-1.onrender.com

## 🚀 Features

### Backend (FastAPI)

* REST API with strict validation
* Full CRUD (Create, Read, Update, Delete)
* BMI auto-calculation
* Health verdict classification
* JSON-based persistence
* Swagger documentation

### Frontend (Served by FastAPI)

* Modern SaaS-style UI
* Light & Dark mode
* Dynamic hover interactions
* Auto-fill update form
* Clean, responsive layout
* Feels like a live product

### Deployment

* Single Render service
* Frontend + backend together
* No external frontend hosting
* No framework lock-in

---

## 🧱 Tech Stack

| Layer      | Technology               |
| ---------- | ------------------------ |
| Backend    | FastAPI                  |
| Frontend   | HTML, CSS, JavaScript    |
| Validation | Pydantic                 |
| Server     | Uvicorn                  |
| Deployment | Render                   |
| Storage    | JSON file (demo purpose) |

---

## 📁 Project Structure

```
carelytics/
│── main.py
│── patients.json
│── requirements.txt
│── static/
│   ├── index.html
│   ├── style.css
│   └── script.js
```

---

## 🧠 Core Logic

### BMI Formula

```
BMI = weight / (height²)
```

### Verdict Rules

| BMI         | Verdict     |
| ----------- | ----------- |
| < 18.5      | Underweight |
| 18.5 – 24.9 | Normal      |
| 25 – 29.9   | Overweight  |
| ≥ 30        | Obese       |

BMI and verdict are **computed automatically** on create/update.

---

## ⚙️ Run Locally

### 1️⃣ Clone Repository

```bash
git clone https://github.com/<your-username>/carelytics.git
cd carelytics
```

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Start Server

```bash
uvicorn main:app --reload
```

### 4️⃣ Open in Browser

```
http://127.0.0.1:8000
```

---

## 🔗 API Endpoints

| Method | Endpoint        | Description                   |
| ------ | --------------- | ----------------------------- |
| GET    | `/`             | Serve frontend UI             |
| GET    | `/view`         | View all patients             |
| GET    | `/patient/{id}` | View one patient              |
| GET    | `/sort`         | Sort by height / weight / BMI |
| POST   | `/create`       | Create patient                |
| PUT    | `/edit/{id}`    | Update patient                |
| DELETE | `/delete/{id}`  | Delete patient                |
| GET    | `/docs`         | Swagger API docs              |

---

## 🧪 Example Request

### Create Patient

```http
POST /create
Content-Type: application/json
```

```json
{
  "id": "P011",
  "name": "John Doe",
  "city": "Delhi",
  "age": 30,
  "gender": "male",
  "height": 1.75,
  "weight": 72
}
```

---

## 🌍 Deployment on Render (Only)

### Render Configuration

| Setting       | Value                                          |
| ------------- | ---------------------------------------------- |
| Runtime       | Python 3                                       |
| Build Command | `pip install -r requirements.txt`              |
| Start Command | `uvicorn main:app --host 0.0.0.0 --port 10000` |

After deployment, your app will be available at:

```
https://carelytics.onrender.com
```

Frontend and backend are served from the **same URL**.



## 👨‍💻 Author

**Yug Khatri**

