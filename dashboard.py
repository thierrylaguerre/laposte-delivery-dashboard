import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ── CONFIG ───────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="La Poste — Suivi Recommandé",
    page_icon="📬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── CSS ──────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .main { background-color: #FAFAFA; }
    .block-container { padding-top: 1.2rem; padding-bottom: 2rem; }
    h1 { color: #003189; font-weight: 800; font-size: 1.8rem; }
    h2, h3 { color: #003189; font-weight: 700; }
    .stMetric {
        background-color: #FFFFFF;
        border-radius: 12px;
        padding: 16px;
        border-left: 4px solid #FFCD00;
        box-shadow: 0 1px 4px rgba(0,0,0,0.08);
    }
    div[data-testid="stMetricValue"] { color: #003189 !important; font-weight: 800 !important; font-size: 1.6rem !important; }
    div[data-testid="stMetricLabel"] { color: #555 !important; font-size: 0.8rem !important; font-weight: 600 !important; text-transform: uppercase; }
    section[data-testid="stSidebar"] { background-color: #003189 !important; }
    section[data-testid="stSidebar"] * { color: #FFFFFF !important; }
    section[data-testid="stSidebar"] .stMultiSelect > div { background-color: #00267a !important; border-radius: 8px; }
    section[data-testid="stSidebar"] h3 { color: #FFCD00 !important; font-size: 0.85rem !important; text-transform: uppercase; letter-spacing: 1px; }
    .section-title {
        font-size: 1rem;
        font-weight: 700;
        color: #003189;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 0.5rem;
        padding-bottom: 4px;
        border-bottom: 2px solid #FFCD00;
        display: inline-block;
    }
    .insight-box {
        background-color: #EEF3FF;
        border-left: 4px solid #003189;
        border-radius: 8px;
        padding: 10px 14px;
        margin-top: 8px;
        font-size: 0.85rem;
        color: #1A1A1A;
    }
    .insight-warn {
        background-color: #FFF8E1;
        border-left: 4px solid #FFCD00;
        border-radius: 8px;
        padding: 10px 14px;
        margin-top: 8px;
        font-size: 0.85rem;
        color: #1A1A1A;
    }
    .insight-success {
        background-color: #E8F5E9;
        border-left: 4px solid #2E7D32;
        border-radius: 8px;
        padding: 10px 14px;
        margin-top: 8px;
        font-size: 0.85rem;
        color: #1A1A1A;
    }
    .recap-table thead th { background-color: #003189 !important; color: white !important; }
    hr { border: none; border-top: 1px solid #E0E0E0; margin: 1.5rem 0; }
</style>
""", unsafe_allow_html=True)

# ── DONNÉES ──────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("dataset_laposte.csv")
    df['date'] = pd.to_datetime(df['date'])
    df['mois'] = df['date'].dt.month
    return df

df = load_data()

MOIS_LABELS = {7:'Juil', 8:'Août', 9:'Sept', 10:'Oct', 11:'Nov', 12:'Déc'}
COULEURS = ['#003189', '#FFCD00', '#0070C0', '#E30613', '#A0A0A0']

# ── SIDEBAR ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.image("logo-la-poste-2024.jpg", width=200)
    st.markdown("---")

    st.markdown("### 📅 Période")
    mois_options = sorted(df['mois'].unique())
    mois_choisis = st.multiselect(
        "", options=mois_options, default=mois_options,
        format_func=lambda x: MOIS_LABELS[x],
        key="mois"
    )

    st.markdown("### 🚴 Tournées")
    tournees = sorted(df['tournee'].unique())
    col_a, col_b = st.columns(2)
    if col_a.button("Toutes", use_container_width=True):
        st.session_state['tournees_sel'] = tournees
    if col_b.button("Aucune", use_container_width=True):
        st.session_state['tournees_sel'] = []
    tournees_choisies = st.multiselect(
        "", options=tournees,
        default=st.session_state.get('tournees_sel', tournees),
        key="tournees"
    )

    st.markdown("### 📦 Type d'objet")
    types = sorted(df['type_objet'].unique())
    types_choisis = st.multiselect(
        "", options=types, default=types, key="types"
    )

    st.markdown("---")
    st.markdown("<div style='font-size:0.7rem; color:#FFFFFF66; text-align:center;'>Données simulées · Paris 18ème · 2025</div>", unsafe_allow_html=True)

# ── FILTRAGE ─────────────────────────────────────────────────────────────────
dff = df[
    df['mois'].isin(mois_choisis) &
    df['tournee'].isin(tournees_choisies) &
    df['type_objet'].isin(types_choisis)
]

if len(dff) == 0:
    st.warning("⚠️ Aucune donnée pour cette sélection. Ajustez les filtres.")
    st.stop()

# ── HEADER ───────────────────────────────────────────────────────────────────
derniere_maj = df['date'].max().strftime('%d %B %Y')
col_titre, col_info = st.columns([3, 1])
with col_titre:
    st.markdown("# 📬 Suivi des recommandés")
    st.caption("Paris 18ème · Ilot CAP 18")
with col_info:
    st.markdown(f"**Données au** {derniere_maj}")
    st.caption(f"{len(tournees_choisies)} tournée(s) · {len(mois_choisis)} mois sélectionné(s)")
st.markdown("---")

# ── KPIs ─────────────────────────────────────────────────────────────────────
taux_livre = (dff['statut'] == 'Distribué').mean() * 100
taux_avise = (dff['statut'] == 'Avisé').mean() * 100
taux_refuse = (dff['statut'] == 'Refusé').mean() * 100
eligibles = dff[dff['type_objet'].isin(['Recommandé', 'Chronopost'])]
taux_2e = (eligibles['statut'] == '2ème présentation').mean() * 100 if len(eligibles) > 0 else 0

# Delta mois précédent
mois_max = dff['mois'].max()
dff_curr = dff[dff['mois'] == mois_max]
dff_prev = dff[dff['mois'] == mois_max - 1]

delta_livre = None
if len(dff_prev) > 0:
    prev_livre = (dff_prev['statut'] == 'Livré').mean() * 100
    curr_livre = (dff_curr['statut'] == 'Livré').mean() * 100
    delta_livre = f"{curr_livre - prev_livre:+.1f}% vs mois préc."

objectif_ok = taux_2e >= 25

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Objets traités", f"{len(dff):,}", help="Volume total sur la période sélectionnée")
col2.metric("Taux de distribution", f"{taux_livre:.1f}%", delta=delta_livre, help="% d'objets remis au destinataire")
col3.metric("Taux d'avisé", f"{taux_avise:.1f}%", help="% d'objets déposés en bureau de poste")
col4.metric("Taux de 2ème présentation", f"{taux_2e:.1f}%",
    delta="✅ Objectif atteint" if objectif_ok else "❌ Sous objectif (≥25%)",
    delta_color="normal" if objectif_ok else "inverse",
    help="KPI lié aux primes d'équipe — objectif quadrimestriel ≥ 25%")
col5.metric("Taux de refus", f"{taux_refuse:.1f}%", help="Objets taxés refusés par le destinataire")

st.markdown("---")

# ── GRAPHES LIGNE 1 ───────────────────────────────────────────────────────────
col_l, col_r = st.columns(2)

with col_l:
    st.markdown('<div class="section-title">Volume mensuel</div>', unsafe_allow_html=True)
    vol = dff.groupby('mois').size().reset_index(name='nb')
    vol['label'] = vol['mois'].map(MOIS_LABELS)
    mois_pic = vol.loc[vol['nb'].idxmax(), 'label']
    fig1 = px.bar(vol, x='label', y='nb',
                  color_discrete_sequence=['#003189'],
                  labels={'label': '', 'nb': 'Objets'})
    fig1.update_layout(plot_bgcolor='white', paper_bgcolor='white',
                       font_color='#1A1A1A', margin=dict(t=20, b=10))
    fig1.update_traces(marker_line_width=0)
    st.plotly_chart(fig1, use_container_width=True)
    mois_max_vol = vol.loc[vol['nb'].idxmax()]
    mois_min_vol = vol.loc[vol['nb'].idxmin()]
    delta_vol = ((mois_max_vol['nb'] - mois_min_vol['nb']) / mois_min_vol['nb'] * 100)
    st.markdown(f'<div class="insight-box">📈 <b>{mois_pic}</b> est le mois le plus chargé — <b>+{delta_vol:.0f}%</b> vs {mois_min_vol["label"]} (creux vacances)</div>', unsafe_allow_html=True)

with col_r:
    st.markdown('<div class="section-title">Répartition par type d\'objet</div>', unsafe_allow_html=True)
    type_c = dff['type_objet'].value_counts().reset_index()
    type_c.columns = ['type', 'count']
    fig2 = px.pie(type_c, values='count', names='type',
                  color_discrete_sequence=COULEURS, hole=0.45)
    fig2.update_layout(paper_bgcolor='white', font_color='#1A1A1A',
                       legend=dict(orientation='h', yanchor='bottom', y=-0.2),
                       margin=dict(t=20, b=40))
    fig2.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig2, use_container_width=True)
    type_dom = type_c.iloc[0]
    st.markdown(f'<div class="insight-box">📊 <b>{type_dom["type"]}</b> représente <b>{type_dom["count"]/len(dff)*100:.0f}%</b> du volume total — type majoritaire sur le secteur</div>', unsafe_allow_html=True)

st.markdown("---")

# ── GRAPHES LIGNE 2 ───────────────────────────────────────────────────────────
col_l2, col_r2 = st.columns(2)

with col_l2:
    st.markdown('<div class="section-title">Taux de livraison par tournée</div>', unsafe_allow_html=True)
    reco = dff[dff['type_objet'] == 'Recommandé']
    if len(reco) > 0:
        taux_t = reco.groupby('tournee')['statut'].apply(
            lambda x: (x == 'Livré').mean() * 100
        ).reset_index(name='taux')
        taux_t = taux_t.sort_values('taux', ascending=True)
        moyenne = taux_t['taux'].mean()
        taux_t['couleur'] = taux_t['taux'].apply(
            lambda x: 'Au-dessus moyenne' if x >= moyenne else 'En dessous moyenne'
        )
        fig3 = px.bar(taux_t, x='taux', y='tournee', orientation='h',
                      color='couleur',
                      color_discrete_map={'Au-dessus moyenne': '#003189', 'En dessous moyenne': '#A0C4E8'},
                      labels={'taux': '% Livré', 'tournee': ''})
        fig3.add_vline(x=moyenne, line_dash='dash', line_color='#FFCD00',
                       annotation_text=f'Moy. {moyenne:.1f}%')
        fig3.update_layout(showlegend=False, plot_bgcolor='white', paper_bgcolor='white',
                           font_color='#1A1A1A', margin=dict(t=20, b=10), height=420)
        st.plotly_chart(fig3, use_container_width=True)
        best = taux_t.iloc[-1]
        worst = taux_t.iloc[0]
        st.markdown(f'<div class="insight-success">🏆 <b>{best["tournee"]}</b> surperforme ({best["taux"]:.1f}%) — zone d\'entreprises avec présence assurée</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="insight-warn">⚠️ <b>{worst["tournee"]}</b> a le taux le plus faible ({worst["taux"]:.1f}%) — adresses non localisables fréquentes</div>', unsafe_allow_html=True)

with col_r2:
    st.markdown('<div class="section-title">2ème présentation vs objectif ≥25%</div>', unsafe_allow_html=True)
    elig = dff[dff['type_objet'].isin(['Recommandé', 'Chronopost'])]
    if len(elig) > 0:
        t2e = elig.groupby('mois')['statut'].apply(
            lambda x: (x == '2ème présentation').mean() * 100
        ).reset_index(name='taux')
        t2e['label'] = t2e['mois'].map(MOIS_LABELS)
        t2e['statut_obj'] = t2e['taux'].apply(
            lambda x: '✅ Objectif atteint' if x >= 25 else '❌ Sous objectif'
        )
        fig4 = px.bar(t2e, x='label', y='taux', color='statut_obj',
                      color_discrete_map={'✅ Objectif atteint': '#003189', '❌ Sous objectif': '#CC0000'},
                      labels={'label': '', 'taux': '% 2ème présentation'})
        fig4.add_hline(y=25, line_dash='dash', line_color='#FFCD00',
                       annotation_text='Objectif ≥ 25%', annotation_position='top left')
        fig4.update_layout(plot_bgcolor='white', paper_bgcolor='white',
                           font_color='#1A1A1A', legend_title_text='',
                           margin=dict(t=20, b=10), height=420)
        st.plotly_chart(fig4, use_container_width=True)
        nb_sous = (t2e['taux'] < 25).sum()
        nb_ok = (t2e['taux'] >= 25).sum()
        if nb_sous > 0:
            mois_sous = ', '.join(t2e[t2e['taux'] < 25]['label'].tolist())
            st.markdown(f'<div class="insight-warn">⚠️ <b>{nb_sous} mois sous objectif</b> : {mois_sous} — impact potentiel sur la prime d\'équipe</div>', unsafe_allow_html=True)
        if nb_ok > 0:
            st.markdown(f'<div class="insight-success">✅ <b>{nb_ok} mois atteignent l\'objectif</b> — Nov. et Déc. portés par le pic de volume Noël</div>', unsafe_allow_html=True)

st.markdown("---")

# ── RECAP MENSUEL ─────────────────────────────────────────────────────────────
st.markdown('<div class="section-title">Récapitulatif mensuel</div>', unsafe_allow_html=True)
st.markdown("")

def recap_mois(g):
    elig_g = g[g['type_objet'].isin(['Recommandé', 'Chronopost'])]
    taux_2e_g = (elig_g['statut'] == '2ème présentation').mean() * 100 if len(elig_g) > 0 else 0
    return pd.Series({
        'Total objets': len(g),
        'Distribué (%)': round((g['statut'] == 'Livré').mean() * 100, 1),
        'Avisé (%)': round((g['statut'] == 'Avisé').mean() * 100, 1),
        '2ème présentation (%)': round(taux_2e_g, 1),
        'Objectif ≥25%': '✅' if taux_2e_g >= 25 else '❌',
    })

recap = dff.groupby('mois').apply(recap_mois).reset_index()
recap['Mois'] = recap['mois'].map(MOIS_LABELS)
recap = recap[['Mois', 'Total objets', 'Distribué (%)', 'Avisé (%)', '2ème présentation (%)', 'Objectif ≥25%']]
st.dataframe(recap, use_container_width=True, hide_index=True)

st.markdown("---")

# ── ZOOM TOURNÉE ──────────────────────────────────────────────────────────────
st.markdown('<div class="section-title">Zoom sur une tournée</div>', unsafe_allow_html=True)
st.markdown("")

tournee_zoom = st.selectbox("", sorted(df['tournee'].unique()), label_visibility="collapsed")
dz = dff[dff['tournee'] == tournee_zoom]

if len(dz) == 0:
    st.warning("Aucune donnée pour cette tournée avec les filtres actuels.")
else:
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total objets", f"{len(dz):,}")
    c2.metric("Taux distribué", f"{(dz['statut']=='Livré').mean()*100:.1f}%")
    c3.metric("Taux avisé", f"{(dz['statut']=='Avisé').mean()*100:.1f}%")
    elig_z = dz[dz['type_objet'].isin(['Recommandé','Chronopost'])]
    taux_2e_z = (elig_z['statut']=='2ème présentation').mean()*100 if len(elig_z) > 0 else 0
    c4.metric("2ème présentation", f"{taux_2e_z:.1f}%",
              delta="✅ Objectif atteint" if taux_2e_z >= 25 else "❌ Sous objectif",
              delta_color="normal" if taux_2e_z >= 25 else "inverse")

    col_za, col_zb = st.columns(2)
    with col_za:
        statuts_z = dz['statut'].value_counts().reset_index()
        statuts_z.columns = ['statut', 'count']
        fig_z1 = px.bar(statuts_z, x='statut', y='count',
                        color_discrete_sequence=['#003189'],
                        labels={'statut': '', 'count': 'Nombre'})
        fig_z1.update_layout(plot_bgcolor='white', paper_bgcolor='white',
                              font_color='#1A1A1A', showlegend=False, margin=dict(t=10))
        st.plotly_chart(fig_z1, use_container_width=True)

    with col_zb:
        vol_z = dz.groupby('mois').size().reset_index(name='nb')
        vol_z['label'] = vol_z['mois'].map(MOIS_LABELS)
        fig_z2 = px.line(vol_z, x='label', y='nb',
                         color_discrete_sequence=['#003189'],
                         markers=True,
                         labels={'label': '', 'nb': 'Objets'})
        fig_z2.update_layout(plot_bgcolor='white', paper_bgcolor='white',
                              font_color='#1A1A1A', margin=dict(t=10))
        st.plotly_chart(fig_z2, use_container_width=True)

# ── FOOTER ────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style='text-align:center; color:#AAAAAA; font-size:0.75rem; padding: 10px 0;'>
    Projet portfolio Data Analyst · Données simulées à partir de l'expérience terrain La Poste Paris 18ème · 2025
</div>
""", unsafe_allow_html=True)