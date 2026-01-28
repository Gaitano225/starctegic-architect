# PROJET : STRATEGIC ARCHITECT - CAHIER DES CHARGES TECHNIQUE (V2.1 - ENHANCED)

## CONTEXTE & OBJECTIF
Transformer l'expertise d'un Architecte SI et Génie Logiciel en une plateforme SaaS automatisée... (Contenu existant...)

## NOUVELLES EXIGENCES (AJOUTÉES V2.1)

### F10 - Système de Validation "Pre-flight" (95% Cohérence)
- **Objectif**: Empêcher la génération de rapports basés sur des réponses contradictoires.
- **Logique**: Vérifie les dépendances logiques (ex: Budget trop faible pour une architecture Microservices).
- **Feedback**: Affiche un avertissement "Attention: Votre budget semble insuffisant pour la scalabilité demandée".

### F11 - Audit Trail & Traçabilité (Sécurité)
- **Objectif**: Prouver la provenance de chaque recommandation.
- **Action**: Stockage de l'ID unique de chaque règle YAML déclenchée dans le rapport (Champ `applied_rule_ids`).

### F12 - Simulateur ROI Dynamique
- **Objectif**: Projeter la rentabilité technique sur 3 ans.
- **Variables**: Coût de dév initial, maintenance infra Cloud (AWS/GCP/Local), croissance utilisateur.

### F13 - Intelligence de Comparaison (Contrast)
- **Objectif**: Présenter systématiquement deux options dans le rapport:
    1. **Option "Vitesse/MVP"**: La solution la plus rentable et rapide.
    2. **Option "Scale/Visionnaire"**: La solution la plus robuste mais plus coûteuse.

## ARCHITECTURE ENHANCEMENTS
- **LLM Prompt Engineering**: Utilisation de "Few-shot prompting" pour garantir que Gemini cite les règles techniques réelles.
- **Offline Reliability**: Mise en place d'un cache Redis pour les sessions de questionnaire afin d'éviter la perte de données sur micro-coupures 3G.
- **Compliance**: Chiffrement AES-256 pour les réponses sensibles conformément aux lois sur le numérique au Bénin et Sénégal.
