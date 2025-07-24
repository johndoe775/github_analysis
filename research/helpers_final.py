import streamlit as st
from PyPDF2 import PdfReader
import os
import yaml

# from langchain.document_loaders.pdf import PyPDFReader
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_core.messages import AIMessage

load_dotenv()
api_key = os.environ["groq"]

# Initialize LLM
class LLM:
    def __init__(self, model="llama-3.3-70b-versatile", temperature=0, max_tokens=None, timeout=None, max_retries=2, api_key=api_key):
        self.params = {
            "model": model,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "timeout": timeout,
            "max_retries": max_retries,
            "api_key": api_key,
        }
        self.llm = ChatGroq(**self.params)

class functions:
    def __init__(self, data: dict, resume: str, job_description: str, personal_info: str):
        self.data = data
        self.resume = resume
        self.job_description = job_description
        self.personal_info = personal_info 
        class State(TypedDict):
            messages: Annotated[list, add_messages]
            option: str

        self.graph = StateGraph(State)

        def intro1(state: State) -> dict:
            state["option"] = st.session_state["option"]
            state["messages"] = [
                AIMessage(content=f"Selected option is {state['option']}.")
            ]
            return state

        def llm_fx(state: State) -> dict:
            key = state["option"]
            input_variables = list(data[key]["inputs"].keys())
            template = data[key]["prompt"].format(
                resume=resume, job_description=job_description, personal_info=personal_info
            )
            prompt_template = PromptTemplate(
                input_variables=input_variables, template=template
            )
            chain = prompt_template | LLM().llm
            response = chain.invoke(data[key]["inputs"]).content
            state["messages"].append(AIMessage(content=response))
            return state

        self.graph.add_node(START, intro1)
        self.graph.add_node("llm_fx", llm_fx)
        self.graph.add_edge(START, "llm_fx")
        self.graph.add_edge("llm_fx", END)

        self.graph1 = self.graph.compile()

        self.final_state = self.graph1.invoke({"messages": ["Welcome to the graph!"]})
        self.final_response = self.final_state["messages"][-1].content
        
