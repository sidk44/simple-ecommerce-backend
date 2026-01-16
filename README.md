# E-Commerce Backend API

High-performance RESTful API for product inventory and shopping cart management built with FastAPI.

## Features

- **Product Management**: Browse product catalog with real-time stock information
- **Shopping Cart**: Add, update, and remove items from cart
- **Checkout**: Process orders with automatic stock deduction
- **Input Validation**: Comprehensive request validation using Pydantic
- **Error Handling**: Detailed error responses for better debugging

## Tech Stack

- **FastAPI**: Modern, fast web framework for building APIs
- **Pydantic**: Data validation and settings management
- **Uvicorn**: Lightning-fast ASGI server

## Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd ecommerce-backend
```

2. Create and activate virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.text
```

## Running the Application

Start the development server:

```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, access:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### Products

- `GET /api/products` - Get all products with ID, name, price, and stock

### Cart

- `POST /api/cart/add` - Add item to cart
- `PUT /api/cart/update` - Update cart item quantity
- `GET /api/cart` - View current cart
- `DELETE /api/cart/clear` - Clear entire cart

### Checkout

- `POST /api/checkout` - Process checkout and create order

## Project Structure

```
ecommerce-backend/
├── main.py           # FastAPI application and route handlers
├── models.py         # Pydantic models for requests/responses
├── services.py       # Business logic and data operations
├── requirements.text # Python dependencies
└── README.md         # Project documentation
```

## Development

This project uses:

- Python 3.x
- FastAPI for API framework
- Uvicorn as ASGI server
- Pydantic for data validation

## License

MIT
