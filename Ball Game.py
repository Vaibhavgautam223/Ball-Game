from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.properties import NumericProperty
from kivy.core.window import Window
from kivy.graphics import Rectangle
import random

Window.size = (360, 640)

class GameWidget(Widget):
    score = NumericProperty(0)

    def __init__(self, **kwargs):
        super(GameWidget, self).__init__(**kwargs)
        self.ball = Widget(size=(50, 50), pos=(random.randint(0, 310), 600))
        self.paddle = Widget(size=(100, 20), pos=(130, 50))

        with self.canvas:
            self.ball_rect = Rectangle(size=self.ball.size, pos=self.ball.pos)
            self.paddle_rect = Rectangle(size=self.paddle.size, pos=self.paddle.pos)

        self.score_label = Label(text="Score: 0", pos=(0, 600), size_hint=(None, None))
        self.add_widget(self.score_label)

        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

        Clock.schedule_interval(self.update, 1/60.)

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == 'left':
            self.paddle.x = max(self.paddle.x - 20, 0)
        elif keycode[1] == 'right':
            self.paddle.x = min(self.paddle.x + 20, Window.width - self.paddle.width)
        return True

    def update(self, dt):
        # Move ball down
        self.ball.y -= 5

        # Update graphics
        self.ball_rect.pos = self.ball.pos
        self.paddle_rect.pos = self.paddle.pos

        # Catch check
        if self.ball.y <= self.paddle.top and self.paddle.x < self.ball.center_x < self.paddle.right:
            self.score += 1
            self.score_label.text = f"Score: {self.score}"
            self.ball.pos = (random.randint(0, 310), 600)

        # Missed ball
        if self.ball.y <= 0:
            self.ball.pos = (random.randint(0, 310), 600)

class GameApp(App):
    def build(self):
        return GameWidget()

GameApp().run()
