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

window_width = 700
window_height = 500
point_thickness = 3

# Determines what stuff to display
show_noise = True
show_trail = True

# Stores the particles.
all_particles = []

# Number and radius of the larger particles with the trails
num_main_particles = 3
main_particle_radius = 30

# Number and radius of the smaller filler particles
num_other_particles = 150
mini_particle_radius = 10


# Main Function
def main():
    pygame.init()
    global display_surf, display2
    display_surf = pygame.display.set_mode((window_width, window_height))
    display2 = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption('Brownian Motional Visualizer')
    display_surf.fill(BLACK)
    create_particles(num_main_particles, num_other_particles)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        display_surf.fill(BLACK)

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
            temp = len(all_particles)
            particle.move(all_particles)
            if temp != len(all_particles):
                print(temp, len(all_particles))

        # Resets the demo with new particles.
        if keyboard.is_pressed('r'):
            all_particles.clear()
            display_surf.fill(BLACK)
            create_particles(num_main_particles, num_other_particles)

        pygame.display.flip()


# Particle object class

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
            self.speed = 3
        self.direction = random.random()*2*pi

    # Draws the particle and trail if applicable
    def display(self):
        pygame.draw.circle(display_surf, self.color,
                           (self.x, self.y), self.radius, 1)
        if self.isMainParticle and show_trail:
            for point in self.past_path:
                pygame.draw.circle(display_surf, self.color, point, 1, 1)
                # Checks if this particle collides with any other particle or the wall.

    def move(self, all_particles):
        self.direction %= (pi*2)
        change_x = cos(self.direction)*self.speed
        change_y = -1 * sin(self.direction)*self.speed
        self.collision(change_x, change_y, all_particles)

    def collision(self, x_change, y_change,  all_particles):
        # checks if the particle collides with the edges or not
        newX = self.x + x_change
        newY = self.y + y_change
        if (newX + self.radius >= window_width) or (newX - self.radius <= 0):
            self.direction = (pi)-self.direction
            x_change *= -1

        if newY + self.radius >= window_height or (newY - self.radius <= 0):
            self.direction *= -1
            y_change *= -1

        # For all other particles, check if the next position of this particle will
        # collide with the other particle or the wall. If so, change direction and continue
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

                    # If they coincide or overlap enough, delete one and recreate it elsewhere
                    if distance < max(self.radius, Particle.radius):
                        if self.isMainParticle or not Particle.isMainParticle:
                            all_particles.remove(Particle)
                            create_particles(0, 1)
                            break
                        else:
                            all_particles.remove(self)
                            create_particles(0, 1)
                            return

                    # Change the direction of this particle and the collided particle using the Elastic
                    # colission equations https://williamecraver.wixsite.com/elastic-equations
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

                    # Find new future corrdinate
                    x_change = cos(self.direction)*self.speed
                    y_change = -1*sin(self.direction)*self.speed

        self.x = newX
        self.y = newY

        # Display
        if self.isMainParticle:
            self.past_path.append((self.x, self.y))
        if show_noise or self.isMainParticle:
            self.display()


# Generates the number of main (big) particles and other (smaller) particles at a random (x,y) coordinate such that they dont overlap
def create_particles(num_main, num_other):
    for n in range(num_main):
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
    for n in range(num_other):
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
