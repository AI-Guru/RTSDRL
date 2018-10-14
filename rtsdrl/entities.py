import math
import numpy as np
from shapely.geometry import Polygon
from .mathcore import *

class Entity:

    def __init__(self, x, y, name):
        self.x = x
        self.y = y
        self.angle = 0.0
        self.width = 10
        self.name = name
        self.update_geometry()


    def update_geometry(self):
        segments = 20
        points = []
        for i in range(segments):
            angle = math.radians(self.angle + 360.0 * i / segments)
            x = self.x + self.width * math.sin(angle)
            y = self.y + self.width * math.cos(angle)
            points.append((x, y))
        self.polygon = Polygon(points)

        #x, y = self.polygon.exterior.coords.xy
        #self.outline = list(zip(x, y))

    def perform_action(self, action):
        pass


class Harvester(Entity):

    def perform_action(self, action):
        if action == "turn_left":
            self.angle += 10
        elif action == "turn_right":
            self.angle -= 10
        elif action == "move_forward":
            vector = vector_from_angle_and_length(math.radians(self.angle), 10)
            self.x += vector[0]
            self.y += vector[1]
        elif action == "move_backward":
            vector = vector_from_angle_and_length(math.radians(self.angle), -10)
            self.x += vector[0]
            self.y += vector[1]
        else:
            print("Unknown action", action)

        while self.angle >= 360.0:
            self.angle -= 360.0
        while self.angle < 0.0:
            self.angle += 360.0

        self.update_geometry()
        self.perceive()


    def update_geometry(self):
        super().update_geometry()

        self.reward = -100.0

        self.color = (250, 50, 25)

        # Computing the visibility fan.
        angle_span = 90
        angle_segments = 20
        vis_range_min = 10
        vis_range_max = 100
        self.visibility_fan_polygons = []
        self.visibility_fan_colors = []
        self.visibility_fan_distances = []
        center = np.array([self.x, self.y])
        for angle_segment in range(angle_segments):
            angle1 = self.angle + angle_span * angle_segment / angle_segments - angle_span / 2
            angle2 = angle1 + angle_span / angle_segments

            angle1 = math.radians(angle1)
            angle2 = math.radians(angle2)

            vector1 = vector_from_angle_and_length(angle1, vis_range_min) + center
            vector2 = vector_from_angle_and_length(angle1, vis_range_max) + center
            vector3 = vector_from_angle_and_length(angle2, vis_range_max) + center
            vector4 = vector_from_angle_and_length(angle2, vis_range_min) + center

            polygon = Polygon([vector1, vector2, vector3, vector4])
            self.visibility_fan_polygons.append(polygon)
            self.visibility_fan_colors.append((0, 0, 255))
            self.visibility_fan_distances.append(1000000.0)


    def perceive(self):
        for entity in self.environment.entities:
            if entity != self:
                for index, fan_polygon in enumerate(self.visibility_fan_polygons):
                    if fan_polygon.intersects(entity.polygon):
                        distance = get_distance(self.x, self.y, entity.x, entity.y)
                        if distance < self.visibility_fan_distances[index]:
                            self.visibility_fan_colors[index] = entity.color
                            self.visibility_fan_distances[index] = distance

                        if isinstance(entity, Resource) and distance < 10:
                            print("Alarm!")



class Obstacle(Entity):
    pass


class Resource(Entity):

    def update_geometry(self):
        super().update_geometry()

        self.color = (25, 255, 50)
