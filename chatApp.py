# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 00:52:01 2020

@author: SahilHP
"""

import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from kivy.lang import Builder
import socket_client
import os
import sys

class ConnectPage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    def bruh(self):
        print('I am an egg')
    
    def getData(self):
        if os.path.isfile('prev_details.txt'):
            with open('prev_details.txt', 'r') as f:
                d = f.read().split(',')
                prev_ip = d[0]
                prev_port = d[1]
                prev_user = d[2]
        else:
            prev_ip = ""
            prev_port = ""
            prev_user = ""
            
        return prev_ip, prev_port, prev_user

        
    def join_button(self):
        global user
        ip = self.ids.ip_field.text
        port = self.ids.port_field.text
        user = self.ids.user_field.text  
        
        with open('prev_details.txt', 'w') as f:
            f.write(f'{ip},{port},{user}')
            
        info = f'Attempting to join {ip}:{port} as {user}'
        self.set_message(info)
        Clock.schedule_once(self.connect, 1)
        
    def set_message(self, message):
        connectWin.get_screen('Info').ids.msg_lbl.text = message
    
    def connect(self, _):
        ip = self.ids.ip_field.text 
        port = int(self.ids.port_field.text)
        user = self.ids.user_field.text 
        
        if not socket_client.connect(ip, port, user, show_error):
            return
        else:
            connectWin.get_screen('Chat').dispatch('on_listen')
            connectWin.current = "Chat"
    
class InfoPage(Screen):
    
    # def update_text_width(self):
    #     msg = self.ids.msg_lbl
    #     msg.text_size = (msg.width*0.9, None)
    pass

class ChatPage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.register_event_type('on_listen')
        
    def on_listen(self):
        socket_client.start_listening(self.incoming_message, show_error)
    
    def send_message(self):
        msg_field = self.ids.msg_field
        message = msg_field.text
        if message:
            self.update_chat_history(f"""[color=dd2020]{connectWin.get_screen(
                'Connect').ids.user_field.text}[/color] > {message}""")
            socket_client.send(message)
            
        Clock.schedule_once(self.set_focus, 0.1)
        
    def set_focus(self, _):
        self.ids.msg_field.focus = True
        
    def incoming_message(self, username, message):
        self.update_chat_history(f"""[color=20dd20]{
            username}[/color] > {message}""")
        
    def update_chat_history(self, message):
        chat_hist = self.ids.chat_history
        chat_layout = self.ids.chat_layout
        
        chat_hist.text = chat_hist.text + '\n' + message
        chat_hist.height += chat_hist.texture_size[1] + 15
        chat_hist.text_size = (chat_hist.width + 0.98, None)
        
        self.ids.scroll_view.scroll_to(self.ids.scroll_lbl)
    pass

class Manager(ScreenManager):
    pass

connectWin = Builder.load_file('connect.kv')
# chatWin = Builder.load_file('Chat.kv')

def show_error(message):
    connectWin.get_screen('Info').ids.msg_lbl.text = message
    connectWin.current = "Info"
    Clock.schedule_once(sys.exit, 10)
    
class ChatApp(App):
    # def on_start(self):
    #     socket_client.start_listening(self.incoming_message, show_error)
    
    def build(self):
        # self.screen_manager = ScreenManager()
        # self.connect_window = ConnectPage()
        # screen = Screen(name='Connect')
        # screen.add_widget(self.connect_window)
        # self.screen_manager.add_widget(screen)
        
        # self.info_page = InfoPage()
        # screen = Screen(name="Info")
        # screen.add_widget(self.info_page)
        # # self.screen_manager.add_widget(screen)
        return connectWin
    
    # def create_chat_page(self):
    #     return chatWin
    
if __name__ == '__main__':
    chat_app = ChatApp()
    chat_app.run()
    