from pydantic import BaseModel, ConfigDict, Field


class CreditScoringRequest(BaseModel):
    limit_bal: float = Field(..., description="Credit limit")
    sex: int = Field(..., description="1 = male, 2 = female")
    education: int = Field(..., description="Education level")
    marriage: int = Field(..., description="Marital status")
    age: int = Field(..., description="Age in years")

    pay_0: int
    pay_2: int
    pay_3: int
    pay_4: int
    pay_5: int
    pay_6: int

    bill_amt1: float
    bill_amt2: float
    bill_amt3: float
    bill_amt4: float
    bill_amt5: float
    bill_amt6: float

    pay_amt1: float
    pay_amt2: float
    pay_amt3: float
    pay_amt4: float
    pay_amt5: float
    pay_amt6: float

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "limit_bal": 20000,
                "sex": 2,
                "education": 2,
                "marriage": 1,
                "age": 24,
                "pay_0": 2,
                "pay_2": 2,
                "pay_3": -1,
                "pay_4": -1,
                "pay_5": -2,
                "pay_6": -2,
                "bill_amt1": 3913,
                "bill_amt2": 3102,
                "bill_amt3": 689,
                "bill_amt4": 0,
                "bill_amt5": 0,
                "bill_amt6": 0,
                "pay_amt1": 0,
                "pay_amt2": 689,
                "pay_amt3": 0,
                "pay_amt4": 0,
                "pay_amt5": 0,
                "pay_amt6": 0
            }
        }
    )


class CreditScoringResponse(BaseModel):
    probability_default: float
    predicted_class: int
    threshold: float
    risk_level: str
    model_name: str