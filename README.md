# Learning Pattern Analysis Framework 🎓

This project is a framework that uses machine learning to analyze student data and uses generative AI and data visualization to provide a teacher with insights not only about the students who are struggling but also about the "why" behind the struggle.

# 📋 Table of Contents

How does it do it?
System Architecture
Key Features
Future Plans
Contributors
Environment Setup

# 🛠 How does it do it?

The application takes a 20-column CSV. It uses a preprocessing pipeline which maps descriptive data columns to numbers and scales them using a Min-Max Scaler. This feeds into a 3-model framework:

## 1. Model 1: Academic Trajectory Based Clustering

This model uses two fields: Exam_Score and Previous_Scores. We use the K-means algorithm to obtain 3 academic trajectory clusters:
- Highly Improved Students

- Steady Performance Students

- Declining Students

Centroids obtained on the dataset:

{
  "cluster1": [0.26407826, 0.4980978],  // Steady_Progress_Students
  "cluster2": [0.28523119, 0.83384127], // Highly_Improved_Students
  "cluster3": [0.24843434, 0.16748274]  // Declining_Students
}


## 2. Model 2: Clustering Beyond Marks

This model takes 19 columns (excluding Exam_Score) and reduces them to 5 Behavioral Pillars:
-Academic Drive
-Resource Access
-Family Capital
-Personal Wellbeing
-Environmental Stability

The student data is clustered into 5 Personas (determined via the Elbow Method).
For more info about how the 5-feature reduction happens, check out the featureReduction script inside the dataConversions folder.

Centroids for this dataset:

Cluster 1: [0.484, 0.518, 0.351, 0.328, 0.691]
Cluster 2: [0.470, 0.517, 0.729, 0.319, 0.695]
Cluster 3: [0.470, 0.513, 0.734, 0.670, 0.734]
Cluster 4: [0.475, 0.508, 0.349, 0.674, 0.726]
Cluster 5: [0.470, 0.512, 0.550, 0.582, 0.383]

## 3. Model 3: Linear Regression Based Model

This model uses the 19 columns as inputs and the unscaled Exam_Score as output. It identifies the relative dependency of scores on specific features.
Visualized Weights:

# 🏗 System Architecture

Backend: Flask
Frontend: HTML, CSS, Javascript (Vanilla)
Visualization: Chart.js
Machine Learning Logic: Located in the utilities package
LLM: Google GenAI API (Gemini)

# ✨ Features

Single Student Analysis: Generates a 5-feature profile displayed as a Spider Chart.

Whole Class Analysis: Visualizes Model 1 and Model 2 to show cluster-wise composition.

<img width="1080" height="252" alt="Class analysis overview" src="https://github.com/user-attachments/assets/7e146bfc-8ea8-4ebc-b98b-9846a67b3f60" />

Cross-Model Querying: Find behavioral trends amongst academic groups (e.g., "The 5-persona composition of declining students").

<img width="1437" height="902" alt="Cross model analysis" src="https://github.com/user-attachments/assets/ebf913f3-b7f0-4eec-b6c0-3c62bd825e0c" />

Predictive Risk Assessment: If Exam_Score is vacant, Model 3 predicts it to identify at-risk students proactively.

Generative AI Insights: Interprets results from all three models to suggest actionable growth steps.

# 🚀 Future Plans

Real-world Training: Training Model 3 on datasets focused on specific real-world use cases.
Scenario Simulator: A "what-if" tool for teachers (e.g., simulating how adding 1 hour of study affects the predicted score).
Dynamic Persona Naming: Using Gen-AI to name clusters based on unique classroom data distributions.
AI Agent: A context-aware agent to help teachers navigate analysis via natural language.

# 👥 Contributors

Neha Malhotra
Ayushi Agrawal
Mayank Chaudhary
Suhani Sharma

# 🤝 How you can contribute?

- Suggest changes to our architecture or new use cases.
- Guide us on making the project more scalable.
- Test the project and expose bugs.

# 💻 How to setup the environment for this project?

Install all packages mentioned in the requirements.txt:

```pip install -r requirements.txt```


Obtain a Gemini API Key from Google AI Studio.

Configure your environment variables to include your API Key.

Run the Flask application:

```python app.py```
