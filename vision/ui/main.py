from typing import Optional
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.properties import ObjectProperty
from kivy.uix.camera import Camera
from kivy.clock import Clock
from kivy.core.window import Window

from .. import db
from ..security import hash_password, verify_password

KV = r"""
ScreenManager:
    LoginScreen:
    RegisterScreen:
    CameraScreen:

<LoginScreen>:
    name: "login"
    BoxLayout:
        orientation: "vertical"
        padding: 16
        spacing: 12
        Label:
            text: "Login"
            size_hint_y: None
            height: 40
        TextInput:
            id: email
            hint_text: "Email"
            multiline: False
        TextInput:
            id: senha
            hint_text: "Senha"
            password: True
            multiline: False
        BoxLayout:
            size_hint_y: None
            height: 48
            spacing: 12
            Button:
                text: "Entrar"
                on_release: root.do_login(email.text, senha.text)
            Button:
                text: "Cadastrar"
                on_release: app.sm.current = "register"

<RegisterScreen>:
    name: "register"
    BoxLayout:
        orientation: "vertical"
        padding: 16
        spacing: 12
        Label:
            text: "Cadastro"
            size_hint_y: None
            height: 40
        TextInput:
            id: nome
            hint_text: "Nome"
            multiline: False
        TextInput:
            id: email
            hint_text: "Email"
            multiline: False
        TextInput:
            id: senha
            hint_text: "Senha"
            password: True
            multiline: False
        BoxLayout:
            size_hint_y: None
            height: 48
            spacing: 12
            Button:
                text: "Salvar"
                on_release: root.do_register(nome.text, email.text, senha.text)
            Button:
                text: "Voltar"
                on_release: app.sm.current = "login"

<CameraScreen>:
    name: "camera"
    camera_widget: cam
    BoxLayout:
        orientation: "vertical"
        padding: 8
        spacing: 8
        Camera:
            id: cam
            resolution: (640, 480)
            play: True
            allow_stretch: True
        BoxLayout:
            size_hint_y: None
            height: 48
            spacing: 12
            Button:
                text: "Capturar"
                on_release: root.capture_to_file()
            Button:
                text: "Sair"
                on_release: app.sm.current = "login"
"""

class LoginScreen(Screen):
    def do_login(self, email: str, senha: str) -> None:
        if not email or not senha:
            return
        user = db.get_user_by_email(email)
        if not user:
            return
        if not verify_password(senha, user["senha"]):
            return
        self.manager.current = "camera"

class RegisterScreen(Screen):
    def do_register(self, nome: str, email: str, senha: str) -> None:
        if not nome or not email or not senha:
            return
        if db.get_user_by_email(email):
            return
        hashed = hash_password(senha)
        db.create_user(nome, email, hashed)
        self.manager.current = "login"

class CameraScreen(Screen):
    camera_widget: Camera = ObjectProperty(None)

    def capture_to_file(self) -> None:
        if not self.camera_widget:
            return
        # Salva captura do widget (preview) como PNG; em Android salva em armazenamento interno do app
        self.camera_widget.export_to_png("data/captura.png")

class VisionRoot(ScreenManager):
    pass

class VisionApp(App):
    def build(self):
        db.create_tables()
        Builder.load_string(KV)
        self.sm = self.root = VisionRoot(transition=NoTransition())
        return self.sm
