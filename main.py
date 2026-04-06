from fastapi import FastAPI, HTTPException
import random
from models import Observation, Action, Reward, PatientData
from tasks import TASKS

app = FastAPI(title="OpenEnv AI Radiologist - Clinical Grade")

class EnvState:
    def __init__(self):
        self.step_count = 0
        self.is_done = False
        self.current_task = None
        self.score = 0.0
        self.time_spent = 0
        # Track what evidence the AI has gathered
        self.has_viewed_image = False
        self.has_viewed_history = False

state = EnvState()

@app.post("/reset", response_model=Observation)
def reset():
    state.step_count = 0
    state.is_done = False
    state.score = 0.0
    state.time_spent = 0
    state.has_viewed_image = False
    state.has_viewed_history = False
    state.current_task = random.choice(TASKS)
    
    return Observation(
        image_url=state.current_task["image_url"],
        feedback=f"URGENT: New patient case opened. Difficulty: {state.current_task['difficulty']}. Gather evidence before diagnosing.",
        is_done=False
    )

@app.post("/step")
def step(action: Action):
    if state.is_done:
        raise HTTPException(status_code=400, detail="Episode done. Call /reset.")
        
    state.step_count += 1
    obs = Observation(
        image_url=state.current_task["image_url"],
        time_spent_minutes=state.time_spent,
        is_done=False
    )
    reward_msg = ""
    reward_score = 0.0

    # 1. ACTION: REQUEST HISTORY (Costs 2 minutes)
    if action.action_type == "request_history":
        state.time_spent += 2
        state.has_viewed_history = True
        obs.patient_info = PatientData(**state.current_task["patient_info"])
        obs.feedback = "Patient history reviewed."
        reward_score = 0.05

    # 2. ACTION: EXAMINE IMAGE (Costs 5 minutes)
    elif action.action_type == "examine_image":
        state.time_spent += 5
        state.has_viewed_image = True
        obs.feedback = f"Radiology report: {state.current_task['image_description']}"
        reward_score = 0.1

    # 3. ACTION: ORDER BLOOD TEST (Costs 30 minutes!)
    elif action.action_type == "order_blood_test":
        state.time_spent += 30
        obs.lab_results = "WBC count elevated. CRP elevated." if state.current_task["true_finding"] in ["pneumonia", "tuberculosis"] else "All lab values within normal limits."
        obs.feedback = "Blood test results received."
        reward_score = 0.0

    # 4. ACTION: SUBMIT DIAGNOSIS
    elif action.action_type == "submit_diagnosis":
        state.is_done = True
        obs.is_done = True
        
        # CLINICAL SAFETY CHECK: Did they guess blindly?
        if not state.has_viewed_image:
            reward_score = -1.0 # Massive penalty
            obs.feedback = "MALPRACTICE: You submitted a diagnosis without examining the X-ray. Patient safety severely compromised."
            reward_msg = "Critical failure. Blind diagnosis."
            
        else:
            # Check accuracy
            if action.diagnosis_finding and state.current_task["true_finding"] in action.diagnosis_finding.lower():
                base_score = 1.0
                
                # Efficiency bonus/penalty based on time spent
                if state.time_spent > 40:
                    base_score -= 0.2 # Penalty for wasting too much time/resources
                    reward_msg = "Correct diagnosis, but resource management was inefficient."
                elif state.has_viewed_history:
                    reward_msg = "Excellent. Correct diagnosis with proper clinical context."
                else:
                    base_score -= 0.1 # Penalty for ignoring patient history
                    reward_msg = "Correct diagnosis, but you ignored the patient's medical history."
                    
                reward_score = base_score
                obs.feedback = "Final diagnosis accepted by the attending physician."
            else:
                reward_score = 0.0
                obs.feedback = f"Misdiagnosis. The correct finding was {state.current_task['true_finding']}."
                reward_msg = "Failed to identify the primary pathology."

    # Update observation with current time
    obs.time_spent_minutes = state.time_spent

    return {
        "observation": obs.model_dump(),
        "reward": Reward(score=reward_score, message=reward_msg).model_dump(),
        "done": state.is_done,
        "info": {"step": state.step_count, "time_spent": state.time_spent}
    }

@app.get("/state")
def get_state():
    return {"step_count": state.step_count, "is_done": state.is_done, "current_time": state.time_spent}