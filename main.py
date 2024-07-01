from kivy.app import App
from kivy.graphics import Color
from kivy.uix.widget import Widget
from kivy.config import Config
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.properties import (
    NumericProperty, ReferenceListProperty, ObjectProperty
)
from kivy.vector import Vector
from kivy.clock import Clock
import time


class PongTableLineTop(Widget):
    pass


class PongTableLineLeft(Widget):
    pass


class PongTableLineCenter(Widget):
    pass


class PongTableLineRight(Widget):
    pass


class PongTableLineBottom(Widget):
    pass


class PongTableNet(Widget):
    pass


class PongTable(Widget):
    pass


class PongPaddleLeft(Widget):
    score = NumericProperty(0)

    def bounce_ball(self, ball):
        if self.collide_widget(ball):
            vx, vy = ball.velocity
            offset = (ball.center_y - self.center_y) / (self.height / 2)
            bounced = Vector(-1 * vx, vy)
            vel = bounced * 1.1
            ball.velocity = vel.x, vel.y + offset


class PongPaddleRight(Widget):
    score = NumericProperty(0)

    def bounce_ball(self, ball):
        if self.collide_widget(ball):
            vx, vy = ball.velocity
            offset = (ball.center_y - self.center_y) / (self.height / 2)
            bounced = Vector(-1 * vx, vy)
            vel = bounced * 1
            ball.velocity = vel.x, vel.y + offset


class PongBall(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos


class PongGame(Widget):
    ball = ObjectProperty(None)
    player1 = ObjectProperty(None)
    player2 = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(PongGame, self).__init__(**kwargs)
        self.countdown()

    def countdown(self):
        self.start.text = "3"

        if self.player1.score == 10:
            self.result.text = "Wygrywa gracz 1"
        elif self.player2.score == 10:
            self.result.text = "Wygrywa gracz 2"
        else:
            self.result.text = ""
        Clock.schedule_once(self.update_timer, 1)

    def update_timer(self, dt):
        current_value = int(self.start.text)
        if current_value > 1:
            self.start.text = str(current_value - 1)
            Clock.schedule_once(self.update_timer, 1)
        else:
            self.start.text = ""
            self.serve_ball()

    def serve_ball(self, vel=(8, 0)):
        self.result.text = ""
        self.ball.center = self.center
        self.ball.velocity = vel
        self.player1.center_y = self.width / 3.5
        self.player2.center_y = self.width / 3.5
        self.ti1.focus = True

    def update(self, dt):
        self.ball.move()

        # bounce off paddles
        self.player1.bounce_ball(self.ball)
        self.player2.bounce_ball(self.ball)

        # bounce ball off bottom or top
        if (self.ball.y < self.y) or (self.ball.top > self.top):
            self.ball.velocity_y *= -1

        if self.player1.score == 11:
            self.countdown()
            self.player1.score = 0
            self.player2.score = 0
        elif self.player2.score == 11:
            self.countdown()
            self.player1.score = 0
            self.player2.score = 0
        else:
            if self.ball.x < self.x:
                self.player2.score += 1
                self.serve_ball(vel=(8, 0))
            if self.ball.right > self.width:
                self.player1.score += 1
                self.serve_ball(vel=(-8, 0))

    def on_touch_move(self, touch):
        if touch.x < self.width / 3:
            self.player1.center_y = touch.y
        if touch.x > self.width - self.width / 3:
            self.player2.center_y = touch.y

    def keyBoardEvents(self, dt):
        if self.ti1.text == 'w':
            self.player1.center_y += 65
            self.ti1.text = ''

        if self.ti1.text == 's':
            self.player1.center_y -= 65
            self.ti1.text = ''

        if self.ti1.text == 'o':
            self.player2.center_y += 65
            self.ti1.text = ''

        if self.ti1.text == 'l':
            self.player2.center_y -= 65
            self.ti1.text = ''

        if self.ball.x < (self.player1.x + self.player1.width + 25) and self.ti1.text == 'e':
            self.ball.velocity[0] *= 1.2
            self.ti1.text = ''

        if self.ball.x < (self.player2.x + self.player2.width + 25) and self.ti1.text == 'p':
            self.ball.velocity[0] *= 1.2
            self.ti1.text = ''

        else:
            self.ti1.text = ''

        if (self.player1.y < self.y):
            self.player1.y = self.y
        elif (self.player1.top > self.top):
            self.player1.y = self.top - 60

        if (self.player2.y < self.y):
            self.player2.y = self.y
        elif (self.player2.top > self.top):
            self.player2.y = self.top - 60


class PongApp(App):
    def build(self):
        Window.size = (1280, 720)
        Window.clearcolor = (237 / 255, 61 / 255, 31 / 255)
        game = PongGame()
        Clock.schedule_interval(game.update, 1.0 / 60.0)
        Clock.schedule_interval(game.keyBoardEvents, 1.0 / 60.0)
        return game


if __name__ == '__main__':
    PongApp().run()
