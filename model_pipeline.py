# -*- coding: utf-8 -*-
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib

# -----------------------------
# 1. Load Data
# -----------------------------
data = pd.read_csv('datasets/dataset1.csv')
X = pd.read_csv('datasets/dataset2.csv')
y = data["Class"].to_numpy()

# -----------------------------
# 2. Split train and test
# -----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# -----------------------------
# 3. Preprocessing
# -----------------------------
numeric_features = X.select_dtypes(include=['int64', 'float64']).columns.tolist()
categorical_features = X.select_dtypes(include=['object']).columns.tolist()

preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numeric_features),
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
    ]
)

# -----------------------------
# 4. Final model (tuned hyperparameters)
# -----------------------------
final_model = DecisionTreeClassifier(
    criterion='gini',
    max_depth=8,
    max_features='sqrt',
    min_samples_leaf=2,
    min_samples_split=10,
    splitter='random',
    random_state=42
)

# -----------------------------
# 5. Complete pipeline
# -----------------------------
pipeline = Pipeline([
    ('preprocessor', preprocessor),
    ('classifier', final_model)
])

# -----------------------------
# 6. Treined pipeline
# -----------------------------
pipeline.fit(X_train, y_train)

# -----------------------------
# 7. Model evaluation
# -----------------------------
y_pred = pipeline.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Pipeline accuracy: {accuracy:.4f}")

# -----------------------------
# 8. Save treined pipeline
# -----------------------------
joblib.dump(pipeline, "capstone_pipeline.pkl")
print("Pipeline saved as capstone_pipeline.pkl")
