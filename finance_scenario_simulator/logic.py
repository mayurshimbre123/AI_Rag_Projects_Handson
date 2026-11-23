"""Business arithmetic is deterministic. The LLM explains, never calculates truth."""
def simulate(base_revenue: float, growth_pct: float, cancellation_pct: float,
             cost_pct: float) -> dict:
    import math
    if not all(math.isfinite(x) for x in (base_revenue, growth_pct, cancellation_pct, cost_pct)):
        raise ValueError("Inputs must be finite numbers")
    if growth_pct < -100:
        raise ValueError("Growth cannot be below -100 percent")
    if base_revenue <= 0: raise ValueError("Base revenue must be positive")
    if not 0 <= cancellation_pct <= 100 or not 0 <= cost_pct <= 100:
        raise ValueError("Cancellation and cost percentages must be between 0 and 100")
    planned=base_revenue*(1+growth_pct/100)
    actual=planned*(1-cancellation_pct/100)
    operating_cost=actual*cost_pct/100
    profit=actual-operating_cost
    return {"base_revenue_m":round(base_revenue,3),"planned_revenue_m":round(planned,3),
            "revenue_after_cancellations_m":round(actual,3),
            "operating_cost_m":round(operating_cost,3),"operating_profit_m":round(profit,3),
            "margin_pct":round(profit/actual*100,2) if actual else 0.0}

def explanation_prompt(results: dict) -> str:
    return ("You are a finance analysis assistant. The numbers below were calculated in Python. "
            "Do not change them. Explain the causes, assumptions, and one possible risk. "
            "Treat the scenario as synthetic; do not present as real financial data.\n"+str(results))
