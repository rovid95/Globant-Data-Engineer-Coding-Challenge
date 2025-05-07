# 📦 DB Migration API – CSV to SQL REST Interface

A local REST API built with **FastAPI** that supports **CSV ingestion** and **batch inserts** into a relational SQL database. This API is part of a database migration use case involving three core tables: `departments`, `jobs`, and `employees`.

## 🧠 Project Purpose

This project was created as part of a **Data Engineer coding challenge** to:

- Accept historical data from CSV files
- Ingest and validate up to 1000 rows per upload
- Persist the data into a relational database
- Demonstrate modular REST API design with FastAPI and SQLAlchemy
- Show development process via version control

## 📂 Project Structure

```
db_migration_api/
├── data/                  # Contains sample CSV files
│   ├── departments.csv
│   ├── jobs.csv
│   └── employees.csv
├── routers/               # API endpoints (modular routers)
│   ├── departments.py
│   ├── jobs.py
│   └── employees.py
├── models.py              # SQLAlchemy models (table structure)
├── schemas.py             # Pydantic schemas (data validation)
├── database.py            # Database configuration (SQLite engine)
├── main.py                # FastAPI app initialization
├── requirements.txt       # Python dependencies
└── README.md              # You're reading it
```

## ⚙️ Tech Stack

- **FastAPI** – modern, high-performance web framework
- **Uvicorn** – lightning-fast ASGI server
- **SQLAlchemy** – ORM for defining database models
- **SQLite** – simple SQL database for local use
- **Pandas** – reading and transforming CSV data
- **Pydantic** – data validation for requests

## 🚀 Getting Started

### ✅ Prerequisites

- Python 3.9+
- pip
- PyCharm (optional but recommended)

### 📥 Installation

```bash
# Clone the repo
git clone https://github.com/rovid95/Globant-Data-Engineer-Coding-Challenge.git
cd db-migration-api

# Install dependencies
pip install -r requirements.txt
```

## ▶️ Running the API

```bash
uvicorn main:app --reload
```

Open Swagger UI at:
```
http://localhost:8000/docs
```

## 📁 Sample CSV Files

### `departments.csv` (no header)
```csv
1,HR
2,Finance
3,Marketing
4,Engineering
5,Sales
```

### `jobs.csv` (no header)
```csv
1,Data Engineer
2,Data Analyst
3,HR Manager
4,Software Developer
5,Sales Representative
```

### `employees.csv` (no header)
```csv
1,John Doe,2021-01-15,1,3
2,Jane Smith,2022-03-10,2,2
3,Alice Johnson,2020-07-20,3,1
4,Bob Williams,2023-01-05,4,4
5,Eva Martinez,2022-10-10,5,5
```

## 📡 API Endpoints

### 🔹 Departments
| Method | Path                         | Description                        |
|--------|------------------------------|------------------------------------|
| POST   | `/departments/upload_csv/`   | Upload historical data via CSV     |
| POST   | `/departments/batch_insert/` | Insert up to 1000 rows via JSON    |
| GET    | `/departments/all/`          | View all department records        |
| DELETE | `/departments/clear/`        | Clear all department records       |

### 🔹 Jobs
| Method | Path                     | Description                        |
|--------|--------------------------|------------------------------------|
| POST   | `/jobs/upload_csv/`      | Upload historical job data via CSV|
| POST   | `/jobs/batch_insert/`    | Insert up to 1000 jobs via JSON    |
| GET    | `/jobs/all/`             | View all job records               |
| DELETE | `/jobs/clear/`           | Clear all job records              |

### 🔹 Employees
| Method | Path                        | Description                        |
|--------|-----------------------------|------------------------------------|
| POST   | `/employees/upload_csv/`    | Upload employee data via CSV       |
| POST   | `/employees/batch_insert/`  | Insert up to 1000 employees via JSON |
| GET    | `/employees/all/`           | View all employee records          |
| DELETE | `/employees/clear/`         | Clear all employee records         |

## 🛡 Data Validation & Constraints

- All upload endpoints **limit batch size to 1000** records.
- CSVs without headers are handled using manual column mapping.
- String cleanup and encoding normalization included (`utf-8-sig`).
- Employee table uses **foreign keys**: `department_id` and `job_id`.

## 🧪 Testing via Swagger UI

1. Visit `http://localhost:8000/docs`
2. Expand an endpoint (e.g., `/jobs/upload_csv/`)
3. Click **"Try it out"**
4. Upload a CSV file (from `data/` folder)
5. Click **Execute**

Expected response:
```json
{
  "message": "CSV data uploaded",
  "rows_inserted": 5
}
```

## ✅ Version Control & Commits

Frequent commits are made to:
- Track iterative development
- Highlight incremental improvements
- Make it easy to review and revert changes

Example commits:
```
feat: add jobs router with CSV upload
fix: clean whitespace from job_name
refactor: move DB session to common function
docs: add sample CSV files
```

## 📌 License

This project is for demonstration purposes and is not currently under an open-source license.

## 🙋‍♂️ Author

**Ronald Solórzano**  
[LinkedIn](https://www.linkedin.com/in/ronald-solorzano-dn2895/) • [GitHub](https://github.com/rovid95)

## 📬 Contact

Have questions? Feel free to open an issue or contact me via GitHub.