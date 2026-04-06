# tasks.py

TASKS = [
    # --- EASY TASKS (Clear normal scans) ---
    {
        "id": "task_easy_01",
        "difficulty": "easy",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c8/Chest_Xray_PA_3-8-2010.png/500px-Chest_Xray_PA_3-8-2010.png",
        "patient_info": {"age": 25, "gender": "Female", "symptoms": "Routine checkup for work. No symptoms."},
        "true_finding": "normal",
        "image_description": "The lungs are clear. The heart size is normal. No abnormalities detected."
    },
    {
        "id": "task_easy_02",
        "difficulty": "easy",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f6/Normal_knee_X-ray.jpg/500px-Normal_knee_X-ray.jpg",
        "patient_info": {"age": 22, "gender": "Male", "symptoms": "Mild knee pain after running, but no swelling."},
        "true_finding": "normal",
        "image_description": "Joint spaces are well preserved. No evidence of fracture, dislocation, or joint effusion."
    },

    # --- MEDIUM TASKS (Clear pathologies) ---
    {
        "id": "task_medium_01",
        "difficulty": "medium",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1c/COVID-19_pneumonia_-_typical_findings.jpg/500px-COVID-19_pneumonia_-_typical_findings.jpg",
        "patient_info": {"age": 58, "gender": "Male", "symptoms": "Fever, severe cough, shortness of breath for 3 days."},
        "true_finding": "pneumonia",
        "image_description": "There are bilateral ground-glass opacities in the lungs, strongly indicating pneumonia."
    },
    {
        "id": "task_medium_02",
        "difficulty": "medium",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c1/Cardiomegaly_CXR.jpg/500px-Cardiomegaly_CXR.jpg",
        "patient_info": {"age": 65, "gender": "Female", "symptoms": "Fatigue, swelling in the ankles, shortness of breath when lying flat."},
        "true_finding": "cardiomegaly",
        "image_description": "The cardiac silhouette is significantly enlarged, taking up more than 50% of the chest width. Lungs are otherwise clear."
    },

    # --- HARD TASKS (Subtle or complex pathologies) ---
    {
        "id": "task_hard_01",
        "difficulty": "hard",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Rib_fracture.jpg/500px-Rib_fracture.jpg",
        "patient_info": {"age": 72, "gender": "Male", "symptoms": "Chest pain on the right side after a minor fall in the bathroom."},
        "true_finding": "fracture",
        "image_description": "The lungs are mostly clear, but there is a subtle hairline fracture on the right 6th rib."
    },
    {
        "id": "task_hard_02",
        "difficulty": "hard",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/89/Tuberculosis_symptoms.jpg/500px-Tuberculosis_symptoms.jpg",
        "patient_info": {"age": 41, "gender": "Male", "symptoms": "Chronic weight loss, night sweats, and coughing up blood for 3 weeks."},
        "true_finding": "tuberculosis",
        "image_description": "Cavitary lesions are present in the upper right lobe, alongside scattered nodular opacities."
    }
]