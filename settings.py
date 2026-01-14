import os

# Configuration de l'écran
LARGEUR_ECRAN = 800
HAUTEUR_ECRAN = 600
FPS = 60

# Couleurs
COULEUR_FOND = (30, 30, 30)
BLANC = (255, 255, 255)
ROUGE_VIE = (255, 100, 100)
JAUNE_INV = (255, 255, 0)

# Chemins des assets
# On définit le chemin vers le dossier Assets
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "AllDatas", "Assets")
IMAGE_VAISSEAU = os.path.join(ASSETS_DIR, "vaisseau.png")

# Paramètres de jeu
NB_ENNEMIS_MAX = 3
