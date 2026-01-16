from threading import Lock
from typing import Dict, List, Optional


# In-memory data stores
products_db: Dict[int, Dict] = {
    101: {"id": 101, "name": "Laptop Charger", "price": 75.00, "stock": 5},
    102: {"id": 102, "name": "Wireless Mouse", "price": 25.00, "stock": 10},
    103: {"id": 103, "name": "USB-C Hub", "price": 40.00, "stock": 2},
    104: {"id": 104, "name": "Monitor Stand", "price": 50.00, "stock": 15},
}

# Cart storage: {product_id: quantity}
cart_db: Dict[int, int] = {}

# Thread lock for thread-safe operations
inventory_lock = Lock()


def get_all_products() -> List[Dict]:
    """Retrieve all products with current stock information."""
    with inventory_lock:
        return list(products_db.values())


def add_to_cart(product_id: int, quantity: int) -> Dict:
    """
    Add item to cart (idempotent - increases quantity if exists).
    Validates stock availability before adding.
    
    Returns: {"success": True, "message": str} or raises ValueError
    """
    if quantity <= 0:
        raise ValueError("Quantity must be greater than 0")
    
    with inventory_lock:
        # Check if product exists
        if product_id not in products_db:
            raise ValueError(f"Product with ID {product_id} not found")
        
        product = products_db[product_id]
        current_cart_quantity = cart_db.get(product_id, 0)
        new_total_quantity = current_cart_quantity + quantity
        
        # Validate stock availability
        if new_total_quantity > product["stock"]:
            raise ValueError(
                f"Insufficient stock for {product['name']}. "
                f"Available: {product['stock']}, Requested: {new_total_quantity}"
            )
        
        # Add/update cart (idempotent)
        cart_db[product_id] = new_total_quantity
        
        return {
            "success": True,
            "message": f"Added {quantity} x {product['name']} to cart"
        }


def update_cart(product_id: int, quantity: int) -> Dict:
    """
    Update item quantity in cart to specified amount.
    If quantity is 0, removes item from cart.
    
    Returns: {"success": True, "message": str} or raises ValueError
    """
    if quantity < 0:
        raise ValueError("Quantity cannot be negative")
    
    with inventory_lock:
        # Check if product exists in inventory
        if product_id not in products_db:
            #same as if 'key' in hashmap/dict
            raise ValueError(f"Product with ID {product_id} not found")
        
        # Check if product exists in cart
        if product_id not in cart_db:
            raise ValueError(f"Product with ID {product_id} not in cart")
        
        product = products_db[product_id]
        
        # If quantity is 0, remove from cart
        if quantity == 0:
            del cart_db[product_id]
            return {
                "success": True,
                "message": f"Removed {product['name']} from cart"
            }
        
        # Validate stock availability
        if quantity > product["stock"]:
            raise ValueError(
                f"Insufficient stock for {product['name']}. "
                f"Available: {product['stock']}, Requested: {quantity}"
            )
        
        # Update cart
        cart_db[product_id] = quantity
        
        return {
            "success": True,
            "message": f"Updated {product['name']} quantity to {quantity}"
        }


def get_cart() -> Dict:
    """
    Get cart contents with calculated totals.
    
    Returns: {
        "items": [...],
        "total_items": int,
        "total_price": float
    }
    """
    with inventory_lock:
        items = []
        total_items = 0
        total_price = 0.0
        
        for product_id, quantity in cart_db.items():
            if product_id in products_db:
                product = products_db[product_id]
                subtotal = product["price"] * quantity
                
                items.append({
                    "product_id": product_id,
                    "name": product["name"],
                    "price": product["price"],
                    "quantity": quantity,
                    "subtotal": subtotal
                })
                
                total_items += quantity
                total_price += subtotal
        
        return {
            "items": items,
            "total_items": total_items,
            "total_price": round(total_price, 2)
        }


def checkout() -> Dict:
    """
    Finalize order with atomic stock validation and update.
    All-or-nothing: if any item has insufficient stock, entire checkout fails.
    
    Returns: {
        "success": True,
        "message": str,
        "order_summary": {...}
    } or raises ValueError
    """
    with inventory_lock:
        if not cart_db:
            raise ValueError("Cart is empty")
        
        # Phase 1: Validate all items have sufficient stock
        validation_errors = []
        for product_id, quantity in cart_db.items():
            if product_id not in products_db:
                validation_errors.append(f"Product ID {product_id} not found")
                continue
            
            product = products_db[product_id]
            if quantity > product["stock"]:
                validation_errors.append(
                    f"{product['name']}: Insufficient stock "
                    f"(Available: {product['stock']}, Requested: {quantity})"
                )
        
        # If any validation fails, abort entire checkout
        if validation_errors:
            raise ValueError("Checkout failed: " + "; ".join(validation_errors))
        
        # Phase 2: All validations passed - commit changes atomically
        order_items = []
        total_price = 0.0
        
        for product_id, quantity in cart_db.items():
            product = products_db[product_id]
            subtotal = product["price"] * quantity
            
            # Deduct stock
            products_db[product_id]["stock"] -= quantity
            
            order_items.append({
                "product_id": product_id,
                "name": product["name"],
                "price": product["price"],
                "quantity": quantity,
                "subtotal": subtotal
            })
            
            total_price += subtotal
        
        # Clear cart after successful checkout
        cart_db.clear()
        
        return {
            "success": True,
            "message": "Order placed successfully",
            "order_summary": {
                "items": order_items,
                "total_items": sum(item["quantity"] for item in order_items),
                "total_price": round(total_price, 2)
            }
        }
