import pandas as pd
import joblib
from database_operation import inference_ip



def recommendation(client_id):
    # Load the trained model pipeline
    model_pipeline = joblib.load("product_recommendation_model.pkl")

    # # Load new or test data (without the target column)
    # df_new = pd.read_csv("testing.csv")  # For demo, using some data
    # X_new = df_new.drop("recommended_product", axis=1)

    # Predict
    predictions = model_pipeline.predict(inference_ip(client_id))

    recommended_product = predictions[0]
    if recommended_product == 'FD':
        op = 'Recommended product is Fixed Deposit'
    else:
        op = "Recommended product is " + recommended_product
    return op


