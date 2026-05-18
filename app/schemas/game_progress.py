from pydantic import BaseModel, Field


class UpdateGameProgressRequest(BaseModel):
    last_passed_level: int = Field(..., ge=1)


class GameProgressResponse(BaseModel):
    progress_id: int
    child_id: int
    last_passed_level: int

    class Config:
        from_attributes = True