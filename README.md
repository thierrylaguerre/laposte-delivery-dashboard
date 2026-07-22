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
