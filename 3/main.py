from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from llm_service import LLMService

# Initialize LLM service with your API key
llm_service = LLMService(api_key="AIzaSyDhRZADofHVUljfmkfqJUvBuifczXTau3A") 

app = FastAPI(title="Hospital Triage API")

class PatientInfo(BaseModel):
    gender: str
    age: int
    symptoms: List[str]

class RecommendationResponse(BaseModel):
    recommended_department: str

@app.post("/recommend")
async def recommend_department(patient: PatientInfo):
    # Use LLM service instead of rule-based logic
    recommended_dept = llm_service.get_department_recommendation(
        gender=patient.gender,
        age=patient.age,
        symptoms=patient.symptoms
    )
    
    return {"recommended_department": recommended_dept}

@app.get("/")
async def root():
    return {"message": "Hospital Triage API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)