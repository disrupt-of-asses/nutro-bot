from pydantic import BaseModel, Field, ValidationError

class UserParams(BaseModel):
    gender: str = Field(..., pattern="^(male|female)$", description="Gender must be 'male' or 'female'")
    weight: float = Field(..., gt=0, description="Weight must be a positive number")
    age: int = Field(..., gt=0, description="Age must be a positive integer")
    activity: str = Field(..., description="Activity level (e.g., low, moderate, high)")
    complexity: str = Field(..., description="Menu complexity (e.g., easy, medium, hard)")
    period: int = Field(..., gt=0, description="Period must be a positive integer")
    portions: int = Field(..., gt=0, description="Portions must be a positive integer")