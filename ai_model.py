import pandas as pd
from sklearn.preprocessing import LabelEncoder, MinMaxScaler

# Simple AI Scoring Model
class ApplicantModel:
    def __init__(self):
        self.scaler = MinMaxScaler()
        self.encoder = LabelEncoder()

    def preprocess(self, applicants):
        # Convert data to DataFrame
        df = pd.DataFrame(applicants)
        
        # Calculate skill strength (number of skills)
        df["skill_score"] = df["skills"].apply(lambda x: len(x))
        
        # Encode education level (for scoring)
        df["education_score"] = self.encoder.fit_transform(df["education"])
        
        # Combine features
        df["total_score"] = (
            df["experience"] * 0.5 +
            df["skill_score"] * 0.3 +
            df["education_score"] * 0.2
        )

        # Normalize score between 0 and 1
        df["final_score"] = self.scaler.fit_transform(df[["total_score"]])
        return df

    def rank_applicants(self, applicants):
        df = self.preprocess(applicants)
        ranked = df.sort_values(by="final_score", ascending=False)
        return ranked.to_dict(orient="records")

# Create model instance
ai_model = ApplicantModel()
