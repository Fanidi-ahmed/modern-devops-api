x# modern-devops-api

Projet backend moderne construit pour apprendre, pratiquer et démontrer une stack DevOps applicative complète autour de FastAPI.

Ce projet montre comment construire une API REST avec authentification JWT, base de données PostgreSQL, cache Redis, Docker, Swagger/OpenAPI, et une structure de code propre prête à évoluer vers CI/CD, Kubernetes et cloud AWS.

---

## Objectif du projet

L’objectif est de construire une API moderne qui permet de :

- créer des utilisateurs
- lire la liste des utilisateurs
- se connecter avec email + mot de passe
- générer un token JWT
- accéder à une route protégée
- modifier ou supprimer un utilisateur avec authentification
- utiliser Redis comme cache
- exécuter l’application dans des conteneurs Docker

Ce projet sert de base pédagogique pour plusieurs suites possibles :

- pipeline CI/CD GitHub Actions
- pipeline Jenkins
- version Kubernetes
- version SaaS
- déploiement cloud AWS
- intégration Terraform

---

## Stack technique

### Backend
- FastAPI
- Uvicorn
- SQLAlchemy
- Pydantic

### Base de données
- PostgreSQL

### Cache
- Redis

### Sécurité
- JWT avec `python-jose`
- hash des mots de passe avec `passlib` + `bcrypt`

### Conteneurisation
- Docker
- Docker Compose

### Documentation API
- Swagger / OpenAPI

### Tests
- pytest

### Monitoring
- Prometheus FastAPI Instrumentator

---

## Architecture générale

```text
Client / curl / Swagger
          ↓
       FastAPI
          ↓
 Redis (cache lecture)
          ↓
   PostgreSQL (source de vérité)
   Rôle de chaque composant
FastAPI

Reçoit les requêtes HTTP, applique la logique métier, valide les entrées, renvoie les réponses JSON.

PostgreSQL

Stocke les données de manière durable. C’est la source principale des utilisateurs.

Redis

Stocke temporairement certaines réponses pour accélérer les lectures.

Swagger

Permet de visualiser et tester l’API dans le navigateur.

Docker

Emballe les services dans des conteneurs pour exécuter le projet de manière reproductible.

Structure du projet
modern-devops-api/
├── backend/
│   ├── app/
│   │   ├── auth.py
│   │   ├── database.py
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   └── security.py
│   ├── tests/
│   │   └── test_main.py
│   ├── requirements.txt
│   └── Dockerfile
├── docker-compose.yml
├── .github/
│   └── workflows/
│       └── ci.yml
├── .gitignore
└── README.md
Description des fichiers
backend/app/main.py

Fichier principal de l’application.

Il contient :

l’application FastAPI
les routes API
la logique de démarrage
la connexion Redis
la logique d’authentification sur les routes protégées
backend/app/database.py

Configure la connexion à PostgreSQL.

Il contient :

l’URL de connexion
le moteur SQLAlchemy
la session de base de données
la base ORM
backend/app/models.py

Définit la structure des tables SQLAlchemy.

Dans ce projet :

modèle User
backend/app/schemas.py

Définit les schémas Pydantic utilisés par l’API.

Ils servent à :

valider les données entrantes
documenter les réponses
séparer la structure API de la structure base de données
backend/app/auth.py

Gère les tokens JWT :

création du token
vérification du token
backend/app/security.py

Gère la sécurité des mots de passe :

hash du mot de passe
vérification du mot de passe
backend/tests/test_main.py

Contient des tests simples pour valider le fonctionnement de l’application.

backend/Dockerfile

Décrit comment construire l’image Docker du backend.

docker-compose.yml

Orchestre les services :

api
db
redis
Fonctionnalités actuelles
Utilisateurs
création d’un utilisateur
lecture de la liste des utilisateurs
modification d’un utilisateur
suppression d’un utilisateur
Authentification
login avec email + mot de passe
génération d’un token JWT
route protégée /me
Cache
la route GET /users peut utiliser Redis
le cache est invalidé après création, modification ou suppression
Endpoints disponibles
Publics
GET /

Vérifie que l’API fonctionne.

POST /users

Crée un utilisateur.

Exemple de body JSON :

{
  "name": "Ahmed",
  "email": "ahmed@example.com",
  "password": "secret123"
}
GET /users

Retourne la liste des utilisateurs.

POST /login

Authentifie un utilisateur avec email et password et retourne un token JWT.

Exemple :

POST /login?email=ahmed@example.com&password=secret123
Protégés
GET /me

Retourne les informations de l’utilisateur connecté.

Header attendu :

Authorization: Bearer <token>
PUT /users/{user_id}

Met à jour un utilisateur.

DELETE /users/{user_id}

Supprime un utilisateur.

Authentification JWT

Le flux est le suivant :

le client crée un utilisateur
le mot de passe est hashé avant stockage
le client se connecte avec email + mot de passe
le serveur vérifie le hash
le serveur génère un token JWT
le client envoie ce token dans le header Authorization
les routes protégées vérifient le token avant d’autoriser l’accès
Pourquoi le mot de passe n’est jamais stocké en clair

Le mot de passe utilisateur n’est jamais conservé tel quel en base.

Le serveur :

reçoit le mot de passe
calcule un hash sécurisé
stocke uniquement ce hash

Au login :

le mot de passe fourni est comparé au hash
si la vérification est correcte, le login réussit

C’est une pratique essentielle en sécurité backend.

Lancement du projet
Prérequis
Docker
Docker Compose
Démarrage
docker compose up --build
URLs utiles
API : http://127.0.0.1:8001
Swagger : http://127.0.0.1:8001/docs
Metrics : http://127.0.0.1:8001/metrics
Tests manuels avec curl
1. Vérifier l’API
curl http://127.0.0.1:8001/
2. Créer un utilisateur
curl -X POST http://127.0.0.1:8001/users \
  -H "Content-Type: application/json" \
  -d '{"name":"Ahmed","email":"ahmed@example.com","password":"secret123"}'
3. Lire les utilisateurs
curl http://127.0.0.1:8001/users
4. Se connecter
curl -X POST "http://127.0.0.1:8001/login?email=ahmed@example.com&password=secret123"
5. Accéder à la route protégée
curl http://127.0.0.1:8001/me \
  -H "Authorization: Bearer TON_TOKEN"
6. Modifier un utilisateur
curl -X PUT http://127.0.0.1:8001/users/1 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer TON_TOKEN" \
  -d '{"name":"Ahmed Updated","email":"ahmed_new@example.com","password":"newsecret123"}'
7. Supprimer un utilisateur
curl -X DELETE http://127.0.0.1:8001/users/1 \
  -H "Authorization: Bearer TON_TOKEN"
Tests avec Swagger

Ouvrir :

http://127.0.0.1:8001/docs

Depuis Swagger, tu peux :

voir tous les endpoints
tester les requêtes directement
remplir les bodies JSON
lire les réponses
utiliser le bouton d’autorisation si nécessaire
Exécution des tests Python

Depuis le dossier backend :

pytest
Cache Redis : logique

La route GET /users essaye d’abord de lire depuis Redis.

Si le cache existe

la réponse est renvoyée rapidement

Sinon

l’API lit PostgreSQL, renvoie la réponse, puis remplit Redis

Pourquoi invalider le cache ?

Après :

POST /users
PUT /users/{id}
DELETE /users/{id}

le cache est supprimé pour éviter de renvoyer des données obsolètes.

Points pédagogiques clés

Ce projet permet d’expliquer clairement :

ce qu’est une API
la différence entre backend et base de données
le rôle du cache Redis
la différence entre modèle ORM et schéma Pydantic
les méthodes HTTP : GET, POST, PUT, DELETE
l’authentification JWT
le hash des mots de passe
Docker et Docker Compose
Swagger
Git et GitHub
Limites actuelles

Ce projet est pédagogique. Certaines améliorations sont possibles :

migrations Alembic
rôles utilisateur
contrôle fin des autorisations
refresh tokens
variables d’environnement plus robustes
logs structurés
tests plus complets
CI/CD enrichie
déploiement Kubernetes
déploiement cloud AWS
Évolutions prévues

Ce projet peut évoluer vers :

github-actions-fastapi-ci
jenkins-devops-pipeline-lab
modern-devops-api-k8s
saas-starter-fastapi
terraform-aws-app-stack
boto3-aws-audit-tools
Auteur

Projet réalisé dans une logique d’apprentissage pratique DevOps / backend / cloud avec objectif de montée en compétences, démonstration GitHub et futur usage en formation technique.


---

# Plan de test simple pour `modern-devops-api`

Après avoir mis ce README, voici l’ordre de test que je te conseille :

```bash
docker compose down -v
docker compose up --build

Puis dans un autre terminal :

curl http://127.0.0.1:8001/
curl -X POST http://127.0.0.1:8001/users \
  -H "Content-Type: application/json" \
  -d '{"name":"Ahmed","email":"ahmed@example.com","password":"secret123"}'
curl http://127.0.0.1:8001/users
curl -X POST "http://127.0.0.1:8001/login?email=ahmed@example.com&password=secret123"

Puis avec le token :

curl http://127.0.0.1:8001/me \
  -H "Authorization: Bearer TON_TOKEN"

Puis :

curl -X PUT http://127.0.0.1:8001/users/1 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer TON_TOKEN" \
  -d '{"name":"Ahmed Updated","email":"ahmed_new@example.com","password":"newsecret123"}'

Puis :

curl http://127.0.0.1:8001/users
Prompt prêt à copier pour une autre page

Tu m’as demandé un prompt pour ouvrir d’autres pages et continuer sur les autres projets.
Voici un prompt général très bon, que tu peux réutiliser.

Prompt générique
Tu es mon formateur expert en DevOps, cloud AWS, Terraform, Python, Linux, Docker, Kubernetes et automatisation.

Je veux construire un projet GitHub propre, pédagogique, progressif et réutilisable pour mon portfolio et mes futures formations.

Travaille avec moi en mode terminal + EOF, étape par étape, sans sauter d’étapes.
À chaque étape :
- donne l’objectif
- explique la logique simplement et techniquement
- crée les fichiers en mode EOF
- fais tester ce qu’on vient de construire
- explique les erreurs possibles
- garde une structure de projet propre
- pense toujours à la pédagogie, car je veux devenir formateur

Je veux un projet concret, bien structuré, avec un README professionnel à la fin.

Commence par me proposer :
1. l’objectif du projet
2. l’architecture
3. l’arborescence
4. l’ordre des étapes
Puis on construit fichier par fichier.
Prompts spécifiques pour plusieurs projets cloud AWS

Je te propose une liste de projets très cohérente avec ton objectif.

1. Projet Terraform AWS réseau
Je veux construire un projet GitHub nommé terraform-aws-network-lab.

Objectif :
apprendre et démontrer la création d’une base réseau AWS avec Terraform.

Le projet doit inclure :
- VPC
- subnets publics et privés
- internet gateway
- route tables
- security groups
- outputs
- variables
- provider
- structure Terraform propre

Travaille avec moi en mode terminal + EOF, étape par étape.
Je veux comprendre chaque fichier et chaque ressource.
Je veux un projet pédagogique, prêt pour GitHub, avec un README détaillé à la fin.
Commence par :
1. architecture
2. arborescence
3. ordre de construction
4. premier bloc EOF
2. Projet Terraform AWS app stack
Je veux construire un projet GitHub nommé terraform-aws-app-stack.

Objectif :
déployer une stack applicative AWS avec Terraform.

Le projet doit inclure :
- VPC
- subnets
- security groups
- EC2 ou ECS
- ALB
- RDS PostgreSQL
- IAM minimal
- outputs
- variables
- fichiers bien structurés

Travaille avec moi en mode terminal + EOF, étape par étape.
Explique toujours la logique cloud, réseau, sécurité et Terraform.
Je veux un projet propre pour portfolio et formation.
Commence par l’architecture cible et l’arborescence du repo.
3. Projet boto3 audit S3 et EC2
Je veux construire un projet GitHub nommé boto3-aws-audit-tools.

Objectif :
créer des scripts Python boto3 pour auditer un compte AWS.

Le projet doit inclure plusieurs scripts pédagogiques :
- lister les buckets S3
- vérifier le chiffrement S3
- lister les instances EC2
- récupérer les régions
- produire des rapports JSON ou CSV
- structure Python propre
- requirements
- README détaillé

Travaille avec moi en mode terminal + EOF, étape par étape.
Je veux comprendre le code ligne par ligne, la logique boto3, client vs resource, les erreurs courantes et la manière de tester.
Commence par l’architecture du projet et la structure des dossiers.
4. Projet Python automation Linux
Je veux construire un projet GitHub nommé python-linux-automation-lab.

Objectif :
créer plusieurs scripts Python utiles pour l’automatisation système et DevOps.

Le projet doit inclure :
- lecture/écriture de fichiers
- exécution de commandes shell
- rotation ou analyse de logs
- vérification espace disque
- vérification ports ouverts
- sauvegarde simple
- structure Python propre
- scripts testables

Travaille avec moi en mode terminal + EOF.
Je veux une progression pédagogique, étape par étape, avec explication claire de la logique Linux et Python.
Je veux un README détaillé à la fin.
Commence par la liste des scripts, l’arborescence, puis le premier script.
5. Projet Jenkins pipeline
Je veux construire un projet GitHub nommé jenkins-devops-pipeline-lab.

Objectif :
montrer un pipeline Jenkins propre autour d’une application backend.

Le projet doit inclure :
- Jenkinsfile
- stages build / test / docker build
- explication des agents, stages, steps
- possibilité d’ajouter scan sécurité plus tard
- README pédagogique
- structure claire

Travaille avec moi en mode terminal + EOF, étape par étape.
Explique Jenkins comme pour quelqu’un qui veut ensuite l’enseigner.
Commence par l’objectif, l’architecture du pipeline, l’arborescence, puis le premier bloc.
6. Projet Kubernetes
Je veux construire un projet GitHub nommé modern-devops-api-k8s.

Objectif :
prendre une API Docker existante et remplacer Docker Compose par Kubernetes.

Le projet doit inclure :
- Deployment
- Service
- ConfigMap
- Secret
- probes
- réplication
- explication claire de chaque manifest YAML
- README détaillé

Travaille avec moi en mode terminal + EOF, étape par étape.
Je veux comprendre comment passer d’un environnement Docker Compose à un environnement Kubernetes.
Commence par l’architecture cible et l’arborescence.
7. Projet multi-agents cloud / ops
Je veux construire un projet GitHub nommé multi-agent-cloud-ops-lab.

Objectif :
concevoir un projet pédagogique de workflow multi-agents orienté DevOps / cloud.

Le projet doit inclure :
- un agent planificateur
- un agent exécuteur
- un agent reviewer
- logique Python modulaire
- README clair
- structure de projet propre
- possibilité d’évolution vers outils cloud ou Terraform

Travaille avec moi étape par étape, de façon pédagogique et pratique.
Je veux d’abord la vision d’ensemble, les rôles des agents, l’arborescence, puis la construction fichier par fichier.
Quels projets cloud AWS différents je te conseille

Voici une sélection très cohérente et forte pour ton GitHub :

terraform-aws-network-lab
terraform-aws-app-stack
boto3-aws-audit-tools
python-linux-automation-lab
jenkins-devops-pipeline-lab
modern-devops-api-k8s
terraform-aws-eks-lab
terraform-aws-ecs-fargate-lab
aws-cost-visibility-scripts
cloud-compliance-mini-scanner
Ordre conseillé

Je te conseille cet ordre :

modern-devops-api
jenkins-devops-pipeline-lab
modern-devops-api-k8s
terraform-aws-network-lab
boto3-aws-audit-tools
python-linux-automation-lab
terraform-aws-app-stack
multi-agent-cloud-ops-lab
Mon conseil pratique

Commence par :

finir modern-devops-api
pousser ce repo sur GitHub avec le README détaillé
puis ouvrir une autre page avec le prompt de jenkins-devops-pipeline-lab
puis une autre avec terraform-aws-network-lab

Comme ça, tu avances de manière nette, repo par repo.

Le prochain meilleur choix, selon moi, est terraform-aws-network-lab, parce qu’il va très bien compléter ton repo API.