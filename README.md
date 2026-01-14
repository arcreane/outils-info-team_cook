Lien Trello : https://trello.com/invite/b/695b9fed03691f9b2a0b69ea/ATTIa44be20536384883263258cce41a843883B0FD7A/tableau-tp



Type de jeu : Shoot Them Up



Equipe de développement: Nicolas Pham, Ahmed Omar, Tom Merlet, Noah Mausse, Simon Beilin-Melseaux



Description du jeu : Un shoot 'em up (aussi écrit shoot them up ou contracté en shmup ; littéralement « abattez-les tous ») est un genre de jeu vidéo dérivé du jeu d'action dans lequel le joueur dirige un véhicule ou un personnage devant détruire un grand nombre d'ennemis à l'aide de projectiles, au fur et à mesure des niveaux, tout en esquivant les projectiles adverses pour rester en vie.



Organisation : Développement de différents petits projets à merge au fur et a mesure. 



Règle de contribution: 



-Discutez avant d'agir : Avant d'ajouter une grosse fonctionnalité, ouvrez une "Issue" pour en discuter avec l'équipe.



-Code propre et testé : Assurez-vous que votre code est lisible, bien commenté et qu'il ne casse pas le gameplay existant.



-Respect des droits : N'utilisez que des images ou des sons libres de droits et citez vos sources dans votre proposition.

# Branch ####
-main (la branche principale)
-PresentationTom
-nepastoucherSimon
AhmedPresentation3
SimonPrésentation
PresentationNoah
PresentationNico
AhmedPresentation
# main.py ####
Fichier principal du projet. Permet le lancement du jeu, importe le module "pygame" et le fichier python "settings" .Avec "sys" et "os" importés on peut créer une liste "dossiers" et l'ajouter à l'exécution du projet
Importer game to Game. Puis créer la fonction main pour créer une fenêtre et ajouter un temps. "vitess_actuelle" =60 fps ou égale 20 si touche " maj" pressée.
Dans le jeu un délai avant de quitter la fenêtre et sortir du jeu.

# game.py ####
Fichier python important pygame,random, settings,AllDatas.Entities.[fichier].
Création de class Game:pour la mise en place de l'écran avec la police , le socre, le boss_mode = false et boss= None, pour ne pas faire apparaître le boss.
La gestion des armes se fait avec weapon_manager
### Création de groupes
-Sprites
-ennemis
-tirs de joueurs
-tirs du boss
-les pouvoirs
# Joueur
Cette partie sert à définir le joueur avec sprites
# Spawn initial
 Fait apparaître l'ennemi , le définit avec le groupe et les sprites appartenants.

# Evenements
Si l'événement est égale à pygame.QUIT, alors self.runnig est faux. Ceci fermera la

# Définir les touches
 Si l'espace est pressée (soit "K_SPACE") alors le joueur tire.

# Apparition Boss
Si le score est supérieur ou égale à 100, alors le boss appraît. La logique du boss est qu'il doit tirer par variable "nouveaux_tirs"

# Boss mort
Si la vie du boss mort , "groupe_tird_boss.empty()" nettoie l'écran, la fenêtre se ferme.

# Joueur mort
Si joueur mort alors la fenêtre se ferme par "self.running= false"

# Power-ups et collisions
Il y a des objets qui apparaissent de couleur orange, si le joueur en mange un il débloque une nouvelle arme qui dépend du dictionnaire "m" composer de chaîne de characters.

# tirs contre Ennemis
Ici si pas de boss , il y a des ennemis.  Pour chaque ennemi en collision avec un tir joueur, le score augmente de 10 . Les ennemis prennent 1 dégât. Le déplacement est aléatoire
# Tirs contre Boss
Si le boss entre en collision avec tirs alors il prend 1 dégât
# Tirs Boss contre Joueur
Ceci permet d'infliger les dégâts au joueur
### Joueur contre Ennemis
Ceci permet d'infliger des dégâts(1) si collision entre objet et joueur
Cela permet de aussi de faire apparaître des ennemis si boss_mode n'est pas là
### Affichage
La fonction "dessiner" permet de déposer une couleur pour le fond de la fenêtre, de dessiner les sprites , d'afficher l'HUD.
La fonction HUD est pour l'HUD soit la police et le texte afficher.

# settings.py ####
Définition de l'écran avec variabe "LARGEUR_ECRAN = 800","HAUTEUR_ECRAN = 600","FPS = 60" . Ainsi un écran de 800x600 à 60 fps. 
Dont les les couleurs sont définient par des tuples RGB allant de 0 à 255.
Le nombre d'ennemis est 3 maximum par la variable NB_ENNEMIS_MAX = 3

# testing.py ####
 Importation du système par "sys" et "os" .Import "unittest" et "pygame". Import de "Player", "Ennemi" et "HAUTEUR_ECRAN".

 Création de la classe "TestFireballeGame où une fonction "setUp" fait que le self.player =Player().

 La fonction test_controles_clavier_60 assure le fonctionnement des touches Q et D.

 La fonction test_perte_vie_et_invincibilite assure que le joueur perd la vie soit 1 par dégât. Ce qui enlève 1 à la vie du joueur.

 la fonction test_ennemi_sortie_ecran assure que pour chaque ennmi détruit le joueur gagne 10  dont le maximum atteint est 100.




# \AllDatas\Entities\entities.py ####
Ce fichier permet la création d'une classe "Entity" dont la fonction "__init__ est définie par 6 paramètres. Elle permet de donner les caractéristiques de la classe , vie , position ,l'image associé.
LA fonction "degat" est définie avec un paramètre, si la vie est égale à -1 et inférieur à 0 alors les entités de la classe meurent donc disparaisse de l'écran.

# \AllDatas\Entities\ennemi.py ####
 Le module random est importé et les fonctions d'entities et de settings sont importées.
 Un classe "Ennemi" est crée avec un paramètre Entity. On crée trois fonctions. La première __init__ avec deux paramètres "x" et "y" dont on définit une vitesse aléatoire. Puis la deuxième fonction "update" qui gère le sorti de l'ennemi qui va revenir s'il sort de l'écran. 
 Puis une troisième fonction "respawn" qui gère la réapparition de des objets.

# \AllDatas\Entities\boss.py ####
On importe pygame et depuis "entities" on importe Entity. Dans la classe Boss, avec la fonction __init__ on définit des caractéristiques comme pour le fichier "ennemi.py" , c'est pareil pour "update". Pour la fonction shoot on a un paramètre . En fonction de "current time" le boss change de comportement dans ses tirs, c'est-à-dire qu'ils seront plus à gauche ou plus à droite.

La classe "BossShoot", la fonction __init__ change les caractéristques du boss. Et la fonction "upadte  est codé pour que lorsque le boss a  pris plus de 600 de dégâts, il meurt par "self.kill()".

# \AllDatas\Entities\boss.py ####
Importation de pygame, os et "d'Entity" de "entities" et LARGEUR_ECRAN" de settings.
Dans la class Shoot, on définit de la même façon dans __init__ que pour boss.py au niveau structure.
Dans la fonction "update" on code pour la vie du joueur , si c'est inférieur à 0 alors le joueur meurt, "self.kill()".
Dans la classe "Player". On définit le jouer à une position de base sur la fenêtre.
On charge le fichier sprite par "chemin_image".
Dans le bloc try on charge l'image ,on stock l'erreur dans "e" on imprime notre erreur avec un message.
On définit les tirs tirs.
