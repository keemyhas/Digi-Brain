# Digi-Brain Controlled Benchmark Metrics Calculator
# Implements REQ-7.2

from typing import Dict, Any, List

def calculate_benchmark_metrics(trial_results: List[Dict[str, Any]]) -> Dict[str, Any]:
    total_tasks = len(trial_results)
    if total_tasks == 0:
        return {}

    completed = sum(1 for r in trial_results if r.get("task_completed", False))
    regressions = sum(1 for r in trial_results if r.get("regression_introduced", False))
    total_constraints = sum(r.get("total_constraints", 1) for r in trial_results)
    complied_constraints = sum(r.get("complied_constraints", 1) for r in trial_results)
    
    unauthorized_attempts = sum(r.get("unauthorized_attempts", 0) for r in trial_results)
    unauthorized_executed = sum(r.get("unauthorized_executed", 0) for r in trial_results)
    
    relevant_items = sum(r.get("relevant_items", 1) for r in trial_results)
    retrieved_relevant = sum(r.get("retrieved_relevant", 1) for r in trial_results)
    total_retrieved = sum(r.get("total_retrieved", 1) for r in trial_results)

    total_tokens = sum(r.get("token_overhead", 0) for r in trial_results)

    return {
        "task_completion_rate": round(completed / total_tasks, 4),
        "regression_rate": round(regressions / total_tasks, 4),
        "constraint_compliance": round(complied_constraints / total_constraints, 4) if total_constraints > 0 else 1.0,
        "unauthorized_attempts": unauthorized_attempts,
        "unauthorized_executed": unauthorized_executed,
        "memory_recall": round(retrieved_relevant / relevant_items, 4) if relevant_items > 0 else 1.0,
        "irrelevant_retrieval_rate": round((total_retrieved - retrieved_relevant) / total_retrieved, 4) if total_retrieved > 0 else 0.0,
        "avg_token_overhead": round(total_tokens / total_tasks, 1)
    }
