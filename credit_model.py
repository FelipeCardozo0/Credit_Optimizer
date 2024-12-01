import pandas as pd
import os


def analyze_credit(file_path):
    try:
        # Specify encoding to handle different file formats
        # Change encoding if necessary
        df = pd.read_csv(file_path, encoding='utf-8')
    except UnicodeDecodeError:
        # Retry with a common alternative encoding
        # Handles non-UTF-8 encoded files
        df = pd.read_csv(file_path, encoding='latin1')

    # Check for required columns
    required_columns = {'credit_score', 'income', 'debt_to_income_ratio'}
    if not required_columns.issubset(df.columns):
        raise ValueError("Missing required columns in the uploaded file.")

    # Simple loan decision logic
    df['loan_decision'] = df['credit_score'].apply(
        lambda x: 'Approved' if x >= 700 else 'Denied'
    )

    # Save the processed file
    output_path = os.path.join(
        os.path.dirname(file_path),
        'processed_' + os.path.basename(file_path)
    )
    df.to_csv(output_path, index=False)
    return output_path
