# DatavizPython

*Introduction* 

Pour notre projet de DataEngineer Tools nous avons décidé de nous intéresser aux biens immobilier à vendre dans les 10 plus grandes villes de France disponible sur le site particulieraparticulier.fr ([lien](https://www.pap.fr/annonce/vente-maisons-paris-75-g439)) 
Notre but ici n'était pas de recréer un site avec des offres immobiliers, mais plutôt de créer un outil d'analyse et de permettre aux utilisateurs une meilleure visualisation du marchés immobilier actuel à l'aide de plusieurs indicateurs/filtres différent.
En effet en parcourant les nombreuses pages d'offre sur les sites d'agences immobilières il est facile de se perdre. Notre but est donc de proposer une vue globale de ce qui est disponible en ce moment pour pouvoir adapter sa demande en fonction de ce qui est le plus rentable et le mieux pour soit.

Ainsi l'utilisateur peut regarder si les offres sur le site particulieràparticuliersuivent l'évolution du marchés immobilier. En effet, grâce au fichier scrappy.py l'utilisateur peut à tout moment récupérer les offres du site juste en l'exécutant.
Pouvoir scrapper les données lorsque l'on veut permet d'avoir des données qui évoluent au fur et à mesure du temps.

Nous avons donc scrappé les informations concernant les maisons à vendre sur le site en question en nous focalisant sur le prix, la taille (en m2), le nombre de chambre, le nombre de pièce et la localisation avec la ville et le code postal.
Pour avoir des données actualiser :
L'utilisateur devra juste changer le nom du fichier json qu'il va générer a la fin du code qui par défaut sera nommé scrapping.json.
Il devra ensuite mettre le même nom qu'il a choisit dans le début du code python et changer le nom de la collection qui sera immobilier de base par immobilier_v1, immobilier_v2 et ainsi de suite

Une fois les données du du site particulier à particulier scrappé, nous avons un dictionnaire de liste qui se compose de la manière suivante:
-    le lieux
-    la ville
-    le code postal
-    le prix
-    la description
-    le nombre de pièce
-    le nombre de chambre
-    le nombre de m2

<br>


### User Guide

*Installation*

Pour pouvoir avoir accès au dashboard il vaus faut suivre les étapes suivantes : 

*  installer un serveur mongo sur sa machine(ex:MongoDB Compass):

*  Copier le projet sur votre machine grace à la commande :

* [ ]  `$ git clone https://git.esiee.fr/kulaveen/projet_python_e4`

* Verifiez que les fichiers suivant soit dans le même repertoire : 

* [ ]  `scrappy.py`
* [ ]  `app.py`

* Ouvrez votre terminal anaconda et taper la commande suivante : 

* [ ]  `conda install -c conda-forge dash-bootstrap-components`

*  Sur VisualStudioCode ouvrir le projet que vous venez de téléchargé : File > Open Folder... séléctionner le fichier téléchargé

* Avant de pouvoir lancer le projet il faut au préalable installer les packages nécéssaires. Pour cela taper les commande suivantes dans votre console : 

* [ ]  `pip install dash`

* [ ]   `pip install plotly`

* [ ]  `pip install pandas`

* [ ]  `pip install pymongo`

* [ ]  `pip install json`

* Exécutez en premier le fichier scrappy.py afin de pouvoir créer le fichier scrapping.json


* A partir du Terminal sous VisualStudioCode lancer le script grace à la commande:

* [ ] `python3 app.py` pour Linux
* [ ] `python app.py`  pour Windows

* A la fin de l'éxécution du script, l'adresse http://127.0.0.1:8050/ est renvoyée. Utilisez cette adresse pour visualiser le DashBoard.


<br>


### Developper Guide

Pour comprendre le programme, nous allons nous intéresser à quatre points qui sont le **scraping**, **la base données Mango/requetes**, **le layout** et **les callbacks/updates**.

**scraping**: 
On uilise BeautifulSoup pour scrapper nos données, par ailleur, BeautifulSoup nous permet de contourner l'erreur 403 qui empêche le scrapping.


**MongoDB**: 
Mango est une base de données NosSQL orientée document. Elle se distingue des bases de données relationnelles par sa flexibilité et ses performances.
Nous l'avons utilisé ici pour regrouper toutes nos données scrapées dans une collection. De ce fait nous avons pu 

**Traitement de données**:
Cette étape est primordiale pour le bon déroulement du projet, cela se passe directement après les imports et commence avec des *pd.read_csv*.
*pd.read_csv* permet d’ouvrir et visualiser les dataframes
On abandonne les colonnes qui ne nous sont pas intéressante avec un *.drop*
C’est là qu'on créer plusieurs sous dataframe afin de pouvoir les utiliser sans modifier notre dataframe mère.
On joint différent dataframe entre eux mais qui possède au moins une colonne commune grâce à *pd.merge*
Ainsi si vous voulez étudier d'autres caractéristiques de notre base de données , il vous faudra surement d’abord créer un sous dataframe sur lequel vous voulez travailler .

**Les figures**:
Cette partie du code se trouve juste après *app=dash.Dash(_name_)*  et avant le layout. C’est ici que sont défini les graphiques à tracer grâce à plotly express avec *px.line*,*px.scatter*,*px.histogram*   
Ainsi, si vous voulez ajouter des figures, graphiques, c’est dans cette partie que vous devez les définir.

**Le layout**:
app.layout permet de structurer le dashboard et décide de ce qui doit être affiché sur l’écran de l’utilisateur.
Dans cette partie on a 
- le titre du dashboard avec *html.H1*
- les description et les zones de textes avec *html.Div*
- la représentation du début de notre dashboard avec *dash_table.DataTable*
- la représentation des figures que l’on a définit plus avec *dcc.Graph*
- des dropdowns avec *dcc.Dropdow*n
- des slider avec *dcc.Slider*
Ainsi si vous voulez modifier l’affichage du dashboard, c’est ici qu’il faut faire des mofications

**Les callbacks/updates**:
Cette partie est l’élément clé pour avoir un dashboard interactif.
- *@app.callback()* indique quels sont les inputs et outputs à prendre en compte et à actualiser, pour cela, les graphiques ou encore les dropdown/slider possède des id que l’on définit lors de leur création dans le layout. Ces id sont données en argument pour les inputs et outputs.
- *update_figure()* prend en argument le nombre d' inputs défini dans le *@app.callback()* qui seront par ailleurs traités dans l’ordre d’apparition dans le callback et retourne le même nombre d'éléments que de outputs défini dans le callback.

### Rapport d'analyse

*Conclusion*


L'Organisation météorologique mondiale a annoncé que les 10 années se terminant à partir de fin 2019 sont les 10 années les plus chaudes de l'histoire mondiale.
En effet avec nos visualisations nous avons pu observer que la température moyenne mondiale augmente de façon alarmante au cours des deux dernières décennies. 
En analysant les graphiques on observe que toutes les régions sont touchées par ce réchauffement climatique dans une certaine mesure. Dans certaines régions, la température a augmenté plus rapidement, les cas les plus notoires sont : l'Asie, le Moyen-Orient, l'Amérique du Nord et l'Europe. En effet il s'agit des régions les plus développées donc avec une dynamique économique élévée (industries lourdes, import, export, ...) .
Il est également possible de voir que l'année 2019 est, dans la plupart des cas, celle qui a la température moyenne maximale.

Comme vous le savez nous traversons actuellement une grave crise sanitaire dû à la pandémie du Covid-2019 apparue en novembre 2019 et qui a entrainé le monde dans un effondrement de l’activité économique et humaine dû à des mesures de confinement, de distanciation imposée par les États pour palier a cette épidémie. 
Il serait donc intéressant, lorsque ce dataset sera mis à jour, de voir quel impact a eu cette crise sur les températures des années suivantes, et si elle a permis de réduire la vitesse du réchauffement climatique. 

Il serait également intéressant de pouvoir utilisé ce jeu de données pour pouvoir prédire l’évolution des températures dans les années à venir pour avoir une idée de ce qui nous attend si nous n’agissons pas maintenant. 
Pour cela nous pourrions utiliser les années 1995 à 2014 comme données d’entrainement et valider notre algorithme grâces aus données des années 2015 à 2019. 

