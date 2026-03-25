from src.data_processing.load_data import load_data
from src.data_processing.clean_data import clean_data
from src.data_processing.preprocess import preprocess

from src.ai.sentiment import apply_sentiment
from src.ai.response_generator import apply_responses

from src.database.db_operations import insert_data

from config import CLEAN_DATA_PATH, FINAL_DATA_PATH


def run_pipeline():
    try:
        print("Loading data...")
        df = load_data()

        print("Cleaning data...")
        df = clean_data(df)

        print("Saving cleaned data...")
        df.to_csv(CLEAN_DATA_PATH, index=False)

        print("Preprocessing data...")
        df = preprocess(df)

        print("Applying AI models...")
        df = apply_sentiment(df)
        df = apply_responses(df)

        print("Final columns:", df.columns)

        print("Saving final processed data...")
        df.to_csv(FINAL_DATA_PATH, index=False)

        df = df.drop(columns=['Customer_Email'], errors='ignore')

        print("Inserting into database...")
        insert_data(df)

        print("Pipeline completed successfully!")

    except Exception as e:
        print("Pipeline failed:", e)


if __name__ == "__main__":
    run_pipeline()