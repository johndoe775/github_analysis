import streamlit as st
from PyPDF2 import PdfReader
import os
import yaml
from src.helpers_final import LLM, fx

# from langchain.document_loaders.pdf import PyPDFReader
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_core.messages import AIMessage

# Load environment variables
load_dotenv()
api_key = os.environ["groq"]

# Initialize LLM
llm = LLM().llm


def main():
    st.title("Graph App")

    with open("/workspaces/github_analysis/src/prompts.yaml", "r") as file:
        data = yaml.safe_load(file)

    options = list(data.keys())
    st.selectbox("Select an option", options, key="option")

    uploaded_resume = st.file_uploader(
        "Upload your resume", type=["pdf", "docx", "txt"]
    )

    if uploaded_resume is not None:

        # Read the PDF file
        if uploaded_resume.type == "application/pdf":
            # Read the PDF file
            pdf_reader = PdfReader(uploaded_resume)

            # Extract the content
            resume = ""
            for page in pdf_reader.pages:
                resume += page.extract_text()
    else:
        resume = ""

    job_description = st.text_area("Enter the job description")
    personal_info = st.text_area("Enter info about the person")

    if st.button("Run"):
        obj = fx(
            data=data,
            resume=resume,
            job_description=job_description,
            personal_info=personal_info,
            option=st.session_state["option"],
        )
        response = obj.create_graph_and_run()
        st.write("Final Result:", response)


if __name__ == "__main__":
    main()
