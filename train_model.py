import pandas as pd
from sqlalchemy import create_engine
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

print("📊 Starting model training script...")

# 1. Connect directly to our local PostgreSQL database
db_connection_string = "postgresql://postgres:iapetus@localhost:5432/predictive_maintenance"
db_engine = create_engine(db_connection_string)

# 2. Pull our recorded entries into a pandas spreadsheet format
sql_query = "SELECT temperature, vibration, rotational_speed FROM telemetry;"
dataset = pd.read_sql(sql_query, db_engine)

print(f"✅ Successfully loaded {len(dataset)} total records from PostgreSQL database.")

# 3. HUMAN DATA CLEANING: 
# Remember how our simulator occasionally sends missing values (None)? 
# Let's find the average vibration value and manually fill in those gaps.
average_vibration = dataset['vibration'].mean()
dataset['vibration'] = dataset['vibration'].fillna(average_vibration)
print(f"🔧 Replaced missing sensor values with table average: {round(average_vibration, 2)}")

# 4. CREATING THE TRAINING LABELS
# We define a failure as high temperature OR high vibration, or when a sensor drops completely
dataset['is_broken'] = 0
dataset.loc[(dataset['temperature'] > 90.0) & (dataset['vibration'] > 60.0), 'is_broken'] = 1

# 5. SPLITTING DATA FOR EXAM TESTING
# X = what the AI looks at (Sensors). y = the answer key (Is Broken)
X = dataset[['temperature', 'vibration', 'rotational_speed']]
y = dataset['is_broken']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 6. TRAIN THE CLASSIFIER
print("🏋️‍♂️ Fitting Random Forest model to training data...")
ai_classifier = RandomForestClassifier(n_estimators=100, random_state=42)
ai_classifier.fit(X_train, y_train)

# 7. SCORE THE PERFORMANCE
test_predictions = ai_classifier.predict(X_test)
final_score = accuracy_score(y_test, test_predictions)

print("\n=================== FINAL PERFORMANCE ===================")
print(f"🎯 Human-Coded Model Accuracy: {final_score * 100:.2f}%")
print("=========================================================\n")
# 8. SAVE THE TRAINED MODEL FILE
import joblib
joblib.dump(ai_classifier, 'trained_machinery_model.pkl')
print("💾 Model saved successfully as 'trained_machinery_model.pkl'!")