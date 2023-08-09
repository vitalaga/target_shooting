class GameStats:
    """Stats tracking for Plant Shooter game"""

    def __init__(self, ai_game):
        """Initializes statistics"""
        self.settings = ai_game.settings
        self.reset_stats()

        self.game_active = False

    def reset_stats(self):
        """Initializes statistics that change during the game"""
        self.hero_left = self.settings.hero_limit