from pydantic import BaseModel, Field, HttpUrl

class Book(BaseModel):
    url: str
    title: str
    price: float = Field(..., description="Price in GBP (£)")
    rating: int = Field(..., ge=1, le=5, description="Star rating between 1 and 5")
    availability: str
    stock_count: int = Field(..., ge=0, description="Available stock quantity")
    upc: str
    product_type: str
    price_excl_tax: float
    price_incl_tax: float
    tax: float
    number_of_reviews: int
    description: str | None = None