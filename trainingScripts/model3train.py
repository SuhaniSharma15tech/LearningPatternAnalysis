import pandas as pd
import joblib # Added for saving the model
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler # Changed from StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error

# 1. Load data
df = pd.read_csv("data/unscalednumericdata.csv")

# 2. Split features and target
TARGET_COL = "Exam_Score"
X = df.drop(TARGET_COL, axis=1)
y = df[TARGET_COL]

# 3. Train/Test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 4. Apply Min-Max Scaling
scaler = MinMaxScaler() 
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# 5. Train the Regression Model
model = LinearRegression()
model.fit(X_train_scaled, y_train)

# 6. Evaluate
y_pred = model.predict(X_test_scaled)
print(f"R2 Score: {r2_score(y_test, y_pred)}")
print(f"Mean Absolute Error: {mean_absolute_error(y_test, y_pred)}")
print("Root Mean Squared Error      :", mean_squared_error(y_test, y_pred, squared=False))
# 7. SAVE FOR DASHBOARD (Important!)
# Create a 'models' folder in your directory first
joblib.dump(model, 'models/regression_model.pkl')
joblib.dump(scaler, 'models/regression_scaler.pkl')

print("Success: Model and Min-Max Scaler saved to /models folder.")

