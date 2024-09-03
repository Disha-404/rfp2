import streamlit as st
from data_processing.data_loader import load_data
from data_processing.excel_utils import unmerge_cells, concatenate_requirements, save_to_excel
from generation.response_generator import generate_response
from retrieval.similarity import find_most_similar
from utils.client import get_openai_client
import os
import numpy as np
import torch
import re


def main():
    st.title("RFP Response Generator")
    
    uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx"])
    
    if uploaded_file:
        df = load_data(uploaded_file)
        df = unmerge_cells(df)
        df = concatenate_requirements(df)

        # Load embeddings
        embeddings_file = 'embeddings.npy'
        if os.path.exists(embeddings_file):
            embeddings = np.load(embeddings_file).astype(np.float32)
            embeddings = torch.tensor(embeddings).to('cpu')
        else:
            st.error("Embeddings file not found. Please upload a file to create embeddings first.")
            return

        requirements = df['requirement'].tolist()
        responses = df['Response'].tolist()
        comments = df['Vendor Comment'].tolist()
        module = df['Module'].tolist()

        responses_list = []
        comments_list = []

        for requirement in df['requirement']:
            try:
                similar_texts, indices = find_most_similar(requirement, embeddings, requirements, get_openai_client())
                similar_responses = [responses[i] for i in indices]
                similar_comments = [comments[i] for i in indices]
                similar_module = [module[i] for i in indices]

                generated_response = generate_response(requirement, similar_texts, similar_responses, similar_comments, similar_module)

                response_match = re.search(r'Response:\s*(.*?)(?:\n|$)', str(generated_response))
                response = response_match.group(1).strip() if response_match else 'No response found'

                comment_match = re.search(r'Comment:\s*(.*?)(?:\n|$)', str(generated_response), re.DOTALL)
                comment = comment_match.group(1).strip() if comment_match else 'No comment found'

                responses_list.append(response)
                comments_list.append(comment)
            except Exception as e:
                st.error(f"Error processing requirement: {e}")
                responses_list.append('Error')
                comments_list.append('Error')

        df['response'] = responses_list
        df['comment'] = comments_list

        output = save_to_excel(df)
        st.download_button(
            label="Download Updated File",
            data=output,
            file_name="updated_rfp.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

if __name__ == "__main__":
    main()
