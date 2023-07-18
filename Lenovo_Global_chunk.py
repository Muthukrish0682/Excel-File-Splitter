import pandas as pd
import streamlit as st
import io

def split_excel_file(input_file, chunk_size):
    # Read the Excel file into a pandas DataFrame
    df = pd.read_excel(input_file, keep_default_na=False, na_values='')

    # Get the total number of rows in the DataFrame
    total_rows = df.shape[0]

    # Calculate the number of chunks required
    num_chunks = total_rows // chunk_size + (total_rows % chunk_size > 0)

    # Split the DataFrame into chunks
    chunks = [df[i*chunk_size:(i+1)*chunk_size] for i in range(num_chunks)]

    # Save each chunk as a separate Excel file
    output_files = []
    for i, chunk in enumerate(chunks):
        output_file = io.BytesIO()
        chunk.to_excel(output_file, index=False)
        output_files.append(output_file)

    return output_files

# Streamlit app
st.title("👋 Excel File Splitter")
st.write("Version 2.0")

# Chunk size input
chunk_size = st.number_input("Enter the chunk size", min_value=1, step=1)

# File upload
file = st.file_uploader("Upload an Excel file", type=["xlsx", "xls"])

# Splitting and generating output files
if chunk_size and file:
    chunks = split_excel_file(file, chunk_size)
    st.success("Excel file has been split into chunks!")

    # Download buttons for each chunk file
    st.subheader("Download Chunks")
    for i, chunk in enumerate(chunks):
        st.download_button(
            label=f"Download Chunk {i+1}",
            data=chunk.getvalue(),
            file_name=f"output_chunk_{i+1}.xlsx"
        )
