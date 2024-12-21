import pygame

#can't remove back_ground color
class button:
    def __init__(self, x, y, img, scale):
        width1 = img.get_width()
        height1 = img.get_height()
        self.img = pygame.transform.scale(img, (int(width1 * scale), int(height1 * scale)))
        self.rect = self.img.get_rect()
        self.rect.topleft = (x, y)
        self.click = False

    def draw(self, surface):
        action = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] and self.click == False:
                self.click = True
                action = True

        if not pygame.mouse.get_pressed()[0]:
            self.click = False
        surface.blit(self.img, (self.rect.x, self.rect.y))
        return action

#can remove back_ground color
class button_v2:
    def __init__(self, x, y, width, height, image, color):

        self.x = x
        self.y = y
        self.screen = pygame.Surface((width, height))
        self.image = pygame.transform.scale(image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.screen.fill("white")
        self.screen.blit(self.image, (0, 0))
        self.screen.set_colorkey(color)
        self.click = False

    def draw(self, surface):
        action = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] and self.click == False:
                self.click = True
                action = True
            if not pygame.mouse.get_pressed()[0]:
                self.click = False
        surface.blit(self.screen, (self.rect.x, self.rect.y))
        return action
