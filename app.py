import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler, LabelEncoder

path = "roomeet_balanced.csv"
try:
    df = pd.read_csv(path)
except FileNotFoundError:
    st.error(f"CSV file not found at: {path}")
    st.stop()

numerical_features = ["Age", "Budget Range (in INR)", "Cleanliness Level", "Fitness Level", "Commuting Distance (km)"]
categorical_features = [
    "Gender", "Occupation", "Smoking Preference", "Pets", "Noise Tolerance",
    "Social Habits", "Sleep Schedule", "Dietary Preference", "Work-from-Home", "Preferred Locations"
]

original_df = df.copy()

df[categorical_features] = df[categorical_features].astype(str)

def get_preprocessors():
    scaler = MinMaxScaler()
    scaler.fit(df[numerical_features])
    
    encoders = {}
    
    for col in categorical_features:
        le = LabelEncoder()
        le.fit(df[col])
        encoders[col] = le
    
    return scaler, encoders

scaler, encoders = get_preprocessors()

st.title("🏡 Roommate Recommendation System")

st.sidebar.header("Your Preferences")

age = st.sidebar.slider("Age", min_value=18, max_value=40, value=25)
budget = st.sidebar.slider("Budget Range (in INR)", min_value=5000, max_value=30000, value=15000, step=500)
cleanliness = st.sidebar.slider("Cleanliness Level", min_value=1, max_value=5, value=3)
fitness = st.sidebar.slider("Fitness Level", min_value=1, max_value=5, value=3)
commute = st.sidebar.slider("Commuting Distance (km)", min_value=0, max_value=10, value=5)

gender = st.sidebar.selectbox("Gender", original_df["Gender"].unique())
occupation = st.sidebar.selectbox("Occupation", original_df["Occupation"].unique())
smoking = st.sidebar.selectbox("Smoking Preference", original_df["Smoking Preference"].unique())
pets = st.sidebar.selectbox("Pets", original_df["Pets"].unique())
noise_tolerance = st.sidebar.selectbox("Noise Tolerance", original_df["Noise Tolerance"].unique())
social_habits = st.sidebar.selectbox("Social Habits", original_df["Social Habits"].unique())
sleep_schedule = st.sidebar.selectbox("Sleep Schedule", original_df["Sleep Schedule"].unique())
dietary_preference = st.sidebar.selectbox("Dietary Preference", original_df["Dietary Preference"].unique())
work_from_home = st.sidebar.selectbox("Work-from-Home", original_df["Work-from-Home"].unique())
preferred_location = st.sidebar.selectbox("Preferred Locations", original_df["Preferred Locations"].unique())

user_input = {
    "Age": age,
    "Budget Range (in INR)": budget,
    "Cleanliness Level": cleanliness,
    "Fitness Level": fitness,
    "Commuting Distance (km)": commute,
    "Gender": gender,
    "Occupation": occupation,
    "Smoking Preference": smoking,
    "Pets": pets,
    "Noise Tolerance": noise_tolerance,
    "Social Habits": social_habits,
    "Sleep Schedule": sleep_schedule,
    "Dietary Preference": dietary_preference,
    "Work-from-Home": work_from_home,
    "Preferred Locations": preferred_location
}

if st.sidebar.button("Find Roommates", type="primary"):
    try:
        with st.spinner("Finding your ideal roommates..."):
            filtered_df = df[(df["Gender"] == user_input["Gender"]) & 
                             (df["Preferred Locations"] == user_input["Preferred Locations"]) &
                             (df["Budget Range (in INR)"] <= user_input["Budget Range (in INR)"])]
            
            if len(filtered_df) == 0:
                st.warning("No matches found with the same gender, location, and within your budget limit. Showing results with matching gender and location only.")
                filtered_df = df[(df["Gender"] == user_input["Gender"]) & 
                                (df["Preferred Locations"] == user_input["Preferred Locations"])]
                
                if len(filtered_df) == 0:
                    st.warning("No matches found with your gender and location. Showing results with matching gender only.")
                    filtered_df = df[df["Gender"] == user_input["Gender"]]
                    
                    if len(filtered_df) == 0:
                        st.error("No matches found with your gender. Please adjust your preferences.")
                        st.stop()
            
            user_numerical = np.array([[
                user_input[feat] for feat in numerical_features
            ]])
            user_numerical_scaled = scaler.transform(user_numerical)[0]
            
            filtered_indices = filtered_df.index.tolist()
            dataset_numerical_scaled = scaler.transform(filtered_df[numerical_features])
            
            all_distances = []
            
            for i, idx in enumerate(filtered_indices):
                num_diff = user_numerical_scaled - dataset_numerical_scaled[i]
                num_squared_diff = np.sum(num_diff ** 2)

                cat_diff = 0
                cat_count = 0
                for feat in categorical_features:
                    if feat in ["Gender", "Preferred Locations"]:
                        continue
                        
                    cat_count += 1

                    try:
                        user_val = encoders[feat].transform([str(user_input[feat])])[0]
                    except ValueError:
                        user_val = 0

                    dataset_val = encoders[feat].transform([str(filtered_df.loc[idx, feat])])[0]
                    
                    if user_val != dataset_val:
                        cat_diff += 1
                
                cat_norm = cat_diff / cat_count if cat_count > 0 else 0
                
                total_distance = np.sqrt(num_squared_diff) + cat_norm
                all_distances.append((idx, total_distance))
            
            all_distances.sort(key=lambda x: x[1])
            
            num_recommendations = min(5, len(all_distances))
            nearest_indices = [x[0] for x in all_distances[:num_recommendations]]
            nearest_distances = [x[1] for x in all_distances[:num_recommendations]]

            max_distance = max([x[1] for x in all_distances]) if all_distances else 1
            
            recommendations = []
            for i in range(len(nearest_indices)):
                idx = nearest_indices[i]
                distance = nearest_distances[i]
                
                match_score = 100 * (1 - distance / max_distance) if max_distance > 0 else 100
                
                rec = original_df.iloc[idx].copy()
                rec_dict = rec.to_dict()
                rec_dict['Match Score'] = round(match_score, 1)
                recommendations.append(rec_dict)
            
            recommendations_df = pd.DataFrame(recommendations)

            recommendations_df = recommendations_df.sort_values('Match Score', ascending=False)
            
            st.write("Recommended Roommates")
            
            columns = ['Match Score'] + [col for col in recommendations_df.columns if col != 'Match Score']
            st.dataframe(recommendations_df[columns])
            
    except Exception as e:
        st.error(f"Error in recommendation system: {str(e)}")
        import traceback
        st.code(traceback.format_exc())
else:
    st.info("👈 Fill in your preferences and click 'Find Roommates' to get started!")