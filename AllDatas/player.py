class Player:
    def __init__(self, name, x, y):
        # Informations de base
        self.name = name
        self.hp = 100

        # Position sur l'écran
        self.x = x
        self.y = y

    def move(self, dx, dy):
        """Déplace le joueur de dx et dy"""
        self.x += dx
        self.y += dy

    def show_status(self):
        """Affiche l'état du joueur pour le debug"""
        print(f"Joueur: {self.name}  HP: {self.hp}  Position: ({self.x}, {self.y})")