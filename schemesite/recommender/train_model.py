import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder
import joblib

# Load your CSV
df = pd.read_csv("schemes.csv")

# Encode occupation column
le = LabelEncoder()
df['occupation_encoded'] = le.fit_transform(df['occupation'])

# Prepare training data
X = df[['min_age', 'max_age', 'min_income', 'max_income', 'occupation_encoded']]
y = df['scheme_name']

# Train model
model = DecisionTreeClassifier()
model.fit(X, y)

# Save model & encoder
joblib.dump(model, 'scheme_model.pkl')
joblib.dump(le, 'occupation_encoder.pkl')

print("✅ Model trained and saved!")
