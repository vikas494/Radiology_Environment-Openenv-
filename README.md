title: AI Radiologist
emoji: 🩺
colorFrom: blue
colorTo: indigo
sdk: docker
app_port: 7860

# OpenEnv: AI Radiologist (Clinical Grade) 🩺

## Environment Description & Motivation
The **AI Radiologist** environment simulates a high-stakes clinical setting where an autonomous agent must evaluate patient cases and submit accurate medical diagnoses. 

Unlike standard image-classification tasks, this environment mimics real-world medical complexities. The agent is evaluated not just on diagnostic accuracy, but on **clinical safety** and **resource efficiency**. Blindly guessing a diagnosis without reviewing the X-ray results in a severe malpractice penalty, while ordering unnecessary tests wastes time resources. The agent must balance accuracy, safety, and time management.

## Action & Observation Spaces

### Observation Space
The agent receives a detailed clinical picture at each step:
* `image_url` (str): Link to the current patient's X-ray.
* `patient_info` (dict): Demographic and symptom history (hidden until requested).
* `lab_results` (str): Results from ordered bloodwork (hidden until ordered).
* `time_spent_minutes` (int): A tracker of clinical time used. Lower is better.
* `feedback` (str): System feedback from the previous action.

### Action Space
The agent can take four distinct actions, each with an associated "time cost":
1. `request_history` (Cost: 2 mins): Retrieve patient demographics and symptoms.
2. `examine_image` (Cost: 5 mins): Mandatory action to review the radiology scan.
3. `order_blood_test` (Cost: 30 mins): Order labs to check for infection markers.
4. `submit_diagnosis`: Conclude the episode by submitting the final finding.

The agent is also expected to provide a `rationale` (Chain of Thought) for each action.

## Tasks & Difficulty
The environment features 6 dynamic tasks across three difficulty tiers:
* **Easy (2 tasks):** Healthy patients with clear scans (Normal chest, Normal knee).
* **Medium (2 tasks):** Clear, distinct pathologies (COVID-19 Pneumonia, Cardiomegaly).
* **Hard (2 tasks):** Subtle or complex conditions requiring careful analysis (Hairline Rib Fracture, Cavitary Tuberculosis).

## Setup and Usage Instructions

### Running Locally
1. Clone this repository and navigate to the directory.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt