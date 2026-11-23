import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
def module(name, path):
    import sys
    spec = importlib.util.spec_from_file_location(name, ROOT / path)
    m = importlib.util.module_from_spec(spec)
    sys.modules[name] = m
    spec.loader.exec_module(m)
    return m

interview = module("interview_logic", "interview_arena/logic.py")
finance = module("finance_logic", "finance_scenario_simulator/logic.py")
rag = module("rag_logic", "rag_evidence_detective/logic.py")

def test_interview():
    assert "RAG evaluation" in interview.build_question_prompt("AI Engineer", "Intermediate", "RAG evaluation")
    assert "Correctness" in interview.build_feedback_prompt("What?", "Because")

def test_finance():
    r = finance.simulate(100, 10, 20, 70)
    assert r["planned_revenue_m"] == 110
    assert r["revenue_after_cancellations_m"] == 88
    assert r["operating_profit_m"] == 26.4
    assert r["margin_pct"] == 30
    for values in [(100,-101,0,0),(float("nan"),0,0,0),(100,0,101,0)]:
        try: finance.simulate(*values)
        except ValueError: pass
        else: raise AssertionError(f"Accepted invalid inputs: {values}")

def test_rag():
    passages = rag.chunk_paragraphs({"sample":"Revenue fell.\n\nMajor customers cancelled contracts."})
    assert len(passages) == 2
    results = rag.retrieve("Which customers cancelled contracts?", passages, 1)
    assert results[0][0].text.startswith("Major customers")
    assert results[0][1] == 3
    assert "score" in rag.build_context(results)

if __name__ == "__main__":
    for name, function in list(globals().items()):
        if name.startswith("test_") and callable(function):
            function()
            print(name + " PASS")
