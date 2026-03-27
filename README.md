# Shelf Analyzer API

This project is a simple API that analyzes a shelf layout and identifies the shape and position of different product groups.
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
http://localhost:8000/api/shelf/analyze/

---

### Run using Docker

```bash
docker-compose up --build
```

---

## API Endpoint

### POST `/api/shelf/analyze/`

### Request

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

### Response

```json
{
  "G": { "shape": "square", "location": "top left" },
  "M": { "shape": "square", "location": "top right" },
  "B": { "shape": "square", "location": "bottom left" },
  "N": { "shape": "square", "location": "bottom right" }
}
```

---

## Implementation Guide

The solution follows a straightforward approach:

* The grid is scanned and cells are grouped by brand
* For each brand, a bounding box is calculated using min and max row/column
* Height and width of the box are used to determine the shape:

  * if all cells fill the box → rectangle or square
  * otherwise → polygon
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
curl -X POST http://localhost:8000/api/shelf/analyze/ \
-H "Content-Type: application/json" \
-d '{ "layout": [...] }'
```

---


## Author

AGHOSH PR
