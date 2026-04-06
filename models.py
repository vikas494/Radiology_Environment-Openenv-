from pydantic import BaseModel, Field
from typing import Optional, Literal

# --- OBSERVATION SPACE ---
class PatientData(BaseModel):
    age: int
    gender: str
    symptoms: str
    vitals: Optional[str] = Field(None, description="Patient vitals (heart rate, blood pressure, etc.)")

class Observation(BaseModel):
    image_url: str = Field(..., description="URL of the current X-ray image")
    patient_info: Optional[PatientData] = Field(None, description="Revealed patient history")
    lab_results: Optional[str] = Field(None, description="Results from ordered bloodwork")
    time_spent_minutes: int = Field(0, description="Time elapsed in this clinical case. Lower is better.")
    feedback: str = Field("", description="System feedback from the last action")
    is_done: bool = Field(False, description="Whether the session is complete")

# --- ACTION SPACE ---
class Action(BaseModel):
    action_type: Literal[
        "request_history", 
        "examine_image", 
        "order_blood_test", 
        "submit_diagnosis"
    ] = Field(..., description="The clinical action to take.")
    
    diagnosis_finding: Optional[str] = Field(
        None, description="If submitting diagnosis, the primary finding."
    )
    rationale: Optional[str] = Field(
        None, description="Brief explanation of WHY you are taking this action or making this diagnosis."
    )

# --- REWARD SPACE ---
class Reward(BaseModel):
    score: float = Field(..., ge=-1.0, le=1.0, description="Reward score. Can be negative for malpractice.")
    message: str = Field(..., description="Explanation of the clinical evaluation")