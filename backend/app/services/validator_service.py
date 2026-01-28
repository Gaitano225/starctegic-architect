from typing import Dict, Any, List

class PreFlightValidator:
    """
    Validates questionnaire answers for consistency before report generation.
    """
    
    @staticmethod
    def validate(answers: Dict[str, Any]) -> List[Dict[str, str]]:
        warnings = []
        
        budget = answers.get("budget_amount", 0)
        users = answers.get("users_expected", 0)
        is_microservices = answers.get("architecture") == "microservices"
        
        # 1. Budget vs Architecture
        if is_microservices and budget < 5000000:
            warnings.append({
                "id": "WARN-BUDG-001",
                "message": "Le budget est potentiellement trop faible pour une architecture Microservices complexe."
            })
            
        # 2. Scale vs Platform
        if users > 100000 and answers.get("hosting") == "vps":
            warnings.append({
                "id": "WARN-SCALE-001",
                "message": "Un VPS unique pourrait être un goulot d'étranglement pour plus de 100 000 utilisateurs."
            })
            
        # 3. Mobile vs WebView
        if answers.get("needs_mobile") and answers.get("budget") == "low":
            warnings.append({
                "id": "WARN-MOB-001",
                "message": "Conseil: Priorisez une PWA (Web App) au lieu d'une app native pour respecter un budget restreint."
            })

        return warnings
