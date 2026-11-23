import gradio as gr
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from ibm_client import generate
from logic import chunk_paragraphs,retrieve,build_context,answer_prompt
SAMPLE=(Path(__file__).parent/"sample_documents.txt").read_text(encoding="utf-8")

def investigate(question,source_text,k,use_llm):
    passages=chunk_paragraphs({"user_text":source_text})
    matches=retrieve(question,passages,int(k))
    context=build_context(matches)
    rows=[{"passage_id":p.id,"overlap_score":score,"text":p.text} for p,score in matches]
    prompt=answer_prompt(question,context)
    if not use_llm:return rows,context,"IBM inference disabled. Inspect retrieved passages first.",prompt
    try:return rows,context,generate(prompt),prompt
    except Exception as exc:return rows,context,f"IBM request unavailable: {type(exc).__name__}.",prompt

with gr.Blocks(theme=gr.themes.Soft(primary_hue="blue"),title="RAG Evidence Detective") as demo:
    gr.Markdown("# RAG Evidence Detective\nLearn what a retriever actually sends to an LLM. This first version uses **keyword overlap**, not embeddings.")
    with gr.Row():
        with gr.Column():
            source=gr.Textbox(value=SAMPLE,lines=13,label="Source documents (editable)")
            question=gr.Textbox(value="What caused the aerospace revenue decline?",label="Question")
            k=gr.Slider(1,6,value=2,step=1,label="Top K passages")
            use_llm=gr.Checkbox(value=False,label="Send retrieved evidence to IBM watsonx")
            run_button=gr.Button("Investigate",variant="primary")
        with gr.Column():
            retrieved=gr.JSON(label="Retrieved passages with measured lexical scores")
            context=gr.Textbox(lines=7,label="Exact context passed to model")
            answer=gr.Markdown(label="LLM answer")
            prompt=gr.Textbox(lines=7,label="Final constructed prompt")
    run_button.click(investigate,[question,source,k,use_llm],[retrieved,context,answer,prompt])
if __name__=="__main__":demo.launch(server_name="127.0.0.1",server_port=7860,share=False)
