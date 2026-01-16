from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from typing import List

from models import (
    Product,
    AddToCartRequest,
    UpdateCartRequest,
    CartResponse,
    CheckoutResponse,
    SuccessResponse,
    ErrorResponse
)
import services


app = FastAPI(
    title="E-Commerce API",
    description="High-performance RESTful API for product inventory and shopping cart management",
    version="1.0.0"
)


@app.get("/api/products", response_model=List[Product])
def get_products():
    """
    Retrieve all products with ID, Name, Price, and current Stock Quantity.
    """
    try:
        products = services.get_all_products()
        return products
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@app.post("/api/cart/add", response_model=SuccessResponse)
def add_to_cart(request: AddToCartRequest):
    """
    Add an item to the cart.
    If product already exists in cart, increases quantity (idempotent).
    Validates stock availability before adding.
    """
    try:
        result = services.add_to_cart(request.productId, request.quantity)
        return result
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@app.patch("/api/cart/update", response_model=SuccessResponse)
def update_cart(request: UpdateCartRequest):
    """
    Update item quantity in the cart to the specified amount.
    Set quantity to 0 to remove item from cart.
    Validates stock availability before updating.
    """
    try:
        result = services.update_cart(request.productId, request.quantity)
        return result
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@app.get("/api/cart", response_model=CartResponse)
def get_cart():
    """
    View cart contents including:
    - List of items with product details and subtotals
    - Total item count
    - Total price
    """
    try:
        cart = services.get_cart()
        return cart
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@app.post("/api/cart/checkout", response_model=CheckoutResponse)
def checkout():
    """
    Finalize the order with atomic stock validation and inventory update.
    
    Process:
    1. Validates all items have sufficient stock
    2. If validation passes: reduces inventory and clears cart
    3. If any item fails validation: entire checkout fails (no changes made)
    
    This is an all-or-nothing operation ensuring data consistency.
    """
    try:
        result = services.checkout()
        return result
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


# Optional: Root endpoint for API info
@app.get("/")
def root():
    """API root endpoint with basic information."""
    return {
        "message": "E-Commerce API",
        "version": "1.0.0",
        "endpoints": {
            "products": "/api/products",
            "cart_add": "/api/cart/add",
            "cart_update": "/api/cart/update",
            "cart_view": "/api/cart",
            "checkout": "/api/cart/checkout"
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
