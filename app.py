""" Auteurs : Kenza SIFOUANE et Diyé NDIAYE
    DATE DE MODIFICATION : 13/01/2010
"""
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dash
import dash_core_components as dcc
import dash_html_components as html

# -------------------------------------------------- #
# -------------- Importer les données -------------- #
# -------------------------------------------------- #

# Lecture
df_histogramme = pd.read_csv("histogramme.csv", sep= ";")
df_carte = pd.read_csv("carte.csv", sep= ",")

# -------------------------------------------------- #
# ------------------ Histogramme ------------------- #
# -------------------------------------------------- #

# Prendre le sexe == 0 (hommes + femmes) pour éliminer les doublons
df_histogramme = df_histogramme.query('sexe == 0')


# Restreindre à une ligne par jour
df_histogramme = df_histogramme.groupby(['jour']).agg({'hosp' : 'sum',
 'rea' : 'sum', 'rad' : 'sum', 'dc' : 'sum'}).reset_index()

# Créer l'histogramme
histogramme = px.histogram(df_histogramme, x="jour", y="hosp")

# Titres
histogramme.update_layout(

    # Titres
    title="Evolution du nombre d'hospitalisation par jour",
    xaxis_title="Jours",
    yaxis_title="Hospitalisations",

    # Couleur de fond du graphique
    plot_bgcolor='white',
)

# Utiliser le mode categories
histogramme.update_xaxes(type="category")

# Surlignage noir
histogramme.update_traces(
    marker=dict( line=dict( width=2 ) )
)

# -------------------------------------------------- #
# ---------------------- Plan ---------------------- #
# -------------------------------------------------- #

# Créer un plan
plan = go.Figure()

for nomColonne, nomLigne in [
        ("hosp", "Hospitalisations"),
        ("rea", "Réanimations"),
        # ("rad", "Retours à domicile"),
        ("dc", "Décès")
    ]:
    # Ajouter la courbe
    plan.add_trace(
        go.Scatter(
            x=df_histogramme["jour"],
            y=df_histogramme[nomColonne],
            mode='lines', #+markers
            name=nomLigne
        )
    )

# Changer le format de date
plan.update_xaxes(tickformat='%B %Y')

# Titres et couleur de fond
plan.update_layout(

    # Titres
    title="Evolution du COVID en France",
    xaxis_title="Mois",
    yaxis_title="Population",

    # Couleur de fond du graphique
    plot_bgcolor='white',
)

# -------------------------------------------------- #
# --------------------- Carte ---------------------- #
# -------------------------------------------------- #

# Créer la carte
carte = px.scatter_mapbox(
    df_carte,

    # Coordonnées
    lat = "latitude",
    lon = "longitude",

    # Affichage
    hover_name="adresse",
    hover_data={

        # Ne pas afficher
        "latitude"     : False,
        "longitude"    : False,
        # Afficher
        "horaire"      : True,
        "mod_prel"     : True,
        "do_prel"      : True,
        "do_antigenic" : True,
        "check_rdv"    : True,
        "tel_rdv"      : True,
        "web_rdv"      : True,
        "public"       : True
    },
    labels={
        # Accessibilité
        "horaire"      : "Horaires",
        "public"       : "Public autorisé",
        "mod_prel"     : "Modalités de prévèvement",
        "check_rdv"    : "Sans rendez vous",

        # Tests
        "do_prel"      : "Tests RT-PCR",
        "do_antigenic" : "Tests antigéniques",

        # Contact
        "tel_rdv"      : "Téléphone",
        "web_rdv"      : "Site web"
    },
    color="do_antigenic",
    color_continuous_scale=[ "green", "blue" ],
    # size="do_prel",
    zoom = 4.7
)

# Titre, type et fond de carte
carte.update_layout(
    title="Les centres de tests COVID en France",
    mapbox_style = "open-street-map",
    plot_bgcolor='white'
)

# -------------------------------------------------- #
# ----------------- Affichage web ------------------ #
# -------------------------------------------------- #

# Créer le dashboard
app = dash.Dash(__name__)

# Générer le code HTML
app.layout = html.Div([

    html.H1("Données COVID-19 en France", style={'text-align': 'center'}),

    # Histogramme
    dcc.Graph(
        id = 'histogramme_hospitalisations',
        className = "histogramme_hospitalisations",
        figure = histogramme,
    ),

    # Graphique (x, y)
    dcc.Graph(
        id = 'plan_cas',
        className = "plan_cas",
        figure = plan,
    ),

    # Carte
    dcc.Graph(
        id = 'carte_tests',
        className = "carte_tests",
        figure = carte,
        style = { 'height': '110vh' }
    ),

 ])

# Lancer le serveur
app.run_server(debug=True)
