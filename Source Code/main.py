from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty, StringProperty
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.core.audio import SoundLoader

ball_hit_sound = SoundLoader.load('Sounds/ball_hit.ogg')
point_sound = SoundLoader.load('Sounds/point.ogg')
victory_music = SoundLoader.load('Sounds/victory.ogg')
bg_music = SoundLoader.load('Sounds/bg.ogg')
bg_music.loop = True

class PongPaddle(Widget):
    score = NumericProperty(0)
    def bounce_ball(self, ball):
        if self.collide_widget(ball):
            vx, vy = ball.velocity
            offset = (ball.center_y - self.center_y) / (self.height / 2)
            bounced = Vector(-1 * vx, vy)
            vel = bounced * 1.1 if abs(bounced.x) < 30 else bounced
            ball.velocity = vel[0], vel[1] + offset
            ball_hit_sound.play()


class PongBall(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos


class PongGame(Widget):
    bg_music.play()
    ball = ObjectProperty(None)
    player1 = ObjectProperty(None)
    player2 = ObjectProperty(None)
    continue_text = ObjectProperty(None)
    message = StringProperty("Score 10 Points to Win")
    game_over = False
    def serve_ball(self, vel=(4, 0)):
        self.ball.center = self.center
        self.ball.velocity = vel

    def update(self, delta_time):
        if not self.game_over:
            self.ball.move()

        # bounce off paddles
        self.player1.bounce_ball(self.ball)
        self.player2.bounce_ball(self.ball)

        # bounce ball off bottom or top
        if (self.ball.y < self.y) or (self.ball.top > self.top):
            self.ball.velocity_y *= -1

        # went of to a side to score point?
        if self.ball.x + self.ball.width < self.x:
            self.player2.score += 1
            self.serve_ball(vel=(4, 0))
            point_sound.play() if self.player2.score <= 9 else victory_music.play()
        if self.ball.x > self.width:
            self.player1.score += 1
            self.serve_ball(vel=(-4, 0))
            point_sound.play() if self.player1.score <= 9 else victory_music.play()

        if self.player1.score == 10:
            self.message = "Black Player Won!"
            self.continue_text.color = (1, 1, 0, 1)
            self.game_over = True
            bg_music.stop()
        if self.player2.score == 10:
            self.message = "Red Player Won!"
            self.continue_text.color = (1, 1, 0, 1)
            self.game_over = True
            bg_music.stop()

    def on_touch_move(self, touch):
        if touch.x < self.width / 2:
            self.player1.center_y = touch.y
        if touch.x > self.width - self.width / 2:
            self.player2.center_y = touch.y
 
    def on_touch_down(self, touch):
        if self.game_over:
            self.continue_text.color = (1, 1, 0, 0)
            self.message = "Score 10 Points to Win"
            self.player1.score = 0
            self.player1.center_y = self.center_y
            self.player2.score = 0
            self.player2.center_y = self.center_y
            victory_music.stop()
            bg_music.play()
            self.game_over = False


class PongApp(App):
    def build(self):
        game = PongGame()
        game.serve_ball()
        Clock.schedule_interval(game.update, 1.0 / 60.0)
        return game


if __name__ == '__main__':
    PongApp().run()
