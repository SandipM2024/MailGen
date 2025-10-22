from pydantic import BaseModel
from typing import Optional,List,Dict
# Request model
class YouTubeRequest(BaseModel):
    url: str


class SummarizeRequest(BaseModel):
    text: str
    token_threshold: Optional[int] = 3500


class MCQ(BaseModel):
    question: str
    options: Dict[str, str]
    answer: str

class MCQResponse(BaseModel):
    questions: List[MCQ]
