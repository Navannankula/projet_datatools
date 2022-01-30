from turtle import title
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import json
import pymongo
from pymongo import MongoClient
import pandas as pd
import plotly.express as px

##  Traitement des données via la base de données MangoDB

# Fichier json de nos données scrappées à integrer dasn notre base de données 
with open("scrapping.json") as jsonFile:
    jsonObject = json.load(jsonFile)
    jsonFile.close()

# Création de notre base de données Mango 
client = pymongo.MongoClient('localhost', 27017)
database6 = client['projet6']
collection6 = database6['immobilier_v2']
database6.collection6.drop()
collection6.insert_many(jsonObject)

# fonction pour transformer notre curseur en liste de dictionnaires
def recup_list(cursor):
    lst = []
    for i in cursor:
        lst.append(i)
    return(lst)


# FILTRE SUR LES VILLES
    
# requête pour obtenir la liste des villes 
cur_ville = collection6.distinct('Ville')
# transformation du curseur en liste 
lst_ville = recup_list(cur_ville)

# Pour nous permettre de filtrer sur les villes 
options_selection_ville = []
for i in range(len(lst_ville)):
    option = {}
    option['label']=lst_ville[i]
    option['value']=lst_ville[i]
    options_selection_ville.append(option)


# FILTRE SUR LES CODES POSTAUX     

cur_cp = collection6.distinct('code postal')
# transformation du curseur en liste 
lst_cp= recup_list(cur_cp)

# Pour nous permettre de filtrer sur les codes postaux
options_selection_cp = []
for i in range(len(lst_cp)):
    option = {}
    option['label']=lst_cp[i]
    option['value']=lst_cp[i]
    options_selection_cp.append(option)


# liste de toutes nos données 
cursor = collection6.find()
lst = recup_list(cursor)

# Pour avoir le nombre total de biens disponible dans une ville séléctionnée 
df_total= pd.DataFrame(lst)
df_total= df_total.drop_duplicates(subset =["code postal","prix", 'm2'])
children_taille_total = str(df_total.shape[0])
  
# requête pour avoir le prix moyen des biens pour chaque ville 
cur_moy = collection6.aggregate([{"$group" : {"_id" : "$Ville", "prix moyen des offres" : {"$avg":"$prix"}}}])
lst_prixmoy= []
for i in cur_moy:
    lst_prixmoy.append(i)

data = pd.DataFrame(lst_prixmoy)
a=data[data['_id']==''].index
data=data.drop(index=a)


#requete pour grouper par rapport aux villes et avoir le prix moyen du m2
cur_moym2 = collection6.aggregate([{"$group" :{
    
                             "_id" : "$Ville",
                            "prix moyen": { "$avg": "$prix" },
                            "moyenne de m2": { "$avg":"$m2"}
                            }}, 
                            {"$project": {
                                "prix moyen": 1,
                                "moyenne de m2": 1,
  
                                          "prix moyen du m2":{"$divide" :["$prix moyen","$moyenne de m2"]},
                                          }

                                    
                                 }
                            
                            ])
                             

lst_prixmoym2 = recup_list(cur_moym2)
datam2= pd.DataFrame(lst_prixmoym2)
nb_prixmoym2 = datam2.shape[0]
a=datam2[datam2['_id']==''].index
datam2=datam2.drop(index=a)
#Diagramme du prix moyen des offres par ville 
fig1 =  px.bar(data, x='_id', y='prix moyen des offres',color = '_id', title="Prix moyen des offres par ville ")
#Diagramme du prix moyen du m2 par ville 
fig2 =  px.bar(datam2, x='_id', y='prix moyen du m2',color = '_id', title="Prix moyen du m2 par Ville")

# POur avoir la répartition des biens dispo par rapport aux villes 
df_total_som = df_total.groupby('Ville',  as_index=False).count()
#Camembert pour représenter cela
fig6 = px.pie(df_total_som,values='lieux', names='Ville',title='Répartition des biens diponibles par rapport aux villes')                    

##### Création de la NavigationBar réalisé avce Boostrap (récupéré sur le web)  ######

external_stylesheets = [dbc.themes.BOOTSTRAP]

# Couleurs utilisées dans le Dashboard
colors = {
    'background1': '#white',
    'background2': '#white',
    'background3': '#white',
    'text': '#white'
}

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# padding for the page content
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.H2("Menu", className="display-4"),
        html.Hr(),
        html.P(
            "Projet DSIA", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("Acceuil", href="/", active="exact"),
                dbc.NavLink("Recherche", href="/page-1", active="exact"),
                dbc.NavLink("Visualisation globale", href="/page-2", active="exact"),
                dbc.NavLink("Visualisation filtrée ", href="/page-3", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", children=[], style=CONTENT_STYLE)

##### Création de l'application Dash  ######

if __name__ == '__main__':
    app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
    app.config.suppress_callback_exceptions=True

# #la mise en page en dash se déroule grâce app.layout c'est à l'interieur du layout que l'on va insérer le texte 
# et l'odre d'appartion des grapghiques
# app.layout = html.Div(children=[ Pour écrire le titre de notre dashboard
    
    #Pour créer notre fenêtre et faire appel au menu
    app.layout = html.Div(style={'backgroundColor': colors['background1']}, children=[
        html.Div([
            dcc.Location(id="url"),
            sidebar,
            content
        ]),
    ])

    colors = {
    'background1': '#white',
    'background2': '#white',
    'background3': '#white',
    'text': '#white'
}

    ## callback pour remplir les pages séléctionnées dans le menu 
    @app.callback(
    Output("page-content", "children"),
    [Input("url", "pathname")]
)
    def render_page_content(pathname):
        if pathname == "/":
            return [
                dbc.Row([], justify='around', align = 'center', style={'height':'30px'}),
                dbc.Row([], justify='around', align = 'center', style={'height':'30px'}),
                dbc.Row([
    
        dbc.Col([
            html.H4(id='title2',
                    children='Présentation',
                    style={
                    'textAlign': 'center',
                    'color': colors['text'],
                    'fontWeight': 'bold',
                    'fontSize':20}
                    ),  
            dbc.Row([], justify='around', align = 'center', style={'height':'30px'}),

            html.Div(
                 children=f'''
                        Pour notre projet de DataEngineer Tools nous avons décidé de nous intéresser aux biens immobilier à vendre dans les 10 plus grandes villes de France disponiblesur le site particulieraparticulier.fr

Nous avons donc scrappé les informations concernant les maisons à vendre sur le site en question en nous focalisant sur le prix, la taille (en m2), le nombre de chambre, le nombre de pièce et la localisation avec la ville et le code postal.

L’enjeu ici est de permettre aux utilisateurs une meilleure visualisation du marchés immobilier actuel à l'aide de plusieurs indicateurs/filtres différent. En effet en parcourant les nombreuses pages d'offre sur les sites d'agences immobilières il est facile de se perdre. Notre but est donc de proposer une vue globale de ce qui est disponible en ce moment pour pouvoir adapter sa demande en fonction de ce qui est le plus rentable et le mieux pour soit.



                            ''', style={'text-align':'center'}
            ), 
        ],width=8),

        dbc.Row([], justify='around', align = 'center', style={'height':'30px'}),

        dbc.Col([
            html.H2(
                id='text-before-button',
                children='Données scrapées depuis le site Particulier à particulier',
                style={
                    'textAlign': 'center',
                    'color': colors['text'],
                    'fontSize':20
                }
            ),
        ], width=5),

        dbc.Col([
            # Lien vers les données utilisées
            dbc.Button("particulieràparticulier.fr",id="scraper-button", color="success", className="mr-1", href="https://www.pap.fr/annonce/vente-maisons-paris-75-g439", style={'fontWeight': 'bold'}),
        ], width=1),
    ], justify='around', style={'height':'70px', 'backgroundColor':colors['background3']}),

    dbc.Row([], justify='around', align = 'center', style={'height':'30px'}),

                ]
        elif pathname == "/page-1":
            return [
                dbc.Row([], justify='around', align = 'center', style={'height':'30px'}),
                html.H4(id='title2',
                    children='Liste des biens disponibles par ville',
                    style={
                    'textAlign': 'center',
                    'color': colors['text'],
                    'fontWeight': 'bold',
                    'fontSize':20}
                    ),  

                dbc.Row([], justify='around', align = 'center', style={'height':'30px'}),
                dbc.Row([], justify='around', align = 'center', style={'height':'30px'}),    
                
                # Menu déroulant pour le choix des villes 
                dbc.Row([
                    dbc.Col([
                        html.Div(children=[
                
                            dcc.Dropdown(
                                id='selection-ville',
                                placeholder='Sélectionnez une ville',
                                options=options_selection_ville,
                                #value='',
                                style={'display': 'inline-block','width':'100%'}
                                ),
                            ]),
                    ], width=7),
                ], justify='around', align = 'center'),

                dbc.Row([], justify='around', align = 'center', style={'height':'30px'}),

                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            dbc.CardHeader("Nombre de bien disponibles"),
                            dbc.CardBody([
                                html.H4(
                                    id = 'ville-selection-nom',
                                    children = "Total", 
                                    className="card-title"),
                                html.P(
                                    id = 'ville-selection-nb',
                                    children = children_taille_total, 
                                    className="card-text"),
                            ]
                            ),
                            #dbc.CardFooter("This is the footer"),
                ], style={"width": "18rem"},)
                ], width=7),
                        dbc.Card([
                            dbc.CardHeader("Prix moyen du m2 "),
                            dbc.CardBody([
                                html.H4(
                                    id = 'ville-selection-nom2',
                                    children = "Total", 
                                    className="card-title"),
                                html.P(
                                    id = 'ville-selection-nbm2',
                                    children = 'x', 
                                    className="card-text"),
                            ]
                            ),
                            #dbc.CardFooter("This is the footer"),
                ], style={"width": "18rem"},)
                ], justify='around', align = 'center'),

                dbc.Row([], justify='around', align = 'center', style={'height':'30px'}),

                # Menu déroulant pour le choix des codes postaux 
                dbc.Row([
                    dbc.Col([
                        html.Div(children=[
                            dcc.Dropdown(
                                id='selection-cp',
                                placeholder='Sélectionnez un code postal',
                                options=options_selection_cp,
                                #value='',
                                style={'display': 'inline-block','width':'100%'}
                                ),
                            ]),
                    ], width=7),
                
                ], justify='around', align = 'center'),

                dbc.Row([], justify='around', align = 'center', style={'height':'30px'}),


                dbc.Row([], justify='around', align = 'center', style={'height':'30px'}),

                dbc.Row([
                    dbc.Col([
                        html.Div(id='filtre-ville', children=[
                            dbc.ListGroup([
                                dbc.ListGroupItem("Lieux", color="secondary", style={'textAlign': 'center','width':'300px','fontWeight': 'bold'}),
                                dbc.ListGroupItem("Prix", color="secondary", style={'textAlign': 'center','width':'110px','fontWeight': 'bold'}),
                                dbc.ListGroupItem("Nombre de pièce", color="secondary", style={'textAlign': 'center','width':'140px','fontWeight': 'bold'}),
                                dbc.ListGroupItem("Nombre de chambre", color="secondary", style={'textAlign': 'center','width':'110px','fontWeight': 'bold'}),
                                dbc.ListGroupItem("Taille", color="secondary", style={'textAlign': 'center','width':'200px','fontWeight': 'bold'}),
                        ],horizontal=True,className="mb-2",),
                            dbc.ListGroup([
                                dbc.ListGroupItem(lst[4]['lieux'], style={'textAlign': 'center','width':'300px'}),
                                dbc.ListGroupItem(lst[4]['prix'], style={'textAlign': 'center','width':'110px'}),
                                dbc.ListGroupItem(lst[4]['pièce'], style={'textAlign': 'center','width':'140px'}),
                                dbc.ListGroupItem(lst[4]['chambre'], style={'textAlign': 'center','width':'110px'}),
                                dbc.ListGroupItem(lst[4]['m2'], style={'textAlign': 'center','width':'200px'}),
                    ],horizontal=True,className="mb-2",),
                    ]),
                    ], width=6, align='center'),

                ] , justify='around', align = 'center', style={'backgroundColor':colors['background1']}),

        ]
        
        elif pathname == "/page-2":
            return [
                html.H1('Visualisation globale',
                        style={'textAlign':'center'}),
                
                dcc.Graph(
                    id='graph1',
                    figure=fig1),

                dcc.Graph(
                    id='graph2',
                    figure=fig2), 

                dcc.Graph(
                    id='graph6',
                    figure=fig6),     
 
     

                ]
        elif pathname == "/page-3":  
            return [
                html.H1('Visualisation filtrée sur les villes',
                        style={'textAlign':'center'}),

                dbc.Row([
                    dbc.Col([
                        html.Div(children=[
                
                            dcc.Dropdown(
                                id='selection-ville2',
                                placeholder='Sélectionnez une ville',
                                options=options_selection_ville,
                                value='Marseille',
                                style={'display': 'inline-block','width':'100%'}
                                ),
                            ]),
                    ], width=7),
                ], justify='around', align = 'center'),   


                dcc.Graph(
                    id='graph3',
                    figure=fig2),

                dcc.Graph(
                    id='graph4',
                    figure=fig2),

                dcc.Graph(
                    id='graph5',
                    figure=fig2)        

                    
  
            ]                    
    # If the user tries to reach a different page, return a 404 message
        return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
        )

    # Mise à jour des pays sélectionnables dans le menu déroulant et affichage des chiffres important concernant la ville
    @app.callback(
        [Output('selection-cp', 'options'),Output('ville-selection-nom', 'children'),Output('ville-selection-nb', 'children'), Output('ville-selection-nbm2', 'children')], 
        [Input('selection-ville','value')])
    def update_dropdown(selected_ville):
    
    

        cur_ville2 = collection6.find({"Ville" : selected_ville})
        lst_ville2 = []
        for i in cur_ville2:
            lst_ville2.append(i)

        df_ville2 = pd.DataFrame(lst_ville2)
        df_ville2= df_ville2.drop_duplicates(subset =["prix", 'm2'])
        children_taille = str(df_ville2.shape[0])

        arrondissement= collection6.aggregate([{"$match":{"Ville":selected_ville}},
                            {"$group" :{
    
                             "_id" : "$code postal",
                            "prixmoyen": { "$avg": "$prix" },
                            "m2moyen": { "$avg":"$m2"}
                            }}, 
                            {"$project": {
                                "prixmoyen": 1,
                                "m2moyen": 1,
  
                                          "prix moyen du m2":{"$divide" :["$prixmoyen","$m2moyen"]},
                            }}
                              ])
        c=(recup_list(arrondissement))
        df_arrondissement = pd.DataFrame(c)
        #df_arrondissement = df_arrondissement.drop(df_arrondissement.columns[-1],axis=1)
        df_arrondissement["prixmoyenm2"]=df_arrondissement['prixmoyen']/df_arrondissement['m2moyen']
        arrond=df_arrondissement["_id"].unique()

        options_selection_cp = []
        for i in range(arrond.size):
            option = {}
            option['label']=arrond[i]
            option['value']=arrond[i]
            options_selection_cp.append(option)
        
        df_m2 = datam2[(datam2['_id'] == selected_ville)]
        print(df_m2)
    
        children_taille_m2 = str(df_m2['prix moyen du m2'].values[0])

        if selected_ville == "Paris":
            children = "Paris"
        if selected_ville == "Marseille":
            children = "Marseille"
        if selected_ville == "Toulouse":
            children = "Toulouse"
        if selected_ville == "Montpellier":
            children = "Montpellier"
        if selected_ville == "Nice":
            children = "Nice"
        if selected_ville == "Nantes":
            children = "Nantes"
        if selected_ville == "Strasbourg":
            children = "Strasbourg"
        if selected_ville == "Lille":
            children = "Lille"
        if selected_ville == "Lyon":
            children = "Lyon" 
        if selected_ville == "Bordeaux":
            children = "Bordeaux"      
        #else : 
            #options = options_selection_paris

        return options_selection_cp, children, children_taille, children_taille_m2 

    # Afficher la liste des biens en fonction de la ville et du code postal séléctionné
    @app.callback(
        Output('filtre-ville', 'children'),
        [Input('selection-ville', 'value'), 
        Input('selection-cp','value')
        ])
    def update_figure(select_ville, select_cp):
       
        children = [
        dbc.ListGroup([
            dbc.ListGroupItem("Lieux", color="secondary", style={'textAlign': 'center','width':'300px','fontWeight': 'bold'}),
            dbc.ListGroupItem("Prix", color="secondary", style={'textAlign': 'center','width':'110px','fontWeight': 'bold'}),
            dbc.ListGroupItem("Nombre de pièce", color="secondary", style={'textAlign': 'center','width':'140px','fontWeight': 'bold'}),
            dbc.ListGroupItem("Nombre de chambre", color="secondary", style={'textAlign': 'center','width':'110px','fontWeight': 'bold'}),
            dbc.ListGroupItem("Taille", color="secondary", style={'textAlign': 'center','width':'200px','fontWeight': 'bold'}),
        ],horizontal=True,className="mb-2",)
        ]

        if select_ville== '':
            select_ville= 'Paris'

        if select_cp== '':
            select_cp= '75001'
        # Requete pour grouper en fontion de la ville et du code postal 
        cur2 = collection6.find({"$and":[{"Ville" : select_ville}, {"code postal" : select_cp}]})
        
        lst_2 = recup_list(cur2)
         
        data = pd.DataFrame(lst_2)
        data= data.drop_duplicates(subset =["prix", 'm2'])
        # Mise à jour du classement
        for i in range(data.shape[0]):
            children.append(dbc.ListGroup([
                dbc.ListGroupItem(lst_2[i]['lieux'], style={'textAlign': 'center','width':'300px'}),
                dbc.ListGroupItem(lst_2[i]['prix'], style={'textAlign': 'center','width':'110px'}),
                dbc.ListGroupItem(lst_2[i]['pièce'], style={'textAlign': 'center','width':'140px'}),
                dbc.ListGroupItem(lst_2[i]['chambre'], style={'textAlign': 'center','width':'110px'}),
                dbc.ListGroupItem(lst_2[i]['m2'], style={'textAlign': 'center','width':'200px'}),
        ],horizontal=True,className="mb-2",))
        return children

    # POur afficher les graphiques en fonction de la ville séléctionnée 
    @app.callback(
        [Output('graph3', 'figure'),Output('graph4', 'figure'),Output('graph5', 'figure')],
        [Input('selection-ville2', 'value') ])
        
    def update_figure2(select_ville):
        
        if select_ville == '' :
            select_ville = 'Paris'

        arrondissement= collection6.aggregate([{"$match":{"Ville":select_ville}},
                        {"$group" :{
    
                            "_id" : "$code postal",
                            "prixmoyen": { "$avg": "$prix" },
                            "m2moyen": { "$avg":"$m2"}
                            }}, 
                            {"$project": {
                                "prixmoyen": 1,
                                "m2moyen": 1,
  
                                          "prix moyen du m2":{"$divide" :["$prixmoyen","$m2moyen"]},
                            }}
                              ])
        b= []
        for i in arrondissement:
           b.append(i)                      
        #b=(recup_list(arrondissement))
        df_arrondissement = pd.DataFrame(b)
        
        #df_arrondissement = df_arrondissement.drop(df_arrondissement.columns[-1],axis=1)
        df_arrondissement["prixmoyenm2"]=df_arrondissement['prixmoyen']/df_arrondissement['m2moyen']
        #arrond=dfParis_arrondissement["_id"].unique()
        a=df_arrondissement[df_arrondissement['_id']==''].index
        df_arrondissement=df_arrondissement.drop(index=a)

        fig = px.histogram(df_arrondissement, x="_id", y=["prixmoyen"],
                     color="_id",
                     title="Prix moyen par arrondissment")


        fig1 = px.histogram(df_arrondissement, x="_id", y=["m2moyen"],
                     color="_id",
                     title="Repartition des m2") 

        fig2 = px.histogram(df_arrondissement, x="_id", y=["prixmoyenm2"],
                     color="_id",
                     title="Prix moyen du m2 par arrondissment")                 


        return fig , fig1, fig2

app.run_server(debug=True)        




