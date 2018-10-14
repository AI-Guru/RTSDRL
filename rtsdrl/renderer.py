import pygame


class EnvironmentRenderer:

    def render(self, environment):
        assert isinstance(environment, Environment)


class PyGameRenderer(EnvironmentRenderer):

    def __init__(self):
        width, height = 600, 600
        self.screen = pygame.display.set_mode((width, height))

        pygame.font.init()
        self.myfont = pygame.font.SysFont('Comic Sans MS', 30)


    def render(self, environment):
        for event in pygame.event.get():
            pass

        background_colour = (0, 0, 0)
        self.screen.fill(background_colour)

        for entity in environment.entities:
            x = int(entity.x)
            y = int(entity.y)
            width = 30

            self.render_polygon(entity.polygon, entity.color)

            if hasattr(entity, "visibility_fan_polygons"):
                for polygon, color in zip(entity.visibility_fan_polygons, entity.visibility_fan_colors):
                    self.render_polygon(polygon, color)

            if hasattr(entity, "reward"):
                text = "{}".format(entity.reward)
                textsurface = self.myfont.render(text, False, (255, 255, 255))
                self.screen.blit(textsurface, (entity.x, entity.y))

        pygame.display.flip()


    def render_polygon(self, polygon, color):
        x, y = polygon.exterior.coords.xy
        outline = list(zip(x, y))
        pygame.draw.polygon(self.screen, color, outline, 1)


    def finish(self):
        pygame.display.quit()
        pygame.quit()
