import yaml
from langchain_community.document_loaders import PyPDFLoader

resume = ""


def docu_loaders():
    with open("/workspaces/github_analysis/data/job_description.txt", "r") as file:
        job_description = file.read()
    loader = PyPDFLoader("/workspaces/github_analysis/data/resume_with_capg.pdf")
    documents = loader.load()
    for i in documents:
        resume += i.page_content.strip()


def intro():
    with open("/workspaces/github_analysis/src/prompts.yaml", "r") as file:
        data = yaml.safe_load(file)
    print("*" * 100)
    for i, j in enumerate(data.keys()):
        print(f"{i+1}. {j}")


def inputs():
    i = input("Enter the number corresponding to the key you want to use: ")
    print("selected number is ", int(i))
    key = list(data.keys())[int(i) - 1]
    return key
