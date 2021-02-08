# Web Application Data Engineering - Bet scraper
*Projet de l'unité Data Engineering*

**Maxime Robillard et Victor Kaczmarczyk**

L'objectif de notre projet est de scraper différents site de paris sportifs et de comparer les côtes par match. Pour l'instant, nous scrapons seulement deux sites Netbet et Zebet.
Nous avons créé un dashboard pour la visualisation des différentes statistiques sur les équipes et les matchs à venir, ce qui devrait permettre à l'utilisateur de prendre de meilleures décisions. Nous aurions aimé entrainer une intelligence artificielle qui à l'aide d'une fonction de score trouve les meilleures combinaisons de paris avec les différents sites et donc minimise le risque de perte.
Nous avons aussi réalisé un moteur de recherche à l'aide d'elasticsearch, ce qui permet de rechercher une équipe, un championnat ou un site en particulier.

**Pour démarrer l'application Flask**

A la racine du projet "multi-docker" taper la commande : 'docker-compose up -d build'

*Création de la base de donnée mongodb*

Taper les commandes :
- 'docker exec -it mongodb1 bash'
- 'mongo'
- 'use mongodb'
- 'db.createCollection("Bet")'

Ceci est nécessaire si la base de données n'est pas instanciée.

*Pour réinitialiser la base de données*  

taper les commandes :
- 'docker exec -it mongodb1 bash'
- 'mongo'
- 'use mongodb'
- 'db.Bet.seleteMany({})'

**Infos partie Scraping :**  

Les fichiers utiles sont situés dans le dossier 'Scraper/Scraper/'.
Il y a pour l'instant 2 spiders, netbet et zebet. Elles retournent des Items qui contiennent le site, la date du jour de scraping,le championnat ,le nom des équipes, les différentes côtes et le jour du match.

Pour lancer manuellement les spiders, taper 'scrapy crawl <spider name>'.

**Infos partie Flask**

Le seul à exécuter si nous n'utilisons pas docker est 'run.py'. L'architecture est une architecture MVC classique d'une application sous FLask. A la racine du projet se trouve le 'run.py' qui instancie l'application et le 'requirements.txt' qui contient les librairies à installer. Dans le dossier 'App' se trouve le '__init__.py' qui instancie l'application, le 'routes.py' qui regroupe les routes de notre application et certaines fonctions associées. Dans le dossier "templates" se trouve les différents fichiers html et dans le dossier static se trouve les fichiers utiles au design.

**Infos partie Docker**

Pour les dockers nous avons choisi de créer :
- Un docker pour flask **Dockerfile_flask** : Container contenant l'application Flask et qui se charge de lancer l'application sur le **port 5000**
- Un docker pour le scraper **Dockerfile_scraper** : Container qui lance le scraper avec scrapyrt sur le **port 9080** et permet de scraper nos différents site via l'API ScrapyRT.
- Un container **Mongodb** : Nous utilisons une image  mongo:4.0.8 . Mongo est une base de donnée permettant le stockage sur le long terme. Elle sera sur le **port 27017**
- Un container **Elasticsearch** : Nous utilisons une image venant du site ***docker.elastic.co***. Base de données utilisée pour le moteur de recherche. Il tourne sur le port **port 9200**.
- Un container **kibana** : Nous utilisons une image venant aussi de  ***docker.elastic.co***. Kibana permet de créer rapidement des dashboard, nous ne l'avons pas utilisé ici sauf pour l'administration des données sous elasticsearch.
- Le **docker-compose.yml** qui permet de lier les différents containers et dockers. Ce qui permet a l'ensemble de fonctionner et d'intégrer le scraper et la base de données dans l'appli flask.


**Infos Arbitrage**

Les fonctions reliées au calcul de l'arbitrage se trouvent dans le dossier 'fonctions' dans le dossier 'App'. Actuellement nous n'avons que deux bookmakers, il se peut donc qu'il n'y ait pas de paris sûr. En effet, ce cas de figure n'arrive que si la somme des inverses des côtes maximales d'un match est inférieur à 1. C'est pourquoi les graphiques affichant les paris sûrs et profits sont vides. Cependant, une version test est disponible dans le dossier dashboard Taper 'py main.py' dans ce dossier pour le tester. Il sera hébergé sur le localhost:8050.

Pour lancer le tout, taper la commande 'docker-compose up --build' lors de la première utilisation. Pour l'éteindre utiliser 'ctrl+c' et pour relancer le tout 'docker-compose up'.
L'application tournera sur le **port 5000**

L'applicaton flask se trouve sur "localhost:5000" et le scraper en temps réel sur 'localhost:9080 + requête' (exemple: http://localhost:9080/crawl.json?spider_name=netbet&url=https://www.netbet.fr/football/angleterre/premier-league?tab=matchs).
Elasticsearch se trouve à l'adresse 'http://localhost:9200/bet'
