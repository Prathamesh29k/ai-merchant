from pydantic import BaseModel, ConfigDict, Field


class ProductCreate(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    category: str = Field(min_length=1, max_length=50)
    description: str = ""
    price_paise: int = Field(ge=0)
    stock: int = Field(ge=0)


class ProductResponse(ProductCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)


class OrderCreate(BaseModel):
    product_id: int
    quantity: int = Field(default=1, ge=1)
    agent_id: str = Field(default="demo-agent", min_length=1, max_length=120)


class OrderResponse(BaseModel):
    id: int
    agent_id: str
    product_id: int
    quantity: int
    amount_paise: int
    amount_inr: float
    status: str
    razorpay_order_id: str
    daily_total_paise: int
    daily_limit_paise: int


class PaymentVerifyRequest(BaseModel):
    order_id: int
    razorpay_order_id: str
    razorpay_payment_id: str
    razorpay_signature: str


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=1000)
    agent_id: str = "demo-agent"
