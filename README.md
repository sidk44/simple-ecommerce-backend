<div align="center">
  <img src="https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png" alt="FastAPI" width="400"/>
  
  # E-Commerce Backend API
  
  ![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
  ![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
  ![Pydantic](https://img.shields.io/badge/Pydantic-E92063?style=for-the-badge&logo=pydantic&logoColor=white)
  
  RESTful API for product inventory and shopping cart management
  
</div>

---

##  Features

-  Product catalog with real-time stock tracking
-  Shopping cart management (add, update, remove)
-  Checkout processing with automatic inventory updates
-  Input validation with Pydantic
-  High-performance async endpoints

##  Tech Stack

**FastAPI** · **Python 3.x** · **Pydantic** · **Uvicorn**

##  Quick Start

```bash
# Clone and navigate
git clone <repository-url>
cd ecommerce-backend

# Setup virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.text

# Run server
uvicorn main:app --reload
```

**API Docs:** [http://localhost:8000/docs](http://localhost:8000/docs) · [ReDoc](http://localhost:8000/redoc)

##  API Endpoints

| Method   | Endpoint           | Description          |
| -------- | ------------------ | -------------------- |
| `GET`    | `/api/products`    | List all products    |
| `POST`   | `/api/cart/add`    | Add item to cart     |
| `PUT`    | `/api/cart/update` | Update cart quantity |
| `GET`    | `/api/cart`        | View cart            |
| `DELETE` | `/api/cart/clear`  | Clear cart           |
| `POST`   | `/api/checkout`    | Process order        |

##  Project Structure

```
├── main.py           # FastAPI app & routes
├── models.py         # Pydantic models
├── services.py       # Business logic
└── requirements.text # Dependencies
```

---

<div align="center">
  Built with ❤️ using FastAPI
</div>
