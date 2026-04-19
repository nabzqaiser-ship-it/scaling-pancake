from pydantic import BaseModel,Field


class DocumentAnalysis(BaseModel):
    summary: str
    sentiment: str
    category: str
    key_points: list[str]
    confidence_score: float = Field(ge=0.0, le=1.0)

class FileInfo(BaseModel):
    filename: str = Field(min_length=1, pattern=r"^.+\.txt$")
    filepath: str = Field(min_length=1)
    wordcount: int = Field(ge=0)

    analysis: DocumentAnalysis