from langchain_openai import ChatOpenAI
from dataclasses import dataclass
from pydantic import BaseModel,Field

@dataclass
class relevant_candidate(BaseModel):
    user_name: str = Field(description='Find the most relevant employee to send a mail based on user message.')
    content: str = Field(description='Summary of the email message to send to the candidate')

def model(base,key):
    model = ChatOpenAI(
        model='gpt-4o-mini',
        base_url = base,
        api_key = key,
        temperature=0
    )
    return model

def structured_model(relevant_candidate: Type[relevant_candidate],llm):
    return llm.with_structured_output(relevant_candidate)
