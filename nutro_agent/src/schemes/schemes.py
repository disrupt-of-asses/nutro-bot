from pydantic import BaseModel
from langchain.agents.mrkl.output_parser import MRKLOutputParser

class MenuParams(BaseModel):
    gender: str
    weight: float
    age: int
    activity: str
    complexity: str
    period: int
    portions: int

class MenuOutputParser(MRKLOutputParser):
    def parse(self, text: str):
        try:
            # Attempt to extract and parse the JSON part
            json_start = text.find("{")
            json_end = text.rfind("}") + 1
            if json_start != -1 and json_end != -1:
                json_text = text[json_start:json_end]
                return super().parse(json_text)
            else:
                raise ValueError("No JSON found in the output.")
        except Exception as e:
            print("Parsing failed:", e)
            return {"error": "Parsing failed", "raw_output": text}

