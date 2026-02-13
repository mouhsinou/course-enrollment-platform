# 🚀 Guide de Déploiement sur Render

## Prérequis

- Compte GitHub (pour héberger le code)
- Compte Render (gratuit) : https://render.com

## 📋 Étapes de Déploiement

### 1. Préparer le Repository Git

```bash
cd course-enrollment-platform

# Initialiser git si ce n'est pas déjà fait
git init

# Ajouter tous les fichiers
git add .

# Créer le premier commit
git commit -m "Initial commit - Course Enrollment Platform"

# Créer un repository sur GitHub et le lier
git remote add origin https://github.com/VOTRE_USERNAME/course-enrollment-platform.git
git branch -M main
git push -u origin main
```

### 2. Créer un Service Web sur Render

1. **Aller sur Render** : https://dashboard.render.com
2. **Cliquer sur "New +"** → **"Web Service"**
3. **Connecter votre repository GitHub**
4. **Configurer le service** :

   - **Name** : `course-enrollment-platform`
   - **Region** : Choisir la région la plus proche
   - **Branch** : `main`
   - **Root Directory** : (laisser vide)
   - **Runtime** : `Python 3`
   - **Build Command** : `./build.sh`
   - **Start Command** : `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### 3. Ajouter une Base de Données PostgreSQL

1. Dans le dashboard Render, cliquer sur **"New +"** → **"PostgreSQL"**
2. Configurer :
   - **Name** : `course-enrollment-db`
   - **Database** : `course_enrollment`
   - **User** : (généré automatiquement)
   - **Region** : Même région que le web service
   - **Plan** : Free (gratuit)

3. **Copier l'URL de connexion** (Internal Database URL)

### 4. Configurer les Variables d'Environnement

Dans les paramètres de votre Web Service sur Render, ajouter ces variables :

| Clé | Valeur |
|-----|--------|
| `DATABASE_URL` | URL PostgreSQL copiée (Internal Database URL) |
| `SECRET_KEY` | Générer une clé aléatoire sécurisée |
| `ALGORITHM` | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `30` |
| `DEBUG` | `False` |
| `PYTHON_VERSION` | `3.13.5` |

**Pour générer une SECRET_KEY sécurisée** :
```python
import secrets
print(secrets.token_urlsafe(32))
```

### 5. Déployer

1. Cliquer sur **"Create Web Service"**
2. Render va automatiquement :
   - Cloner votre repository
   - Installer les dépendances
   - Exécuter les migrations
   - Démarrer l'application

3. Attendre que le déploiement soit terminé (5-10 minutes)

### 6. Vérifier le Déploiement

Une fois déployé, votre API sera accessible à :
```
https://course-enrollment-platform-XXXX.onrender.com
```

**Tester les endpoints** :
- Documentation : `https://votre-app.onrender.com/docs`
- Health check : `https://votre-app.onrender.com/health`

## 🔧 Configuration Avancée

### Fichiers Créés pour le Déploiement

1. **`build.sh`** : Script de build qui installe les dépendances et exécute les migrations
2. **`Procfile`** : Commande pour démarrer l'application (optionnel sur Render)

### Variables d'Environnement Importantes

```env
# Production
DATABASE_URL=postgresql://user:password@host:5432/dbname
SECRET_KEY=votre-clé-secrète-très-longue-et-aléatoire
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
DEBUG=False
```

## 🎯 Après le Déploiement

### Créer un Utilisateur Admin

```bash
curl -X POST "https://votre-app.onrender.com/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Admin",
    "email": "admin@example.com",
    "password": "votre-mot-de-passe-sécurisé",
    "role": "admin"
  }'
```

### Tester l'API

Visitez : `https://votre-app.onrender.com/docs`

## 📊 Monitoring

Sur Render, vous pouvez :
- Voir les logs en temps réel
- Monitorer l'utilisation des ressources
- Configurer des alertes
- Voir les métriques de performance

## 🔄 Mises à Jour

Pour déployer des modifications :

```bash
git add .
git commit -m "Description des changements"
git push origin main
```

Render redéploiera automatiquement votre application !

## ⚠️ Notes Importantes

1. **Plan Gratuit Render** :
   - L'application peut se mettre en veille après 15 minutes d'inactivité
   - Premier démarrage peut prendre 30-60 secondes
   - 750 heures gratuites par mois

2. **Base de Données Gratuite** :
   - PostgreSQL gratuit avec 1GB de stockage
   - Expire après 90 jours (peut être renouvelé)

3. **CORS** :
   - Déjà configuré dans `app/main.py`
   - Modifier `allow_origins` pour la production si nécessaire

## 🆘 Dépannage

### Erreur de Migration
```bash
# Se connecter à la base de données et réinitialiser
alembic downgrade base
alembic upgrade head
```

### Voir les Logs
- Aller dans le dashboard Render
- Cliquer sur votre service
- Onglet "Logs"

### Redémarrer le Service
- Dashboard Render → Votre service → "Manual Deploy" → "Clear build cache & deploy"

## ✅ Checklist de Déploiement

- [ ] Code pushé sur GitHub
- [ ] Web Service créé sur Render
- [ ] Base de données PostgreSQL créée
- [ ] Variables d'environnement configurées
- [ ] Build réussi
- [ ] Migrations exécutées
- [ ] API accessible
- [ ] Documentation Swagger fonctionne
- [ ] Utilisateur admin créé
- [ ] Tests effectués

---

**Votre API est maintenant en production ! 🎉**

Pour toute question, consultez la documentation Render : https://render.com/docs
