import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.schema import HumanMessage
from typing import List

class LLMService:
    def __init__(self, api_key: str):
        # Initialize LangChain with Google AI
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=api_key,
            temperature=0.1
        )
        
        # Create prompt template
        self.prompt_template = PromptTemplate(
            input_variables=["gender", "age", "symptoms"],
            template="""
            Based on patient symptoms, recommend the most appropriate medical department.
            
            Patient: {gender}, {age} years old
            Symptoms: {symptoms}
            
            Available departments: Neurology, Cardiology, Orthopedics, Gastroenterology, Dermatology, Psychiatry, General Medicine, Emergency Medicine, Pulmonology
            
            Respond with ONLY the department name.
            """
        )
    
    def get_department_recommendation(self, gender: str, age: int, symptoms: List[str]) -> str:
        """Get department recommendation using LangChain + Google AI"""
        symptoms_text = ", ".join(symptoms)
        
        # Format prompt using LangChain
        formatted_prompt = self.prompt_template.format(
            gender=gender,
            age=age,
            symptoms=symptoms_text
        )
        
        try:
            # Use LangChain to call Google AI
            message = HumanMessage(content=formatted_prompt)
            response = self.llm([message])
            return response.content.strip()
        except Exception as e:
            print(f"LLM Error: {e}")
            return "General Medicine"  