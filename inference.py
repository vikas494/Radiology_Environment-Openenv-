import os
import requests
import json
from openai import OpenAI

# 1. READ MANDATORY ENVIRONMENT VARIABLES
# The competition requires these exact variable names.
API_BASE_URL = os.getenv("API_BASE_URL", "https://api.openai.com/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini") # You can change this to your preferred model
HF_TOKEN = os.getenv("HF_TOKEN", "").strip() # .strip() removes hidden spaces/newlines

if not HF_TOKEN:
    print("Error: HF_TOKEN environment variable is not set. Please set it to your API key.")
    exit(1)

# 2. SETUP OPENAI CLIENT
client = OpenAI(
    api_key=HF_TOKEN,
    base_url=API_BASE_URL
)

# 3. ENVIRONMENT URL (Your local FastAPI server)
ENV_URL = "https://vm36-radiology-environment.hf.space"

def get_ai_action(observation_text):
    """Asks the LLM what to do next based on what it sees."""
    system_prompt = """
    You are an expert AI Radiologist in a high-stakes hospital environment. 
    Your goal is to diagnose the patient accurately, safely, and efficiently.

    Available Actions:
    1. 'request_history': (Costs 2 mins) Get patient symptoms. Always do this.
    2. 'examine_image': (Costs 5 mins) Look at the scan. MANDATORY before diagnosing.
    3. 'order_blood_test': (Costs 30 mins) Order labs. Only use if infection is suspected.
    4. 'submit_diagnosis': Make your final diagnosis.

    You must respond ONLY with a raw JSON object matching this schema:
    {
      "action_type": "request_history" | "examine_image" | "order_blood_test" | "submit_diagnosis",
      "diagnosis_finding": "<disease name or 'normal'>",
      "rationale": "<Brief explanation of why you are choosing this action>"
    }
    """
    
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Current Observation: {observation_text}\nWhat is your next action in JSON?"}
        ],
        temperature=0.0 # Keep it predictable
    )
    
    # Clean up the response in case the LLM adds markdown formatting like ```json
    raw_response = response.choices[0].message.content.strip()
    if raw_response.startswith("```json"):
        raw_response = raw_response[7:-3]
        
    return json.loads(raw_response)

def run_episode(episode_id):
    """Runs a single diagnostic session from start to finish."""
    print(f"[START] Episode {episode_id}")
    
    # Call /reset to start
    response = requests.post(f"{ENV_URL}/reset")
    obs = response.json()
    
    is_done = False
    step_num = 0
    total_reward = 0.0
    
    while not is_done:
        step_num += 1
        
        # 1. Ask the AI what to do
        action_json = get_ai_action(json.dumps(obs))
        
        # 2. Send the action to your environment
        step_response = requests.post(f"{ENV_URL}/step", json=action_json).json()
        
        # 3. Update state
        obs = step_response["observation"]
        reward = step_response["reward"]["score"]
        total_reward = reward # In this env, the final score overrides
        is_done = step_response["done"]
        
        # 4. Mandatory [STEP] logging format
        print(f"[STEP] {step_num} | Action: {action_json['action_type']} | Reward: {reward}")
        
        # Safety break to prevent infinite loops
        if step_num > 10:
            print("[STEP] Max steps reached. Forcing end.")
            break

    print(f"[END] Episode {episode_id} | Final Score: {total_reward}")
    return total_reward

if __name__ == "__main__":
    # Run 3 episodes to test Easy, Medium, and Hard cases
    print("Starting OpenEnv Baseline Inference...")
    for i in range(1, 4):
        run_episode(i)