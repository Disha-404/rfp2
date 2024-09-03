def save_processed_file(df):
    from io import BytesIO
    output = BytesIO()
    df.to_excel(output, index=False)
    output.seek(0)
    return output
