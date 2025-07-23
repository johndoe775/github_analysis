import streamlit as st
from PyPDF2 import PdfReader
import os
import yaml
#from langchain.document_loaders.pdf import PyPDFReader
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
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    api_key=api_key
)

def run_graph(data: dict, resume: str, job_description: str, personal_info: str) -> None:
    class State(TypedDict):
        messages: Annotated[list, add_messages]
        option: str

    graph = StateGraph(State)

    def intro1(state: State) -> dict:
        state["option"] = st.session_state["option"]
        state["messages"] = [AIMessage(content=f"Selected option is {state['option']}.")]
        return state

    def llm_fx(state: State) -> dict:
        key = state["option"]
        input_variables = list(data[key]["inputs"].keys())
        template = data[key]["prompt"].format(
            resume=resume, job_description=job_description, personal_info=personal_info
        )
        prompt_template = PromptTemplate(
            input_variables=input_variables,
            template=template
        )
        chain = prompt_template | llm
        response = chain.invoke(data[key]["inputs"]).content
        state["messages"].append(AIMessage(content=response))
        return state

    graph.add_node("input", intro1)
    graph.add_node("llm", llm_fx)
    graph.add_edge(START, "input")
    graph.add_edge("input", "llm")
    graph.add_edge("llm", END)

    graph1 = graph.compile()

    final_state = graph1.invoke({"messages": ["Welcome to the graph!"]})
    final_response = final_state["messages"][-1].content  
    return final_response

def main():
    st.title("Graph App")

    with open('/workspaces/github_analysis/src/prompts.yaml', 'r') as file:
        data = yaml.safe_load(file)

    options = list(data.keys())
    st.selectbox("Select an option", options, key="option")

    uploaded_resume = st.file_uploader("Upload your resume", type=["pdf", "docx", "txt"])

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
        resume=""

    job_description = st.text_area("Enter the job description")
    personal_info = st.text_area("Enter info about the person")

    if st.button("Run"):
        response = run_graph(data, resume, job_description, personal_info)
        st.write("Final Result:", response)

if __name__ == "__main__":
    main()
