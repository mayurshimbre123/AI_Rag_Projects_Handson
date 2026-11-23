import gradio as gr
from logic import ROLE_TOPICS, build_question_prompt, build_feedback_prompt
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from ibm_client import generate

def ask(role, difficulty, topic):
    prompt=build_question_prompt(role,difficulty,topic)
    try: return generate(prompt), prompt
    except Exception as exc: raise gr.Error(f"IBM request unavailable: {type(exc).__name__}. Check the course environment.") from None

def assess(question, answer):
    if not question.strip() or not answer.strip(): return "Please generate a question and write an answer first."
    try:return generate(build_feedback_prompt(question,answer), max_new_tokens=450)
    except Exception as exc:return f"IBM request unavailable: {type(exc).__name__}."

with gr.Blocks(theme=gr.themes.Soft(primary_hue="indigo"),title="AI Interview Arena") as demo:
    gr.Markdown("# AI Interview Arena\nA learning project: inspect the prompts and critique the LLM feedback.")
    with gr.Row():
        role=gr.Dropdown(list(ROLE_TOPICS),value="AI Engineer",label="Role")
        difficulty=gr.Radio(["Beginner","Intermediate","Advanced"],value="Intermediate",label="Difficulty")
        topic=gr.Textbox(value="RAG evaluation",label="Topic (editable)")
    question=gr.Textbox(label="Generated technical question",lines=3)
    prompt=gr.Textbox(label="Prompt sent to IBM",lines=4)
    gr.Button("Generate question",variant="primary").click(ask,[role,difficulty,topic],[question,prompt])
    answer=gr.Textbox(label="My answer",lines=6)
    feedback=gr.Markdown(label="Evaluation")
    gr.Button("Evaluate my answer").click(assess,[question,answer],feedback)
if __name__ == "__main__":demo.launch(server_name="127.0.0.1",server_port=7860,share=False)
