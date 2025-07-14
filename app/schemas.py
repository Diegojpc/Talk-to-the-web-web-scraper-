from datetime import datetime
from typing import Annotated, Literal
from uuid import uuid4
from pydantic import BaseModel, Field, IPvAnyAddress

class ModelRequest(BaseModel):
    prompt: Annotated[str, Field(min_length=1, max_length=10000)] 

class ModelResponse(BaseModel):
    request_id: Annotated[str, Field(default_factory=lambda: uuid4().hex)] 
    # no defaults set for ip field
    # raise ValidationError if a valid IP address or None is not provided
    ip: Annotated[str, IPvAnyAddress] | None 
    content: Annotated[str | None, Field(min_length=0, max_length=10000)] 
    created_at: datetime = datetime.now()

class TextModelRequest(ModelRequest):
    # model: Literal["gemini-2.5-pro", "gemini-2.5-flash"]
    model: Literal["v2/en_speaker_1", "v2/en_speaker_9"]
    temperature: Annotated[float, Field(ge=0.0, le=1.0, default=0.7)] 

class TextModelResponse(ModelResponse):
    tokens: Annotated[int, Field(ge=0)]