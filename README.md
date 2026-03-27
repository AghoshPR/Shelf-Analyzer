# Shelf Analyzer API

This project provides an API that analyzes a shelf layout and identifies the shape and position of different product groups.
It is based on a retail use case where products are arranged on shelves and need to be analyzed automatically.

---

## Tech Stack

* Python 3
* Django
* Django REST Framework
* Docker
* Docker Compose

---

## Setup and Run

### Run locally

```bash
pip install -r requirements.txt
python manage.py runserver
```

Open:
http://localhost:8000/

---

### Run using Docker

```bash
docker-compose up --build
```

---

## API Endpoint

`POST /`

---

## Request

```json
{
  "layout": [
    ["G","G","M","M"],
    ["G","G","M","M"],
    ["B","B","N","N"],
    ["B","B","N","N"]
  ]
}
```

---

## Response

```json
{
  "G": { "shape": "square", "location": "top left" },
  "M": { "shape": "square", "location": "top right" },
  "B": { "shape": "square", "location": "bottom left" },
  "N": { "shape": "square", "location": "bottom right" }
}
```

---

## Project Structure

```bash
shelfAnalyzer/
│
├── shelf/                     # Core app (business logic)
│   ├── migrations/
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py              # Shelf analysis logic
│
├── shelfAnalyzer/            # Project configuration
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py               # Root routing
│   └── wsgi.py
│
├── Dockerfile                # Container setup
├── docker-compose.yml        # Multi-container config
├── manage.py                 # Django entry point
├── requirements.txt          # Dependencies
├── .dockerignore
├── .gitignore
└── README.md
```

---

## Implementation Guide

The solution follows a straightforward approach:

* The grid is scanned and cells are grouped by brand
* For each brand, a bounding box is calculated using min and max row/column
* Height and width of the box are used to determine the shape:

  * If all cells fill the box → rectangle or square
  * Otherwise → polygon
* Based on the position of the box in the grid, the location is assigned (top, middle, bottom, left, right)

---

## Test Cases

### Case 1 – Vertical Rectangles

```json
{
  "layout": [
    ["G","M","N","B"],
    ["G","M","N","B"],
    ["G","M","N","B"],
    ["G","M","N","B"]
  ]
}
```

Expected:

* All brands → vertical rectangle

---

### Case 2 – Squares

```json
{
  "layout": [
    ["G","G","M","M"],
    ["G","G","M","M"],
    ["B","B","N","N"],
    ["B","B","N","N"]
  ]
}
```

Expected:

* All brands → square with correct positions

---

### Case 3 – Mixed Shapes

```json
{
  "layout": [
    ["G","G","G","M","M","M","M"],
    ["G","B","G","M","N","N","M"],
    ["G","G","G","M","N","N","M"],
    ["B","B","B","B","B","N","N"]
  ]
}
```

Expected:

* G → polygon
* M → polygon
* B → horizontal rectangle
* N → polygon

---

## How to Test

You can test the API using:

* Postman / Thunder Client
* Django REST Framework UI
* curl:

```bash
curl -X POST http://localhost:8000/ \
-H "Content-Type: application/json" \
-d '{
  "layout": [
    ["G","G","M","M"],
    ["G","G","M","M"],
    ["B","B","N","N"],
    ["B","B","N","N"]
  ]
}'
```

---

## Author

AGHOSH PR
