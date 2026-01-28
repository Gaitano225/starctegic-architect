import yaml
import re
from typing import List, Dict, Any
from pydantic import BaseModel

class Rule(BaseModel):
    id: str
    condition: str
    recommendation: str
    justification: str

class RulesEngine:
    def __init__(self, rules_path: str):
        self.rules = self._load_rules(rules_path)

    def _load_rules(self, path: str) -> List[Rule]:
        with open(path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
            return [Rule(**r) for r in data.get('rules', [])]

    def evaluate(self, context: Dict[str, Any]) -> Dict[str, Any]:
        recommendations = []
        applied_ids = []
        for rule in self.rules:
            if self._check_condition(rule.condition, context):
                recommendations.append(rule.dict())
                applied_ids.append(rule.id)
        return {
            "recommendations": recommendations,
            "applied_rule_ids": applied_ids
        }

    def _check_condition(self, condition: str, context: Dict[str, Any]) -> bool:
        """
        Evaluate a rule condition against a given context.
        Supports: ==, !=, >, <, >=, <=, 'in', 'and', 'or', 'not', True, False
        """
        # Security: Clean the condition and check against allowed context keys
        # For MVP, we use eval with a restricted global/local environment.
        try:
            # Prepare context for eval (ensure booleans and strings are handled)
            return eval(condition, {"__builtins__": None}, context)
        except Exception as e:
            print(f"Evaluation error for rule condition '{condition}': {e}")
            return False
