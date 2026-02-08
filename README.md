
 # What is this project about?
This project basically is a framework that uses machine learning to analyse student data and uses generative AI and data visualisation to provide a teacher with insights not only about the students who are struggling but also about the "why" behind the struggle

# How does it do it?
The application takes a 20 column csv, the 20 columns being as follows:
It uses a preprocessing pipeline (which maps descriptive data columns to numbers and scales it using min-max scaler for each column) , and uses it to obtain a 3 model framework:
### Model 1 :The academic trajectory based clustering
This model uses two fields Exam_Score and Previous_Scores and clusters the student data based on these 2 features.
We use the K-means algorithm to  obtain 3 academic trajectory clusters:
  -Highly Improved Students
  -Steady Performance Students
  -Declining Students
The centroids obtained on the given student dataset are as follows:
    ` {'cluster1': array([0.26407826, 0.4980978 ]), 'cluster2': array([0.28523119, 0.83384127]), 'cluster3': array([0.24843434, 0.16748274])}
     {"cluster1":"Steady_Progress_Students","cluster2":"Highly_Improved_Students","cluster3":"Declining_Students"}`

### Model 2: clustering beyond marks
This model takes the 19 columns (except the Exam_Score column) from the preprocessing pipeline , reduces them to 5 features viz Academic Drive, Resource access, Family Capital,Personal Wellbeing and environmental stability.
This is how the 5 features map to the original 19 features:
The 5 features are then used to cluster students based on metrics other than academics and this enables us to identify various personas that exist in our classroom and also helps us to see each student with more information and not just marks.
for more info about how the 5 feature reduction happens check out the **featureReduction script** inside the **dataConversions folder**
Based on the 5 features the student data is clustered into 5 personas(the choice of number of clusters has been done through Elbow method and  hence we use K=5 in the K-means algorithm)
Here is what each cluster in this specific dataset is named:
and here are the centroids:
`{'cluster1': array([0.48434735, 0.51876055, 0.35172773, 0.32871612, 0.69163936]), 'cluster2': array([0.4705168 , 0.51762281, 0.72973323, 0.31982215, 0.69597686]), 'cluster3': array([0.47009039, 0.51307385, 0.73488024, 0.67072522, 0.73466401]), 'cluster4': array([0.47551055, 0.50872846, 0.34926632, 0.67422251, 0.72645642]), 'cluster5': array([0.4701202 , 0.51256057, 0.55062768, 0.58281026, 0.38376831])}`


### Model 3: The linear regression based model 
This model takes the 19 columns from the preprocessing pipeline as inputs and use the unscaled Exam_Score column as output . Linear regression algorithm is applied to it and the relative dependency of Exam-Score on the 19 columns is identified.
here are our weights on the given dataset (visualised)
![WhatsApp Image 2026-01-26 at 11 09 02 PM](https://github.com/user-attachments/assets/01485963-4188-44e1-90f5-8b535cb61163)

This model enables us to find the weights of the 19 features in determining the Exam_Score of the student, so that we can control the most positively or negatively influencing factors and help the student in  improving their scores.

# The system architecture
### the project structure
- Backend : flask
- frontend :HTML, CSS, Javascript(Vanilla), chart.js for viualising charts
- Machine learning logic : lives in the utilities package which is imported in the backend
- LLM : google genai API 
### features :
we enable the teacher to conduct analysis in 2 modes:
- analyse single student (here we use our 5 feature script to generate the 5 feature profile of the student and display it in the form of a spider chart
- analyse whole class or full dataset (here we use our Model1 and Model2 to obtain the clusterwise composition of the class.
  <img width="1080" height="252" alt="image" src="https://github.com/user-attachments/assets/7e146bfc-8ea8-4ebc-b98b-9846a67b3f60" />

-  We also use a cross model query to find out the behavioural composition of each acdamic trajectory (e.g the 5 persona composition of the declining students cluster) enabling us to identify behavioural trends amongst various academic groups
<img width="1437" height="902" alt="image" src="https://github.com/user-attachments/assets/ebf913f3-b7f0-4eec-b6c0-3c62bd825e0c" />


- if the Exam_Score column is kept vacant , then the application uses model 3 to predict Exam_score, obtain clustering on the predicted score and identify at risk students before the risk becomes the reality
- Generative AI is used to interpret the results from the 3 models and suggest actionable insights which help in academic growth of the students


# future plans:
-making the application more useful by training model3 on a dataset that focuses on  features that serve real world use cases
-implementing a scenario simulator where teacher can simulate scenarios like how will the Exam_Score of the student change if he begins to study 1 hour more or if he sleeps 1 extra hour without the app treating it as a new instance (specially the gen-ai should see it as a simulation and not a separate analysis)
-clustering user data and not just run predictions on it using pretrained models (this will help us cluster classrooms which differ completely from our current dataset and this means we will have to dynamically name our clusters for which we plan to use genai)
-embedding an ai agent which is context aware and can help the teacher analyse even further as the teacher asks questions or makes requests


# contributors 
Neha Malhotra
Ayushi Agrawal
Mayank Chaudhary
Suhani Sharma


# How you can contribute?
- contribute us with new ideas about how cann we change our architecture , approach or suggesting us a new use case for the project
- guide us about how we can make this project scalable
- test our project and expose bugs
  
# How to setup the environment for this project?
Install all the packages mentioned in the requirements.txt
Get yourself a gemini API key


