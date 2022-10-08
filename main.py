import pygame
import random
pygame.init()

# <>
clock = pygame.time.Clock()
bg = pygame.image.load('imgs/BKG.png')

dWidth = bg.get_width() - 20
dHeight = bg.get_height() - 20
win = pygame.display.set_mode((dWidth, dHeight))
pygame.display.set_caption('Finestra')

globalCooldown = 0
evilGlobalCooldown = 0


class player():

    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.health = 3
        self.upgrade = 1
        self.vel = 2

        self.img = pygame.image.load('imgs/naveF.png')
        self.imgSx = pygame.image.load('imgs/naveSx.png')
        self.imgDx = pygame.image.load('imgs/naveDx.png')

        self.width = self.img.get_width()
        self.height = self.img.get_height()

        self.hitbox = self.x, self.y, self.width, self.height
        self.left = False
        self.right = False

    def draw(self, win):

        if self.left:
            win.blit(self.imgSx, (self.x, self.y))
        elif self.right:
            win.blit(self.imgDx, (self.x, self.y))
        else:
            win.blit(self.img, (self.x, self.y))

        self.hitbox = self.x, self.y, self.width, self.height

        for x in range(1, self.health+1):
            win.blit(pygame.image.load('imgs/cuore.png'),
                     (dWidth - 100 + (13 * x), dHeight - 30))
#        pygame.draw.rect(win, (255,0,0), self.hitbox, 2)

    def hit(self):
        global score
        score -= 5
        self.health -= 1


class projectile():
    def __init__(self, x, y, w, h, color, evil=False):
        self.x = x
        self.y = y

        self.width = w
        self.height = h
        self.visibile = True
        self.color = color

        self.evil = evil
        self.dir = -1 if not self.evil else 1
        self.vel = 2 if not self.evil else 1

    def draw(self, win):
        self.move()
        pygame.draw.rect(
            win, self.color, (self.x, self.y, self.width, self.height))
        if self.y < 0 or self.y > dHeight:
            self.visibile = False

    def move(self):
        self.y += self.vel * self.dir


class enemy():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.big = random.choice([True, False])
        self.vel = 1
        self.animation = random.choice([1, 2])

        if not self.big:
            self.health = 10
            self.img1 = pygame.image.load('imgs/ES1.png')
            self.img2 = pygame.image.load('imgs/ES2.png')
        else:
            self.health = 20
            self.img1 = pygame.image.load('imgs/EB1.png')
            self.img2 = pygame.image.load('imgs/EB2.png')

        self.width = self.img1.get_width()
        self.height = self.img1.get_height()
        self.max = dWidth - self.img1.get_width() - 20
        self.min = 0 + 20
        self.verso = random.choice([1, -1])

        self.hitbox = self.x, self.y, self.width, self.height

    def draw(self, win):
        global globalCooldown

        self.move()

        if globalCooldown == 0:
            self.cambiaAnimazione()

        if self.animation == 1:
            win.blit(self.img1, (self.x, self.y))
        else:
            win.blit(self.img2, (self.x, self.y))

        self.hitbox = self.x, self.y, self.width, self.height
#            pygame.draw.rect(win,(255,0,0), self.hitbox, 1)

    def cambiaAnimazione(self):
        if self.animation == 1:
            self.animation = 2
        else:
            self.animation = 1

    def move(self):
        if self.x >= self.max:
            self.verso = -1

        if self.x <= self.min:
            self.verso = 1

        self.x += (self.vel * self.verso)
        pass

    def hit(self):
        global score
        self.health -= 1
        score += 1

    def shoot(self, win):
        pygame.draw.rect(win, (255, 0, 0), (self.x +
                         self.width - 3, self.y + self.height, 6, 6))
        Ebullets.append(projectile(self.x + self.width//2 - 3,
                        self.y + self.height + 3, 6, 6, (255, 0, 0), True))


def redrawWindow():
    global enemyProjectiles
    win.blit(bg, (0, 0))

    if not(perso or vinto):

        win.blit(punteggio, (10, dHeight - 20))
        pg.draw(win)

        if not spawnPowerUp or PowerUpSpawned:
            if PowerUp.visibile:
                PowerUp.draw(win)

        for enemy in enemies:
            enemy.draw(win)

        for bullet in Abullets:
            bullet.draw(win)
            if not bullet.visibile:
                Abullets.pop(Abullets.index(bullet))
                enemyProjectiles -= 1

        for bullet in Ebullets:
            bullet.draw(win)
            if not bullet.visibile:
                Ebullets.pop(Ebullets.index(bullet))
                enemyProjectiles -= 1

    elif perso:
        fontPerso = pygame.font.SysFont('comicsans', 30, True)
        textPerso = fontPerso.render('Hai perso!', 1, (255, 255, 255))
        win.blit(textPerso, (dWidth//2 - textPerso.get_width()//2, dHeight//2))

    elif vinto:
        fontVinto = pygame.font.SysFont('comicsans', 30, True)
        textVinto = fontVinto.render('Hai vinto!', 1, (255, 255, 255))
        win.blit(textVinto, (dWidth//2 - textVinto.get_width()//2, dHeight//2))
        punteggioF = pygame.font.SysFont('comicsans', 20, True).render(
            "Punteggio: " + str(score), 1, (255, 255, 255))
        win.blit(punteggioF, (dWidth//2 - punteggioF.get_width() //
                 2, dHeight//2 + textVinto.get_height()))

    pygame.display.update()


def generaNemici():
    for i in range(15):
        enemies.append(enemy(random.randint(0, dWidth),
                       random.randint(0, dHeight//2)))


Abullets = []
Ebullets = []
enemies = []
enemyProjectiles = 0
score = 0
vinto = False
perso = False
inizio = True
PowerUp = projectile(random.randint(10, dWidth-6 - 10),
                     10, 6, 6, (255, 255, 0), True)
spawnPowerUp = 1
spawnPowerUpContatore = 0
PowerUpSpawned = False

pg = player(dWidth//2 - 32, dHeight//2 + 140)
run = True
while run:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # contatore power up
    if spawnPowerUp >= 0 and not PowerUpSpawned:
        spawnPowerUp += 1
    if spawnPowerUp == 1000:
        PowerUp = projectile(random.randint(
            10, dWidth-6 - 10), 10, 6, 6, (255, 255, 0), True)
        PowerUpSpawned = True
        spawnPowerUp = 0

    # contatore proiettili
    if globalCooldown > 0:
        globalCooldown += 1
        if globalCooldown % 2 == 0:
            evilGlobalCooldown += 1
    if globalCooldown == 10:
        globalCooldown = 0
        evilGlobalCooldown = 0

    if not(perso or vinto):
        # collisione Abullets con nemici
        for bullet in Abullets:
            for nemico in enemies:
                if bullet.y >= nemico.y and bullet.y + bullet.height < nemico.y + nemico.height:
                    if bullet.x > nemico.x and bullet.x + bullet.width < nemico.x + nemico.width:
                        nemico.hit()
                        win.blit(pygame.font.SysFont('comicsans', 10, True).render(
                            "-5", 1, (255, 0, 0)), (dWidth//2, dHeight//2))
                        if nemico.health == 0:
                            enemies.pop(enemies.index(nemico))
                        try:
                            Abullets.pop(Abullets.index(bullet))
                        except:
                            pass

        # collisione Ebullets con nave
        for bullet in Ebullets:
            if bullet.y >= pg.y and bullet.y + bullet.height < pg.y + pg.height:
                if bullet.x > pg.x and bullet.x + bullet.width < pg.x + pg.width:
                    bullet.visibile = False
                    pg.hit()

        if PowerUp.y >= pg.y and PowerUp.y + PowerUp.height < pg.y + pg.height:
            if PowerUp.x > pg.x and PowerUp.x + PowerUp.width < pg.x + pg.width:
                pg.upgrade = 2
                pg.vel = 3
                PowerUp.visibile = False

    # fai sparare i nemici a caso
    if not(perso or vinto):
        try:
            if enemyProjectiles < 10 and evilGlobalCooldown == 0:
                tizioRandom = random.randint(0, len(enemies)-1)
                enemies[tizioRandom].shoot(win)
                enemyProjectiles += 1
        except:
            pass

    # movimenti
    keys = pygame.key.get_pressed()
#    mb =  pygame.mouse.get_pos()
#
#    pg.x = mb[0]
#    pg.y = mb[1]
    if keys[pygame.K_ESCAPE]:
        run = False

    pg.right = False
    pg.left = False
    if (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and pg.x + pg.width + pg.vel < dWidth:
        pg.x += pg.vel
        pg.right = True
        pg.left = False
#            globalCooldown = 1

    if (keys[pygame.K_a] or keys[pygame.K_LEFT]) and pg.x > 0:
        pg.x -= pg.vel
        pg.left = True
        pg.right = False
#            globalCooldown = 1

    if keys[pygame.K_n]:
        pg.upgrade += 1

    # spara
    if globalCooldown == 0:
        if keys[pygame.K_SPACE]:

            if pg.upgrade == 1:
                Abullets.append(projectile(pg.x + pg.width //
                                2 - 3, pg.y - 3, 6, 6, (0, 255, 127)))
            else:
                Abullets.append(projectile(pg.x + pg.width //
                                4 - 3, pg.y - 3, 6, 6, (0, 255, 127)))
                Abullets.append(projectile(pg.x + 3*pg.width //
                                4 - 3, pg.y - 3, 6, 6, (0, 255, 127)))

        globalCooldown = 1

        for nemico in enemies:
            nemico.cambiaAnimazione()

    if PowerUp.y > dHeight:
        PowerUpSpawned = False
        spawnPowerUp = 1
        del PowerUp
        PowerUp = projectile(random.randint(
            10, dWidth-6 - 10), 10, 6, 6, (255, 255, 0), True)

    if PowerUpSpawned:
        spawnPowerUpContatore += 1
        if spawnPowerUpContatore == 700:
            pg.upgrade = 1
            PowerUpSpawned = False
            spawnPowerUp = 1
            pg.vel = 2
            del PowerUp
            PowerUp = projectile(random.randint(
                10, dWidth-6 - 10), 10, 6, 6, (255, 255, 0), True)
            spawnPowerUpContatore = 0
    punteggio = pygame.font.SysFont('comicsans', 20, True).render(
        "Punteggio: " + str(score), 1, (255, 255, 255))

    if pg.health == 0:
        perso = True

    if enemies == [] and inizio:
        generaNemici()
        inizio = False

    elif enemies == []:
        vinto = True

    redrawWindow()

pygame.quit()
