# tools.py
from typing import Optional
from langchain_core.tools import tool
from database import SessionLocal, Shoe, Order

@tool
def check_stock(brand: Optional[str] = None, model: Optional[str] = None, size: Optional[float] = None, max_price: Optional[float] = None) -> str:
    """Check inventory for shoes using any combination of brand, model, size, or maximum price."""
    db = SessionLocal()
    query = db.query(Shoe)
    
    # Dynamically build the query based on what the user provided
    if brand:
        query = query.filter(Shoe.brand.ilike(f"%{brand}%"))
    if model:
        query = query.filter(Shoe.model.ilike(f"%{model}%"))
    if size:
        query = query.filter(Shoe.size == size)
    if max_price:
        query = query.filter(Shoe.price <= max_price)
        
    shoes = query.all()
    db.close()
    
    if not shoes:
        return "I couldn't find any shoes matching those exact criteria."
        
    # Filter for items actually in stock
    available_shoes = [s for s in shoes if s.stock > 0]
    
    if not available_shoes:
        return "We carry those shoes, but they are currently out of stock."
        
    # Format the results
    results = [f"- {s.brand} {s.model} (Size {s.size}): {s.stock} pairs left at ${s.price}" for s in available_shoes]
    
    # If the search is too broad (e.g., just asking for "Nike"), limit the output so the LLM doesn't get overwhelmed
    if len(results) > 10:
        return "We have many options matching that! Here are the first 10:\n" + "\n".join(results[:10]) + "\n(Ask the user to be more specific to narrow it down)."
        
    return "Here is what we have in stock:\n" + "\n".join(results)

@tool
def place_order(customer_name: str, model: str, size: float, quantity: int) -> str:
    """Place an order for shoes. Deducts the requested quantity from stock if available."""
    db = SessionLocal()
    shoe = db.query(Shoe).filter(Shoe.model.ilike(f"%{model}%"), Shoe.size == size).first()
    
    if not shoe:
        db.close()
        return "Failed to place order: Shoe does not exist."
    
    # Check if we have enough stock for the requested quantity
    if shoe.stock < quantity:
        db.close()
        return f"Failed to place order: We only have {shoe.stock} pairs of size {size} left."
    
    # Decrement stock by the requested quantity
    shoe.stock -= quantity
    new_order = Order(customer_name=customer_name, shoe_id=shoe.id, quantity=quantity, status="Confirmed")
    db.add(new_order)
    db.commit()
    
    order_id = new_order.id
    db.close()
    return f"Success! Order #{order_id} placed for {customer_name}. You bought {quantity} pair(s) of the {model} size {size}."

@tool
def list_available_models(brand: str = None) -> str:
    """Lists available shoe models, optionally filtered by a specific brand."""
    db = SessionLocal()
    
    if brand:
        shoes = db.query(Shoe).filter(Shoe.brand.ilike(f"%{brand}%")).all()
        prefix = f"Here are the {brand} models we have:"
    else:
        shoes = db.query(Shoe).distinct(Shoe.brand, Shoe.model).all()
        prefix = "Here is a list of the brands and models we carry:"

    db.close()
    
    if not shoes:
        return "I couldn't find any shoes matching that description."
        
    # Create a unique list of brand/model combinations
    unique_models = set(f"- {shoe.brand} {shoe.model}" for shoe in shoes)
    
    return f"{prefix}\n" + "\n".join(unique_models)

# List of tools for the agent to use
tools = [check_stock, place_order, list_available_models]