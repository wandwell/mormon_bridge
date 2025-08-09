import pygame.mixer

#contains the sounds for the animations
class SoundManager:
    def __init__(self):
        self.sounds = {
            "shuffle": pygame.mixer.Sound("sounds/shuffle.wav"),
            "deal": pygame.mixer.Sound("sounds/deal.wav"),
            "correct": pygame.mixer.Sound("sounds/correct.wav"),
            "wrong": pygame.mixer.Sound("sounds/wrong.wav"),
            "end": pygame.mixer.Sound("sounds/end.wav"),
        }

        self.channels = {
            name: pygame.mixer.Channel(i)
            for i, name in enumerate(self.sounds)
        }

    #plays the sound
    def play(self, name):
        if name in self.sounds:
            self.channels[name].play(self.sounds[name])

    #stops the sound
    def stop(self, name):
        if name in self.channels:
            self.channels[name].stop()
