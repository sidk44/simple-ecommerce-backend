from pydantic import BaseModel, Field
from typing import List


class Product(BaseModel):
    """Product model for inventory."""
    id: int
    name: str
    price: float
    stock: int


class AddToCartRequest(BaseModel):
    """Request model for adding items to cart."""
    productId: int = Field(..., description="Product ID to add to cart")
    quantity: int = Field(..., gt=0, description="Quantity to add (must be > 0)")


class UpdateCartRequest(BaseModel):
    """Request model for updating cart item quantity."""
    productId: int = Field(..., description="Product ID to update")
    quantity: int = Field(..., ge=0, description="New total quantity (0 to remove)")


class CartItem(BaseModel):
    """Cart item with product details and subtotal."""
    product_id: int
    name: str
    price: float
    quantity: int
    subtotal: float


class CartResponse(BaseModel):
    """Response model for cart contents."""
    items: List[CartItem]
    total_items: int
    total_price: float


class CheckoutResponse(BaseModel):
    """Response model for successful checkout."""
    success: bool
    message: str
    order_summary: dict


class SuccessResponse(BaseModel):
    """Generic success response."""
    success: bool
    message: str


class ErrorResponse(BaseModel):
    """Error response model."""
    error: str
