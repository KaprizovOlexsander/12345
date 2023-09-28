from pygame import *
import random
init()


window = display.set_mode((1000, 700))
clock = time.Clock()


game = True


bag = image.load('res/kosmos.jpg')
bag = transform.scale(bag, (window.get_width(), window.get_height()))

def draw_bag():
    window.blit(bag, (0, 0))

class Sprite(sprite.Sprite):
    # init - функція конструктор (вона створює екземпляри класу)
    def __init__(self, filename, x, y, width=50, height=50, speed=0):

        super().__init__()

        # завантажити текстуру картинки і змінити її розмір
        self.image = transform.scale(image.load(filename), (width, height))
        self.rect = self.image.get_rect()  # get_rect - створює хітбокс розміру картинки
        # задаю кординати хітбоксу
        self.rect.x, self.rect.y = x, y  # одночасне присвоювання
        # self.rect.x = x
        # self.rect.y = y те ж саме, але одним рядком
        self.speed = speed


    def draw(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class UFO(Sprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > window.get_height():
            self.kill()


class Bullet(Sprite):
    def update(self):
        self.rect.y -= self.speed


def label(text, size, label_font, color, x, y):
    # Створити шрифт
    new_font = font.SysFont(label_font, size)
    # На основі шрифта створити текст
    text = new_font.render(text, True, color)
    # намалювати текст
    window.blit(text, (x, y))



class Player(Sprite):

    def update(self):
        pressed_keys = key.get_pressed()
        if pressed_keys[K_a]:
            self.rect.x -= self.speed
        if pressed_keys[K_d]:
            self.rect.x += self.speed
        if pressed_keys[K_s]:
            self.rect.y += self.speed
        if pressed_keys[K_w]:
            self.rect.y -= self.speed


rocket = Player('res/raketa.png', 500, 500, height=120, width=100, speed=7)


bullets = sprite.Group()
ufos = sprite.Group()
game_score = 0


run = True
lifes = 3
while game:
    if run == True:
        if lifes < 1:
            run = False


        while len(ufos) < 7:
            new_ufo = UFO('res/ufosprite.png', random.randint(0, window.get_width() - 100), -100, 100, 50, 1)
            ufos.add(new_ufo)


        for e in event.get():
            if e.type == QUIT:
                game = False


            if e.type == KEYDOWN:
                if e.key == K_SPACE:
                    bullets.add(
                        Bullet('res/bullet.png', rocket.rect.x, rocket.rect.y, 10, 30, 5)
                    )


        ufos.update()
        bullets.update()
        rocket.update()


        interaction = sprite.groupcollide(bullets, ufos, True, True)
        for bullet in interaction:
            game_score += len(interaction[bullet])


        inter1 = sprite.spritecollide(rocket, ufos, True)
        if len(inter1) > 0:
            lifes -= 1
        draw_bag()
        ufos.draw(window)
        bullets.draw(window)
        rocket.draw()


        label('Рахунок: ' + str(game_score), 40, 'Montserrat', (255, 255, 255), 800, 630)
        label('Життя: ' + str(lifes), 40, 'Montserrat', (255, 255, 255), 50, 630)

    else:
        for e in event.get():
            if e.type == QUIT:
                game = False
        label('Поразка', 50, 'Algerian', (255, 0, 0), 420, 300)


    display.update()
    clock.tick(60)