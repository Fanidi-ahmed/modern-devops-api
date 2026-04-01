x# modern-devops-api

Projet backend moderne construit pour, pratiquer et démontrer une stack DevOps applicative complète autour de FastAPI.

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
├── .gitignor
└── README.md
