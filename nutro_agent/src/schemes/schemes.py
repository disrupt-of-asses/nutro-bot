from pydantic import BaseModel

class MenuParams(BaseModel):
    gender: str
    weight: float
    age: int
    activity: str
    complexity: str
    period: int
    portions: int