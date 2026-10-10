import os
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
import joblib

# Load dataset
X, y = load_iris(return_X_y=True)

# Train simple model
model = LogisticRegression(max_iter=200)
model.fit(X, y)

# Save model
os.makedirs("data", exist_ok=True)
joblib.dump(model, "data/model.pkl")
print("✅ Model trained and saved as data/model.pkl")
