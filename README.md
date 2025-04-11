# 🎮 Power4 App - Jeu de Puissance 4 en ligne

Bienvenue dans **Power4 App**, un jeu web complet de **Puissance 4** multijoueur (joueur vs joueur ou joueur vs IA). Il a été conçu avec **Flask** pour le backend, **React + Tailwind CSS** pour le frontend, et une IA configurable selon 3 niveaux de difficulté.

---

## 🔗 Démo en ligne

🌐 Application Web : [https://power4-app-j0yb0y28.vercel.app/](https://power4-app-j0yb0y28.vercel.app/)

---

## 📁 Structure du projet

```
power4-app/
├── backend/                   # API Flask + logique du jeu
│   ├── app.py                 # API REST (démarrage, move, IA)
│   └── logic.py               # Moteur du jeu Puissance 4 avec IA
├── frontend/                  # Application React + Tailwind
│   ├── public/                # favicon, index.html
│   └── src/                   # Composants React, GameBoard, App.js, styles
```

---

## ✨ Fonctionnalités

- 👥 Mode Joueur vs Joueur (local)
- 🤖 Mode Joueur vs IA avec **3 niveaux** de difficulté (facile / moyen / difficile)
- 🧠 IA Minimax avec élagage alpha-bêta pour le mode difficile
- ⏱️ Calcul du **temps de réflexion** pour chaque joueur
- 🧑 Saisie de pseudo pour chaque joueur
- 🟩 Surlignage des **jetons gagnants** à la fin de la partie
- 🎵 Son de victoire + animation de fin
- 🌙 Interface moderne, responsive, et agréable

---

## 🚀 Installation locale

### 1. Cloner le projet

```bash
git clone https://github.com/J0YB0Y28/power4-app.git
cd power4-app
```

### 2. Backend : Flask

```bash
cd backend
python -m venv venv
source venv/bin/activate        # (Linux/Mac) ou venv\Scripts\activate (Windows)
pip install -r requirements.txt
python app.py                   # Lance l'API Flask
```

### 3. Frontend : React

```bash
cd frontend
npm install
npm run dev                     # Lance le serveur de développement React
```

---

## 🛰️ Déploiement

- 🎯 Backend Flask : déployé sur [Render](https://render.com)
- 🎯 Frontend React : déployé sur [Vercel](https://vercel.com)

---

## 🙌 Auteur

Projet réalisé par **J0YB0Y28**  
📧 Contact : [kanaboumkwoiit@outlook.com](mailto:kanaboumkwoiit@outlook.com)  
🔗 [Portfolio](https://j0yb0y28.github.io/portfolio/) · [GitHub](https://github.com/J0YB0Y28) · [LinkedIn](https://www.linkedin.com/in/teddy-kana-6a26832b9/)

---

## ⭐ Technologies utilisées

- `Flask`, `Flask-CORS` pour le backend
- `React`, `Tailwind CSS` pour l’interface
- `Vercel` + `Render` pour le déploiement
- `Math`, `Minimax`, `random` pour l’intelligence artificielle

---

## ✅ Idées d'améliorations futures

- [ ] Mode multijoueur en ligne (avec WebSocket)
- [ ] Ajout d'un système de score ou classement local
- [ ] Export des parties ou replay
- [ ] Personnalisation des couleurs ou avatars

---

## 🖼️ Aperçu du jeu

<img src="frontend/public/demo-ui.png" width="600">

