import pickle
import os
from sklearn.ensemble import RandomForestClassifier

models_dir = os.path.join(os.path.dirname(__file__), "models_repo")
os.makedirs(models_dir, exist_ok=True)

# 1. Dummy Model 1: Churn Predictor
m1 = RandomForestClassifier(n_estimators=10, random_state=42)
with open(os.path.join(models_dir, "churn_rf_v1.pkl"), "wb") as f:
    pickle.dump({"model": m1, "name": "Samyak_User_Churn_RF", "version": "1.0.0"}, f)

# 2. Dummy Model 2: Medical Imaging Classifier
with open(os.path.join(models_dir, "mri_efficientnet_b0_v2.bin"), "wb") as f:
    f.write(b"SAMPLE_WEIGHTS_TENSOR_EFFICIENTNET_B0_PERCEPTUAL_HASH_AUDITED_96_ACCURACY")

print("Created sample models in models_repo/")
