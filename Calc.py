from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.graphics import Color, Ellipse


class CustomButton(Button):
    def __init__(self, is_operator=False, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_down = ''    
        self.background_color = (0, 0, 0, 0)  # transparente

        # 🎨 Paleta moderna (dark + azul marino)
        if not is_operator:
            self.normal_color = (0.18, 0.18, 0.18, 1)   # gris oscuro
            self.hover_color = (0.28, 0.28, 0.28, 1)   # gris más claro
            self.pressed_color = (0.1, 0.1, 0.1, 1)    # casi negro
        else:
            self.normal_color = (0.12, 0.22, 0.45, 1)  # azul marino
            self.hover_color = (0.23, 0.42, 0.85, 1)   # azul brillante
            self.pressed_color = (0.08, 0.18, 0.35, 1) # azul oscuro

        self.current_color = self.normal_color

        # Texto
        self.color = (1, 1, 1, 1) if not is_operator else (1, 1, 1, 1)
        self.font_size = 26

        with self.canvas.before:
            self.color_instruction = Color(*self.current_color)
            self.circle = Ellipse(pos=self.pos, size=self.size)

        self.bind(pos=self.update_button, size=self.update_button)
        Window.bind(mouse_pos=self.on_mouse_pos)

    def update_button(self, *args):
        """ Mantener el botón circular """
        size = min(self.width, self.height)
        self.circle.pos = (self.center_x - size / 2, self.center_y - size / 2)
        self.circle.size = (size, size)

    def on_mouse_pos(self, window, pos):
        """ Hover efecto """
        if self.get_root_window():
            inside = self.collide_point(*self.to_widget(*pos))
            if inside:
                self.set_color(self.hover_color)
            else:
                self.set_color(self.normal_color)

    def on_press(self):
        self.set_color(self.pressed_color)

    def on_release(self):
        self.set_color(self.hover_color)

    def set_color(self, rgba):
        self.current_color = rgba
        self.color_instruction.rgba = rgba


class CalculadoraApp(App):
    def build(self):
        self.title = "Calculadora"
        Window.size = (800, 600)
        Window.clearcolor = (0.08, 0.08, 0.08, 1)  # fondo global oscuro
        self.last_was_operator = None
        self.last_was_equal = False

        main_ventana = BoxLayout(orientation="vertical", padding=20, spacing=15)

        # Display
        display_ventana = BoxLayout(size_hint_y=0.25, padding=5)
        main_ventana.add_widget(display_ventana)

        self.entrada = TextInput(
            font_size=50,
            readonly=True,
            halign="right",
            multiline=False,
            background_color=(0.15, 0.15, 0.15, 1),
            foreground_color=(1, 1, 1, 1),
            cursor_color=(1, 1, 1, 1),
            padding=(25, 25),
        )
        display_ventana.add_widget(self.entrada)

        # Botones
        botones_ventana = GridLayout(cols=5, spacing=18, padding=[5, 15, 5, 5])

        botones = [
            "<-", "C", "(", ")", "/",
            "√", "7", "8", "9", "X",
            "%", "4", "5", "6", "-",
            "rad", "1", "2", "3", "+",
            "tan", "^", "0", ".", "="
        ]

        for boton in botones:
            is_operator = boton in {"/", "X", "-", "+", "=", "(", ")", "^", "√", "rad", "%", "tan"}
            btn = CustomButton(
                text=boton, 
                is_operator=is_operator,
                on_press=self.on_button_press
            )
            botones_ventana.add_widget(btn)

        main_ventana.add_widget(botones_ventana)

        return main_ventana

    def on_button_press(self, instance):
        actual = self.entrada.text
        boton_texto = instance.text

        if boton_texto == "C":
            self.entrada.text = ""
        elif boton_texto == "=":
            try:
                resultado = eval(actual)
                if isinstance(resultado, float):
                    self.entrada.text = f"{resultado:.2f}".rstrip('0').rstrip('.')
                else:
                    self.entrada.text = str(resultado)
                self.last_was_equal = True
            except Exception:
                self.entrada.text = "Error"
        else:
            if self.last_was_equal and boton_texto not in {"+", "-", "*", "/", "^", "√", "rad", "%", "(", ")"}:
                self.entrada.text = ""
                self.last_was_equal = False
                self.entrada.text = boton_texto
            else:
                if boton_texto == "^":
                    self.entrada.text = actual + "**"
                elif boton_texto == "X":
                    self.entrada.text = actual + "*"
                elif boton_texto == "√":
                    self.entrada.text = actual + "**0.5"
                elif boton_texto == "rad":
                    self.entrada.text = actual + "*(3.1416/180)"
                elif boton_texto == "tan":
                    self.entrada.text = actual + "*(3.1416/180)"
                elif boton_texto == "<-" and actual == "Error":
                    self.entrada.text = ""
                elif boton_texto == "<-":
                    self.entrada.text = actual[:-1]
                else:
                    self.entrada.text = actual + boton_texto


if __name__ == "__main__":
    CalculadoraApp().run()
