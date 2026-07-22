# 📬 Tableau de bord — Suivi des Livraisons La Poste

## 🎯 Contexte & Objectif

### Contexte
Ce projet est né d'une double expérience : celle d'un facteur au quotidien dans le 18ème arrondissement de Paris, et celle d'un étudiant en Master Big Data cherchant à valoriser cette connaissance terrain en compétences Data Analyst.

Chaque jour, La Poste distribue des milliers d'objets postaux sur des dizaines de tournées. Les performances de livraison sont suivies chaque mois par les managers via un récapitulatif interne : taux de distribution, taux d'avisé, taux de 2ème présentation. Ce dernier est directement lié aux primes d'équipe, avec un objectif quadrimestriel fixé à ≥ 23%.

### Problématique
**Comment analyser et visualiser les performances de livraison d'un secteur postal pour identifier les tournées sous-performantes et piloter l'atteinte des objectifs ?**

### Objectif du projet
- Modéliser un dataset réaliste à partir des vraies contraintes opérationnelles du terrain (formats de numéros de tracking, types d'objets, logique des statuts, saisonnalité)
- Construire un dashboard interactif permettant de suivre les KPIs clés du secteur
- Reproduire le récapitulatif mensuel utilisé en interne par La Poste
- Identifier les tournées et périodes sous-performantes pour aider à la prise de décision

### Ce qui rend ce projet unique
Les données ne sont pas issues d'un dataset Kaggle générique — elles ont été entièrement modélisées à partir d'une connaissance terrain réelle : vrais formats de numéros de tracking, vrais noms de tournées, vrais taux de livraison par zone (résidentielle, entreprises, HLM), vraie saisonnalité (creux vacances d'été, pic Noël +50%).

## 📊 Dashboard interactif

🔗 **[Accéder au dashboard en ligne](LIEN_STREAMLIT_ICI)**

## 🗂️ Structure du projet
```
laposte-delivery-dashboard/
│
├── dashboard.py          # Application Streamlit
├── lapostedata.csv       # Dataset simulé (95 000 lignes)
├── requirements.txt      # Dépendances Python
└── README.md
````


## 📦 Données simulées

**95 000 lignes** · 14 tournées · 6 mois

| Variable | Description |
|---|---|
| `recommandé_id` | Numéro de tracking (formats réels La Poste) |
| `date` | Date de distribution |
| `type_objet` | Recommandé / Lettre Suivie / Colissimo / Chronopost |
| `type_chronopost` | PM2 (signature) ou PM2-BAL (boîte aux lettres) |
| `tournee` | Identifiant de tournée (TL-14xx matin / TL-24xx après-midi) |
| `facteur_id` | Identifiant facteur |
| `taxe` | Objet taxé hors UE |
| `statut` | Livré / Avisé / 2ème présentation / Fausse direction / ... |

## 📈 Analyses réalisées

- Volume mensuel avec pic Noël (+50% en décembre)
- Taux de distribution par tournée (TL-1476 zone entreprises vs résidentiel)
- Taux de 2ème présentation vs objectif quadrimestriel ≥ 23%
- Répartition par type d'objet
- Zoom interactif par tournée

## 🛠️ Stack technique

- **Python** · Pandas · Plotly
- **Streamlit** — dashboard déployé sur Streamlit Cloud
- **GitHub** — versioning du projet

## 🚀 Lancer le projet en local

```bash
git clone https://github.com/TON_USERNAME/laposte-delivery-dashboard
cd laposte-delivery-dashboard
pip install -r requirements.txt
streamlit run dashboard.py
```

## 👤 Auteur

**Thierry** · Candidat Data Analyst Junior · Paris Île-de-France  
Facteur à La Poste · Master Big Data Paris 8 · Licence Informatique Sorbonne Paris Nord
