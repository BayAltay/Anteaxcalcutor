"""
Gizli Hesap Makinesi - Python Kivy Uygulaması
Hesap makinesi + Şifreli Notlar
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
import json
import os
from datetime import datetime

# Pencere boyutu
Window.size = (400, 600)

class SecretCalculator(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.notes_file = 'notes.json'
        self.current_display = '0'
        self.operator = None
        self.first_number = None
        self.password = '1234'
        self.authenticated = False
        self.notes = self.load_notes()

    def load_notes(self):
        """Notları dosyadan yükle"""
        try:
            if os.path.exists(self.notes_file):
                with open(self.notes_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except:
            pass
        return []

    def save_notes(self):
        """Notları dosyaya kaydet"""
        try:
            with open(self.notes_file, 'w', encoding='utf-8') as f:
                json.dump(self.notes, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Not kaydedilemedi: {e}")

    def build(self):
        """Ana ekran"""
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Başlık
        title = Label(
            text='Gizli Hesap Makinesi',
            size_hint_y=0.1,
            font_size='24sp',
            bold=True
        )
        main_layout.add_widget(title)

        # Hesap makinesi bölümü
        calc_layout = BoxLayout(orientation='vertical', size_hint_y=0.7, spacing=5)
        
        # Display
        self.display = TextInput(
            text=self.current_display,
            font_size='32sp',
            multiline=False,
            readonly=True,
            size_hint_y=0.15
        )
        calc_layout.add_widget(self.display)

        # Butonlar grid
        buttons_layout = GridLayout(cols=4, spacing=5, size_hint_y=0.85)
        
        buttons = [
            ('7', self.on_number_press), ('8', self.on_number_press), ('9', self.on_number_press), ('/', self.on_operator_press),
            ('4', self.on_number_press), ('5', self.on_number_press), ('6', self.on_number_press), ('*', self.on_operator_press),
            ('1', self.on_number_press), ('2', self.on_number_press), ('3', self.on_number_press), ('-', self.on_operator_press),
            ('0', self.on_number_press), ('.', self.on_number_press), ('=', self.on_calculate), ('C', self.on_clear),
            ('Delete', self.on_delete), ('+', self.on_operator_press),
        ]

        for button_text, callback in buttons:
            btn = Button(
                text=button_text,
                font_size='18sp',
                background_color=self.get_button_color(button_text)
            )
            btn.bind(on_press=lambda instance, text=button_text, cb=callback: cb(text))
            buttons_layout.add_widget(btn)

        calc_layout.add_widget(buttons_layout)
        main_layout.add_widget(calc_layout)

        # Gizli notlar butonu
        notes_btn = Button(
            text='Gizli Notlar (1234)',
            size_hint_y=0.1,
            background_color=(0.2, 0.6, 0.8, 1),
            font_size='16sp'
        )
        notes_btn.bind(on_press=self.open_notes)
        main_layout.add_widget(notes_btn)

        return main_layout

    def get_button_color(self, button_text):
        """Buton rengini belirle"""
        if button_text in ['/', '*', '-', '+', '=']:
            return (0.8, 0.4, 0.2, 1)
        elif button_text == 'C':
            return (0.8, 0.2, 0.2, 1)
        elif button_text == 'Delete':
            return (0.6, 0.2, 0.8, 1)
        else:
            return (0.3, 0.3, 0.3, 1)

    def on_number_press(self, number):
        """Sayı tuşuna basıldı"""
        if self.current_display == '0' and number != '.':
            self.current_display = number
        elif not (number == '.' and '.' in self.current_display):
            self.current_display += number
        self.display.text = self.current_display

    def on_operator_press(self, op):
        """Operatör tuşuna basıldı"""
        try:
            self.first_number = float(self.current_display)
            self.operator = op
            self.current_display = '0'
            self.display.text = self.current_display
        except:
            self.display.text = 'Hata'

    def on_calculate(self, _=None):
        """Hesapla"""
        try:
            if self.operator and self.first_number is not None:
                second_number = float(self.current_display)
                
                if self.operator == '/':
                    if second_number == 0:
                        self.display.text = 'Hata'
                        self.current_display = '0'
                        return
                    result = self.first_number / second_number
                elif self.operator == '*':
                    result = self.first_number * second_number
                elif self.operator == '-':
                    result = self.first_number - second_number
                elif self.operator == '+':
                    result = self.first_number + second_number
                
                if result == int(result):
                    self.current_display = str(int(result))
                else:
                    self.current_display = str(round(result, 6))
                
                self.display.text = self.current_display
                self.first_number = None
                self.operator = None
        except:
            self.display.text = 'Hata'
            self.current_display = '0'

    def on_clear(self, _=None):
        """Temizle"""
        self.current_display = '0'
        self.operator = None
        self.first_number = None
        self.display.text = self.current_display

    def on_delete(self, _=None):
        """Son karakteri sil"""
        if len(self.current_display) > 1:
            self.current_display = self.current_display[:-1]
        else:
            self.current_display = '0'
        self.display.text = self.current_display

    def open_notes(self, _=None):
        """Notlar penceresini aç"""
        self.authenticated = False
        
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        
        # Şifre girişi
        password_input = TextInput(
            text='',
            password=True,
            multiline=False,
            hint_text='Sifre Girin (1234)',
            font_size='16sp',
            size_hint_y=0.15
        )
        content.add_widget(password_input)

        error_label = Label(text='', size_hint_y=0.1, color=(1, 0, 0, 1))
        content.add_widget(error_label)

        def check_password(btn):
            """Şifreyi kontrol et"""
            if password_input.text == self.password:
                self.authenticated = True
                popup.dismiss()
                self.show_notes()
            else:
                error_label.text = 'Yanlis Sifre'

        login_btn = Button(text='Giris', size_hint_y=0.15)
        login_btn.bind(on_press=check_password)
        content.add_widget(login_btn)

        popup = Popup(
            title='Gizli Notlar',
            content=content,
            size_hint=(0.9, 0.4)
        )
        popup.open()

    def show_notes(self):
        """Notları göster"""
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)

        # Notların listesi
        scroll = ScrollView(size_hint_y=0.6)
        notes_layout = GridLayout(cols=1, spacing=5, size_hint_y=None)
        notes_layout.bind(minimum_height=notes_layout.setter('height'))

        for i, note in enumerate(self.notes):
            note_btn = Button(
                text=f"Not: {note['title']}\n{note['content'][:30]}",
                size_hint_y=None,
                height=80,
                background_color=(0.2, 0.4, 0.6, 1)
            )
            note_btn.bind(on_press=lambda btn, idx=i: self.edit_note(idx))
            notes_layout.add_widget(note_btn)

        scroll.add_widget(notes_layout)
        content.add_widget(scroll)

        # Not ekleme
        new_note_layout = BoxLayout(orientation='vertical', spacing=5, size_hint_y=0.4)
        
        title_input = TextInput(hint_text='Not Basligi', multiline=False, size_hint_y=0.2)
        content_input = TextInput(hint_text='Not Icerigi', multiline=True, size_hint_y=0.6)
        
        def add_note(btn):
            """Yeni not ekle"""
            if title_input.text.strip():
                self.notes.append({
                    'title': title_input.text,
                    'content': content_input.text,
                    'date': datetime.now().strftime('%d.%m.%Y %H:%M')
                })
                self.save_notes()
                title_input.text = ''
                content_input.text = ''
                popup.dismiss()
                self.show_notes()

        add_btn = Button(text='+ Not Ekle', size_hint_y=0.2)
        add_btn.bind(on_press=add_note)
        
        new_note_layout.add_widget(title_input)
        new_note_layout.add_widget(content_input)
        new_note_layout.add_widget(add_btn)
        
        content.add_widget(new_note_layout)

        popup = Popup(
            title='Gizli Notlarim',
            content=content,
            size_hint=(0.95, 0.9)
        )
        popup.open()

    def edit_note(self, index):
        """Notu düzenle"""
        note = self.notes[index]
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)

        title_input = TextInput(text=note['title'], multiline=False, size_hint_y=0.2)
        content_input = TextInput(text=note['content'], multiline=True, size_hint_y=0.6)

        buttons_layout = BoxLayout(size_hint_y=0.2, spacing=5)

        def save_edit(btn):
            """Değişiklikleri kaydet"""
            self.notes[index]['title'] = title_input.text
            self.notes[index]['content'] = content_input.text
            self.notes[index]['date'] = datetime.now().strftime('%d.%m.%Y %H:%M')
            self.save_notes()
            popup.dismiss()
            self.show_notes()

        def delete_note(btn):
            """Notu sil"""
            del self.notes[index]
            self.save_notes()
            popup.dismiss()
            self.show_notes()

        save_btn = Button(text='Kaydet')
        save_btn.bind(on_press=save_edit)
        delete_btn = Button(text='Sil', background_color=(1, 0.2, 0.2, 1))
        delete_btn.bind(on_press=delete_note)

        buttons_layout.add_widget(save_btn)
        buttons_layout.add_widget(delete_btn)

        content.add_widget(Label(text=f"Tarih: {note['date']}", size_hint_y=0.1))
        content.add_widget(title_input)
        content.add_widget(content_input)
        content.add_widget(buttons_layout)

        popup = Popup(
            title='Notu Duzenle',
            content=content,
            size_hint=(0.95, 0.7)
        )
        popup.open()


if __name__ == '__main__':
    SecretCalculator().run()
