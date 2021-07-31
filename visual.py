import pygame
import sys
from pygame.locals import *
import random
from array import *
from math import *
from tkinter import *
import keyboard

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

root = Tk()

window_width = 600
window_height = 400
point_thickness = 3
display_surf = pygame.display.set_mode((window_width, window_height))

show_noise = True
show_trail = True
# Main Function


def main():
    pygame.init()
    global display_surf
    display_surf = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption('Brownian Motional Visualizer')
    display_surf.fill(BLACK)
    create_particles()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        display_surf.fill(BLACK)
        pygame.time.wait(1)

        if keyboard.is_pressed('s'):
            global show_noise
            show_noise = not show_noise
            pygame.time.delay(100)
        if keyboard.is_pressed('t'):
            global show_trail
            show_trail = not show_trail
            pygame.time.delay(100)
            # Iterates through all the particles.
        for particle in all_particles:
            # particle.collision(all_particles)
            # Checks if this particle collides with any other particle.
            # for otherParticle in all_particles:
            #     if particle != otherParticle:
            #         particle.collision(otherParticle)
            particle.move(all_particles)

        # Resets the demo with new particles.
        if keyboard.is_pressed('r'):
            all_particles.clear()
            display_surf.fill(BLACK)
            create_particles()

        pygame.display.flip()

# Particle object class.


class Particle:
    def __init__(self, x, y, isMainParticle):
        self.x = x
        self.y = y
        self.isMainParticle = isMainParticle
        if isMainParticle:
            self.color = WHITE
            self.radius = main_particle_radius
            self.speed = 1
            self.past_path = []
        else:
            self.color = (255, 0, 0)
            self.radius = mini_particle_radius
            self.speed = 2
        self.direction = random.random()*2*pi

    # Draws the particle.
    def display(self):
        pygame.draw.circle(display_surf, self.color,
                           (self.x, self.y), self.radius, 1)
        if self.isMainParticle and show_trail:
            for point in self.past_path:
                pygame.draw.circle(display_surf, self.color, point, 1, 1)
                # Checks if this particle collides with any other particle or the wall.

    def collision(self, x_change, y_change,  all_particles):
        for Particle in all_particles:
            newX = self.x + x_change
            newY = self.y + y_change
            if self != Particle:

                # checks if the particle collides with the edges or not
                if (newX + self.radius >= window_width) or (newX - self.radius <= 0):
                    self.direction = (pi)-self.direction
                    x_change *= -1

                if newY + self.radius >= window_height or (newY - self.radius <= 0):
                    self.direction *= -1
                    y_change *= -1

                self.direction %= (pi*2)

                # Potential new center of the particle
                newX = self.x + x_change
                newY = self.y + y_change
                distance = dist((newX, newY), (Particle.x, Particle.y))
                if distance <= self.radius + Particle.radius:
                    if distance < self.radius + Particle.radius:
                        if self.isMainParticle or not Particle.isMainParticle:
                            del(Particle)
                            break
                        else:
                            del(self)
                            return
                    m1 = (pi*self.radius**2)
                    m2 = (pi*Particle.radius**2)
                    self_phi = atan2((newY - Particle.y),
                                     (Particle.x - newX))
                    v1 = self.speed
                    v2 = Particle.speed
                    theta1 = self.direction
                    theta2 = Particle.direction
                    selfspeedx = (v1*cos(theta1-self_phi)*(m1 - m2) + 2*m2*v2*cos(theta2 - self_phi)) * cos(
                        self_phi)/(m1 + m2) + v1 * sin(theta1 - self_phi)*cos(self_phi + pi/2)
                    selfspeedy = (v1*cos(theta1-self_phi)*(m1 - m2) + 2*m2*v2*cos(theta2 - self_phi)) * sin(
                        self_phi)/(m1 + m2) + v1 * sin(theta1 - self_phi)*sin(self_phi + pi/2)
                    self.speed = sqrt(selfspeedx ** 2 + selfspeedy**2)
                    self.direction = atan2(selfspeedy, selfspeedx)

                    particle_phi = (self_phi + pi) % (2*pi)
                    particlespeedx = (v2*cos(theta2-particle_phi)*(m2 - m1) + 2*m1*v1*cos(theta1 - particle_phi)) * cos(
                        particle_phi)/(m1 + m2) + v2 * sin(theta2 - particle_phi)*cos(particle_phi + pi/2)
                    particlespeedy = (v2*cos(theta2-particle_phi)*(m2 - m1) + 2*m1*v1*cos(theta1 - particle_phi)) * sin(
                        particle_phi)/(m1 + m2) + v2 * sin(theta2 - particle_phi)*sin(particle_phi + pi/2)
                    Particle.speed = sqrt(
                        particlespeedx ** 2 + particlespeedy**2)
                    Particle.direction = atan2(particlespeedy, particlespeedx)

                    x_change = cos(self.direction)*self.speed
                    y_change = -1*sin(self.direction)*self.speed
        self.x = newX
        self.y = newY
        if self.isMainParticle:
            self.past_path.append((self.x, self.y))
        if show_noise or self.isMainParticle:
            self.display()

    def move(self, all_particles):
        self.direction %= (pi*2)
        change_x = cos(self.direction)*self.speed
        change_y = -1 * sin(self.direction)*self.speed
        self.collision(change_x, change_y, all_particles)

        # bounceX = False
        # bounceY = False
        # if (change_x + self.x + self.radius >= window_width and (self.direction < pi/2 or self.direction > 3*pi/2))\
        #         or change_x + self.x - self.radius <= 0 and (self.direction > pi/2 and self.direction < 3*pi/2):
        #     self.direction = (pi)-self.direction
        #     bounceX = True

        # if change_y + self.y + self.radius >= window_height and (self.direction > pi and self.direction < 2*pi) \
        #         or (change_y + self.y - self.radius <= 0 and (self.direction < pi and self.direction > 0)):
        #     self.direction *= -1
        #     bounceY = True
        # self.direction %= (pi*2)

        # if bounceX:
        #     if bounceY:
        #         self.collision(-change_x, change_y, all_particles)
        #     else:
        #         self.collision(-change_x, -change_y, all_particles)
        # elif bounceY:
        #     self.collision(change_x, change_y, all_particles)
        # else:
        #     self.collision(change_x, -change_y, all_particles)

        # self.direction %= (pi*2)
        # change_x = cos(self.direction)*self.speed
        # change_y = sin(self.direction)*self.speed
        # bounceX = False
        # bounceY = False
        # if (change_x + self.x + self.radius >= window_width and (self.direction < pi/2 or self.direction > 3*pi/2))\
        #         or change_x + self.x - self.radius <= 0 and (self.direction > pi/2 and self.direction < 3*pi/2):
        #     self.x -= change_x
        #     self.direction = (pi)-self.direction
        #     bounceX = True
        # else:
        #     self.x += change_x

        # if change_y + self.y + self.radius >= window_height and (self.direction > pi and self.direction < 2*pi) \
        #         or (change_y + self.y - self.radius <= 0 and (self.direction < pi and self.direction > 0)):
        #     self.y += change_y
        #     self.direction *= -1
        #     bounceY = True
        # else:
        #     self.y -= change_y
        # self.direction %= (pi*2)


# Stores the displayed particles.
all_particles = []
num_main_particles = 0
main_particle_radius = 30

num_other_particles = 150
mini_particle_radius = 5
# Generates the particles with random size, speed, and starting positions and adds them to the list of particles.


def create_particles():
    for n in range(num_main_particles):
        x = random.randint(main_particle_radius,
                           window_width-main_particle_radius)
        y = random.randint(main_particle_radius,
                           window_height-main_particle_radius)
        for particle in all_particles:
            if dist((x, y), (particle.x, particle.y)) <= particle.radius + mini_particle_radius:
                x = random.randint(main_particle_radius,
                                   window_width-main_particle_radius)
                y = random.randint(main_particle_radius,
                                   window_height-main_particle_radius)
        all_particles.append(Particle(x, y, True))
    for n in range(num_other_particles):
        x = random.randint(mini_particle_radius,
                           window_width-mini_particle_radius)
        y = random.randint(mini_particle_radius,
                           window_height-mini_particle_radius)
        for particle in all_particles:
            if dist((x, y), (particle.x, particle.y)) <= particle.radius + mini_particle_radius:
                x = random.randint(mini_particle_radius,
                                   window_width-mini_particle_radius)
                y = random.randint(mini_particle_radius,
                                   window_height-mini_particle_radius)
        all_particles.append(Particle(x, y, False))


if __name__ == '__main__':
    main()
