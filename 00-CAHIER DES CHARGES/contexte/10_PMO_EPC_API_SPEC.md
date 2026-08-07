# PMO_EPC_API_SPEC.md

# PMO EPC Platform
## API & Service Specification

Version : 1.0
Auteur : GED-SERVICES
Statut : Architecture cible

---

# Objectif

Même si PMO EPC est aujourd'hui une application Django "monolithique", toute
l'architecture est pensée pour évoluer naturellement vers :

- REST API
- API interne
- Micro-services
- Mobile
- Power BI
- Primavera
- SAP
- EDMS externes

Les vues Django ne doivent jamais contenir la logique métier.

Toute la logique doit être placée dans les Services.

---

# Architecture

```
Views
    │
    ▼
Services
    │
    ▼
Models
```

Jamais :

```
View
    ▼
Model
```

---

# Principe

Une View :

- récupère les paramètres
- appelle un Service
- transmet le Context

Exemple :

```python
def dashboard(request):

    context = dashboard_service(request)

    return render(
        request,
        "planning/dashboard.html",
        context
    )
```

---

# Services

Chaque module possède son propre dossier :

```
apps/

planning/

services/

dashboard.py
gantt.py
calendar.py
retards.py
charge.py
jalons.py
...
```

---

# Règles

Un service :

- ne retourne jamais du HTML
- retourne uniquement des données Python

Exemple :

```
{
    "projects": ...,
    "statistics": ...,
    "late_tasks": ...
}
```

---

# API interne

Chaque Service pourra être utilisé :

- par les Views Django
- par les API REST
- par les exports Excel
- par les exports PDF
- par les tableaux Power BI
- par les WebSockets

sans duplication.

---

# API REST future

```
/api/projects/

/api/contracts/

/api/tasks/

/api/planning/

/api/costs/

/api/risks/

/api/documents/
```

---

# Exemple

GET

```
/api/tasks/
```

Retour

```json
[
    {
        "id":1,
        "name":"Installation",
        "progress":42
    }
]
```

---

# Dashboard

```
GET

/api/dashboard
```

retourne

```
KPIs

Widgets

Charts

Alerts

Statistics
```

---

# Planning

```
GET

/api/planning/projects
```

```
GET

/api/planning/contracts
```

```
GET

/api/planning/calendar
```

```
GET

/api/planning/gantt
```

---

# Planning Project

```
GET

/api/planning-project
```

```
GET

/api/planning-project/baselines
```

```
GET

/api/planning-project/resources
```

```
GET

/api/planning-project/dependencies
```

```
GET

/api/planning-project/critical-path
```

---

# Documents

```
GET

/api/documents
```

```
GET

/api/transmittals
```

```
GET

/api/mdr
```

```
GET

/api/document-progress
```

---

# Coûts

```
GET

/api/costs
```

```
GET

/api/costs/evm
```

```
GET

/api/costs/forecast
```

---

# Reporting

```
GET

/api/reporting/dashboard
```

```
GET

/api/reporting/project
```

```
GET

/api/reporting/contract
```

---

# Authentification

Aujourd'hui :

Session Django

Demain :

JWT

OAuth2

Azure AD

Microsoft Entra ID

LDAP

---

# Formats

JSON

CSV

Excel

PDF

XML

---

# Import

Excel

CSV

Primavera XER

MS Project XML

SAP

---

# Export

Excel

PDF

Power BI

Primavera

MS Project

---

# API Versioning

Toujours prévoir :

```
/api/v1/
```

puis

```
/api/v2/
```

afin d'éviter toute rupture de compatibilité.

---

# Bonnes pratiques

Les Services :

- ne connaissent pas HTTP
- ne connaissent pas Django Templates
- ne connaissent pas Bootstrap

Ils manipulent uniquement :

- modèles
- calculs
- règles métier

Les Views :

- affichent
- contrôlent les permissions
- construisent le contexte

Les Templates :

- affichent uniquement.

Aucun calcul métier ne doit être présent dans les templates.

---

# Objectif final

L'ensemble du système devra pouvoir être utilisé simultanément par :

- Interface Web Django
- API REST
- Application Mobile
- Power BI
- Scripts Python
- IA (ChatGPT, Claude, DeepSeek, Copilot)
- ERP externes
- EDMS externes

sans modifier la logique métier.