'''
taken from ipynb colab file
'''
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

# generative AI
import google.generativeai as genai
from google.colab import userdata
from typing import List, Dict, Any

# =====Reading CSV=====
# data
url = "https://raw.githubusercontent.com/GregaVrbancic/Phishing-Dataset/refs/heads/master/dataset_full.csv"

# dataframe
df = pd.read_csv(url)

# =====Configuring Gemini=====
# retrieve the key securely from the secrets tab
api_key = userdata.get("GEMINI_API_KEY")

# Configure the client globally; all subsequent calls use this key by default.
genai.configure(api_key=userdata.get("GEMINI_API_KEY"))

# set the persona
sys_instruction = (
    '''
    You are an expert Cybersecurity Risk Analyst for a corporate IT department.
    Your job is to interpret machine language learning model outputs for non-technical business managers.
    Be professional, concise, and focus on risk mitigation.
    Do not use techincal jargon such as "decision trees" or "hyperplanes".
    Explain "why" a URL was flagged based on the provided features.
    '''
)

# Choose a model. 'gemini-2.0-flash' is fast and affordable; 'gemini-2.0-pro' is stronger.
model_name = "gemini-2.0-flash"  # change to 'gemini-2.0-pro' for higher quality


# Create a GenerativeModel instance for repeated calls.
model = genai.GenerativeModel(
    model_name,
      generation_config={
      "temperature": 0.3,    # range: 0-2, Creativity: 0 = deterministic, 2 = creative
      "top_p": 0.85,          # Lower p (e.g., 0.7) → more focused, conservative text. Higher p (e.g., 0.95–0.98) → freer, more creative text.
      "top_k": 40,           # Lower k → more deterministic (less diversity). Higher k → more randomness and variety.
      "max_output_tokens": 150  # Limit output length
  })

=====Explanation=====
def generate_explanation(ml_model, accuracy, report_text):
  # set a prompt
  prompt = f"""
  Briefly explain what {ml_model} is used for in the context of the dataset.
  Provide a brief non-technical overview of these results.
  Provide a a 2-sentence explanation for a business manager about what
  this means for the corporation's security risk.

  - Overall Model Accuracy: {accuracy * 100:.2f}%
  - Detailed report:
  {report_text}
  """

  response = model.generate_content(prompt)
  return response.text

# 1. column names (predictors & target)
# 2. non-null counts (checking for missing data)
# 3. data types (is transformation needed?)
print("\nDataFrame Info:")
df.info()

#=====Identifying target & predictors=====
# descriptive statistics for every numerical columns
print("\nDescriptive Statistics:")
print(df.describe())

# defining the target
target = "phishing"

# every other column is predictor
predictors = [col for col in df.columns if col!=target]
print(f"\nTarget variable: {target}")
print(f"Predictors: {predictors}")

# target variable distribution, is it balanced?
print("\nTarget variable distribution:")
print(df[target].value_counts(normalize=True)) # shows the percentage of each result

# =====Decision Trees=====
# define x (features) and y (target)
x = df[predictors]
y = df[target]

# split the data into testing and training, 80/20; 42 seed ensures you get the same split every time
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

print(f"Training shape: {x_train.shape}") # shows that the model learned from a dataset of 70,917 URLs using 111 features for each URL
print(f"Testing shape: {x_test.shape}") # shows that it tested the performance on a set of 17,730 URLS

# building the decision tree
decision_tree = DecisionTreeClassifier(random_state=42) # using seed 42 to ensure the algorithm is reproducible
decision_tree.fit(x_train, y_train) # fit the decision tree on training data
y_prediction_dt = decision_tree.predict(x_test) # make predictions on the testing data

# evaluating the model
accuracy_dt = accuracy_score(y_test, y_prediction_dt) # test the accuracy
print(f"\nAccuracy: {accuracy_dt * 100:.2f}%") # it should show 95.41% - out of 17,730 test URLs, it classified 95.41% of them as phishing or legitimate

# print the results!
print("\n---Decision Tree Report---")
report_str = classification_report(y_test, y_prediction_dt, target_names=['Phishing (-1)', 'Legitimate (1)'])
print(report_str)
'''
how to interpret the report:
precision - model correctly predicted a site was phishing/legitimate x% of the time; few false positives (rarely accuse a legitimate site of being phishing)
recall - model correctly predicted a site was phishing/legitimate x% of the time; few false negatives (rarely let a real phishing/legitmate site slip by)
f1-score - single number that combines a model's precision and recall into one balanced measure

You use a wide net, and catch 80 of 100 total fish in a lake. That's 80% recall. But you also get 80 rocks in your net. That means 50% precision, half of the net's contents is junk.
'''

# generative AI interpretation
print("\n---Gemini 2.0-flash Interpretation---")
explanation = generate_explanation("Decision Tree", accuracy_dt, report_str)
print(explanation)

# =====Random Forests=====
# creating the random forest; creating 100 decision trees
random_forest = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1) # once again setting seed to 42 for reproducibility

# fit the model to training data
random_forest.fit(x_train, y_train)

# make predictions on the testing data
y_prediction_rf = random_forest.predict(x_test)

# evaluate the model
accuracy_rf = accuracy_score(y_test, y_prediction_rf) # test the accuracy
print(f"\nAccuracy: {accuracy_rf * 100:.2f}%")

# print the results!
print("\n---Random Forest Report---")
report_str_rf = classification_report(y_test, y_prediction_rf, target_names=['Phishing (-1)', 'Legitimate (1)'])
print(report_str_rf)
'''
how to interpret the report:
precision - model correctly predicted a site was phishing/legitimate x% of the time; few false positives (rarely accuse a legitimate site of being phishing)
recall - model correctly predicted a site was phishing/legitimate x% of the time; few false negatives (rarely let a real phishing/legitmate site slip by)
f1-score - single number that combines a model's precision and recall into one balanced measure

You use a wide net, and catch 80 of 100 total fish in a lake. That's 80% recall. But you also get 80 rocks in your net. That means 50% precision, half of the net's contents is junk.
'''
# generative AI interpretation
print("\n---Gemini 2.0-flash Interpretation---")
explanation = generate_explanation("Random Forests", accuracy_rf, report_str_rf)
print(explanation)
