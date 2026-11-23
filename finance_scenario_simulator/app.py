import gradio as gr
import pandas as pd
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from ibm_client import generate
from logic import simulate, explanation_prompt

def run(base,growth,cancellation,cost,use_llm):
    try:
        results=simulate(base,growth,cancellation,cost)
        chart = pd.DataFrame({"measure": ["Planned revenue", "Revenue after cancellations", "Operating cost", "Operating profit"], "million_usd": [results["planned_revenue_m"], results["revenue_after_cancellations_m"], results["operating_cost_m"], results["operating_profit_m"]]})
        if not use_llm:return results,chart,"AI explanation disabled: these numbers are computed in Python."
        try:return results,chart,generate(explanation_prompt(results))
        except Exception as exc:return results,chart,f"IBM explanation unavailable: {type(exc).__name__}. The computed numbers are still valid."
    except Exception as exc:return {},pd.DataFrame({"measure": [], "million_usd": []}),f"Invalid input: {exc}"

with gr.Blocks(theme=gr.themes.Soft(primary_hue="emerald"),title="Finance Scenario Simulator") as demo:
    gr.Markdown("# Finance Scenario Simulator\n**Synthetic scenario only** · Python calculates; the LLM explains.")
    with gr.Row():
        base=gr.Slider(100,2000,value=740,step=10,label="Base revenue (million USD)")
        growth=gr.Slider(-40,40,value=7,step=1,label="Growth %")
    with gr.Row():
        canc=gr.Slider(0,80,value=8,step=1,label="Revenue cancellations %")
        cost=gr.Slider(0,100,value=70,step=1,label="Operating cost as % of revenue")
    use_llm=gr.Checkbox(value=False,label="Ask IBM watsonx to explain the results")
    numbers=gr.JSON(label="Computed financial outcomes")
    chart=gr.BarPlot(x="measure", y="million_usd", title="Scenario breakdown", tooltip=["measure", "million_usd"])
    commentary=gr.Markdown(label="Explanation")
    gr.Button("Simulate",variant="primary").click(run,[base,growth,canc,cost,use_llm],[numbers,chart,commentary])
if __name__=="__main__":demo.launch(server_name="127.0.0.1",server_port=7860,share=False)
