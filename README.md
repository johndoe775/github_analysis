# github_analysis

# Graph App: Automated Cold Email Generator

This repository contains a Streamlit application that leverages LangGraph and LLMs to generate cold emails or other HR-related outputs based on a user's resume, job description, and information about a recruiter. The workflow is defined using a graph-based approach, allowing for flexible and modular prompt engineering.

## Features

- Upload your resume (PDF, DOCX, or TXT)
- Enter a job description and personal information
- Select from multiple prompt options (defined in `src/prompts.yaml`)
- Generates a tailored output (e.g., cold email) using an LLM and prompt chaining

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/github_analysis.git
cd github_analysis
```

### 2. Create and Activate a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

> **Note:** If `requirements.txt` is missing, install the main dependencies manually:
> ```bash
> pip install streamlit langchain langgraph python-dotenv pyyaml PyPDF2
> ```

### 4. Set Up Environment Variables

Create a `.env` file in the root directory and add your Groq API key:

```
groq=YOUR_GROQ_API_KEY
```

### 5. Prepare Prompt Templates

Ensure you have a `src/prompts.yaml` file with your prompt templates and tool definitions.

### 6. Run the Application

```bash
streamlit run app.py
```

The app will open in your browser. Upload your resume, fill in the job description and personal info, select an option, and click "Run" to generate your output.

---

## File Structure

- `app.py` - Main Streamlit application
- `src/prompts.yaml` - Prompt templates and tool definitions
- `data/` - Directory for job descriptions and sample resumes

## Example Usage

1. Upload your resume as a PDF.
2. Enter the job description and your personal information.
3. Select the desired prompt/tool from the dropdown.
4. Click "Run" to generate a cold email or other output.

---

## License

MIT License

---

## Acknowledgements

- [LangChain](https://github.com/langchain-ai/langchain)
- [LangGraph](https://github.com/langchain-ai/langgraph)
- [Streamlit](https://streamlit.io/)