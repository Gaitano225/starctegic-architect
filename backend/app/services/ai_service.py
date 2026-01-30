import os
from typing import List, Dict, Any
import google.generativeai as genai

class AIService:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-1.5-flash')

    async def enhance_report(self, 
                             project_data: Dict[str, Any], 
                             recommendations: List[Dict[str, Any]],
                             user_plan: str = "FOUNDER") -> str:
        """
        Uses Gemini to transform bullet-point recommendations into a professional Business Case narrative.
        Content is gated based on user subscription plan.
        """
        if not self.api_key:
            return "Note : L'IA d'analyse n'est pas activée (Clé API manquante). Les recommandations techniques ci-dessous restent valides."

        prompt = self._build_prompt(project_data, recommendations, user_plan)
        
        try:
            # Using generate_content (synchronous version or wrapper if needed)
            # In a real async environment, we'd use generate_content_async
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error generating AI enhancement: {str(e)}"

    def _build_prompt(self, project_data: Dict[str, Any], recommendations: List[Dict[str, Any]], user_plan: str) -> str:
        answers = project_data.get('answers', {})
        rules_str = "\n".join([f"- [Prop {r['id']}]: {r['recommendation']} (Justification: {r['justification']})" for r in recommendations])
        
        # Architecture Level Gating
        arch_instructions = self._get_architecture_scope(user_plan)
        
        return f"""
        Rôle : Tu es le "Cerveau" d'un Cabinet de Conseil Stratégique et Architectural Senior (inspiré par McKinsey, BCG et Palantir).
        Mission : Rédiger un "Executive Summary" et une "Analyse de Cohérence Architecturale" pour le Business Case '{project_data.get('name')}'.
        
        POSTURE : 
        - Rigoureux, auditant, finançable.
        - Tu ne vends pas du rêve, tu valides une viabilité technique et économique.
        - Focus sur le marché Africain (contraintes locales, infrastructures, régulations).

        DONNÉES D'ENTRÉE (Questionnaire Fondamental) :
        1. Intention & Contexte : {answers.get('problem_statement')} (Impact : {answers.get('stakeholders')})
        2. Pays de déploiement : {answers.get('deployment_zone')} (Urgence : {answers.get('criticality')})
        3. Modèle économique : {answers.get('value_creation')} (Revenus : {answers.get('revenue_model')})
        4. Maturité & Existant : {answers.get('existing_assets')} (Points de friction : {answers.get('friction_points')})
        5. Maturité numérique : {answers.get('digital_maturity')}
        6. Contraintes & Risques : {answers.get('constraints')} (Risque d'échec : {answers.get('failure_consequences')})
        7. Scalabilité : {answers.get('scalability_needs')}
        8. Données & IA : Critiques : {answers.get('critical_data')} (Automatisation : {answers.get('ai_automation_level')})
        9. Sécurité : Sensibilité : {answers.get('sensitive_data')}
        10. Gouvernance : Responsabilité : {answers.get('final_accountability')}
        11. Exécution : Compétences : {answers.get('internal_skills')} (Contrôle : {answers.get('monitoring_level')})
        12. Horizon : {answers.get('roadmap_horizon')}
        
        PILIER TECHNIQUES (Sortie du moteur de décision) :
        {rules_str}
        
        {arch_instructions}
        
        STRUCTURE ATTENDUE DU RAPPORT (En Français) :
        1. RÉSUMÉ EXÉCUTIF : Synthèse de la valeur et de l'alignement stratégique.
        2. ANALYSE PAYS & SECTEUR : Analyse approfondie des défis et opportunités pour {answers.get('target_country')}.
        3. COHÉRENCE ARCHITECTURALE : Justification de pourquoi l'architecture proposée est la seule viable.
        4. ROADMAP STRATÉGIQUE (Horizon {answers.get('roadmap_horizon')}) : Étapes clés de succès.
        5. ANALYSE DES RISQUES & RÉSILIENCE : Pourquoi ce projet ne fera pas partie des 80% qui échouent.
        
        Ton ton doit être impérial, analytique et extrêmement structuré.
        """
    
    def _get_architecture_scope(self, user_plan: str) -> str:
        """Returns architecture scope instructions based on subscription plan."""
        scopes = {
            "FOUNDER": """
            NIVEAU D'ARCHITECTURE (Plan Fondateur) :
            - Architecture MÉTIER : Processus, flux de valeur, cartographie des acteurs.
            - Architecture FONCTIONNELLE : Modules applicatifs de haut niveau, interfaces utilisateurs.
            - NE PAS inclure : Architecture SI détaillée, Software Engineering, Data/IA avancée, Sécurité technique.
            """,
            "STRATEGIST": """
            NIVEAU D'ARCHITECTURE (Plan Stratège) :
            - Architecture MÉTIER & FONCTIONNELLE (complète).
            - Architecture APPLICATIVE : Découpage en services, API, intégrations tierces.
            - Analyse des RISQUES spécifiques au contexte africain (infrastructure, régulation).
            - NE PAS inclure : Architecture SI/Logiciel détaillée, Data Engineering, Sécurité avancée.
            """,
            "CONSULTANT": """
            NIVEAU D'ARCHITECTURE (Plan Consultant) :
            - Architecture MÉTIER, FONCTIONNELLE & APPLICATIVE (complète).
            - Architecture DATA (partielle) : Sources, flux principaux, gouvernance de base.
            - Architecture SÉCURITÉ (partielle) : Authentification, autorisation, conformité RGPD/locale.
            - NE PAS inclure : Architecture SI complète, Software Engineering détaillé, IA/ML avancée.
            """,
            "VISIONARY": """
            NIVEAU D'ARCHITECTURE (Plan Visionnaire - ACCÈS TOTAL) :
            - Architecture MÉTIER, FONCTIONNELLE, APPLICATIVE (complète).
            - Architecture SI : Infrastructure cloud/on-premise, résilience, disaster recovery.
            - Architecture LOGICIELLE : Patterns (microservices, event-driven), CI/CD, DevOps.
            - Architecture DATA & IA : Data Lake/Warehouse, pipelines ML, gouvernance avancée.
            - Architecture SÉCURITÉ : Zero-trust, cryptographie, audit de conformité, stress-tests.
            """
        }
        return scopes.get(user_plan, scopes["FOUNDER"])
