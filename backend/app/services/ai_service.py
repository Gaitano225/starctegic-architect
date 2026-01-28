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
                             recommendations: List[Dict[str, Any]]) -> str:
        """
        Uses Gemini to transform bullet-point recommendations into a professional Business Case narrative.
        """
        if not self.api_key:
            return "Note : L'IA d'analyse n'est pas activée (Clé API manquante). Les recommandations techniques ci-dessous restent valides."

        prompt = self._build_prompt(project_data, recommendations)
        
        try:
            # Using generate_content (synchronous version or wrapper if needed)
            # In a real async environment, we'd use generate_content_async
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error generating AI enhancement: {str(e)}"

    def _build_prompt(self, project_data: Dict[str, Any], recommendations: List[Dict[str, Any]]) -> str:
        answers = project_data.get('answers', {})
        rules_str = "\n".join([f"- [Prop {r['id']}]: {r['recommendation']} (Justification: {r['justification']})" for r in recommendations])
        
        return f"""
        Rôle : Tu es un Consultant Stratégique Senior et Architecte Solutions spécialisé dans le marché technologique africain.
        Mission : Rédiger la section "Analyse Stratégique & Narrative" d'un Business Case pour le projet '{project_data.get('name')}'.
        
        CONTEXTE DÉTAILLÉ DU PROJET :
        - Problème à résoudre : {answers.get('problem_statement')}
        - Solution proposée : {answers.get('solution_description')}
        - Demande du marché : {answers.get('market_demand')}
        - Analyse de la concurrence : {answers.get('competitor_analysis')}
        - Différenciateur (UVP) : {answers.get('unique_value_prop')}
        - Pays cible : {answers.get('target_country')}
        - Secteur : {answers.get('sector')}
        
        CONTRAINTES TECHNIQUES (Issues de notre moteur de règles) :
        Tu DOIS impérativement construire ton argumentation autour de ces points techniques :
        {rules_str}
        
        STRUCTURE ATTENDUE DU RAPPORT NARRATIF :
        1. Opportunité de Marché (Pourquoi maintenant et pourquoi ce pays ?)
        2. Diagnostic de la Concurrence & Positionnement (Comment battre l'existant cité ?)
        3. Alignment Technologique (Explique pourquoi les recommandations citées sont les meilleures pour le secteur {answers.get('sector')})
        4. Vision ROI & Scalabilité (Perspectives de croissance technique)
        
        Ton ton doit être extrêmement professionnel, inspirant confiance aux investisseurs tout en étant pragmatique sur les défis de connectivité ou de paiement locaux.
        Utilise le Français uniquement.
        """
