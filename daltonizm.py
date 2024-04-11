import tkinter as tk
from tkinter import *
from PIL import ImageTk, Image
import os
import random
from datetime import datetime
from tkinter import messagebox
import smtplib, ssl
from email.message import EmailMessage

class LoginForn:
    def __init__(self, window):
        self.window = window
        self.window.geometry('1166x718')
        self.window.state('zoomed')
        self.window.resizable(0, 0)
        self.server = None

        self.used_images = []

        ####TŁO####
        self.bg_frame = Image.open('tlo.png')
        self.bg_frame = self.bg_frame.resize((self.window.winfo_screenwidth(), self.window.winfo_screenheight()))
        photo = ImageTk.PhotoImage(self.bg_frame)
        self.bg_panel = Label(self.window, image=photo)
        self.bg_panel.image = photo
        self.bg_panel.place(x=0, y=0, relwidth=1, relheight=1)

        ####LOGIN RAMKA####
        self.login_frame = Frame(self.window, bg='#040405', width='950', height=600)
        self.login_frame.place(x=200, y=70)

        self.txt = 'TEST NA DALTONIZM'
        self.heading = Label(self.login_frame, text=self.txt, font=('yu gothic ui', 25, 'bold'), bg='#040405', fg='white')
        self.heading.place(x=80, y=30, width=500, height=30)

        ####LEWA STRONA ZDJĘCIE####
        self.side_left = Image.open('logowanie.jpg')
        photo = ImageTk.PhotoImage(self.side_left)
        self.side_left_label = Label(self.login_frame, image=photo, bg='#040405')
        self.side_left_label.image = photo
        self.side_left_label.place(x=150, y=100)

        ####OBRAZ LOGOWANIA####
        self.sign_image = Image.open('mail2.jpg')
        self.sign_image = self.sign_image.resize((120, 120))
        photo = ImageTk.PhotoImage(self.sign_image)
        self.sign_image_label = Label(self.login_frame, image=photo, bg='#040405')
        self.sign_image_label.image = photo
        self.sign_image_label.place(x=625, y=130)

        self.sign_label = Label(self.login_frame, text='Podaj maila', bg='#040405', fg='white', font=('yu gothic ui', 13, 'bold'))
        self.sign_label.place(x=640, y=240)

        ####LOGOWANIE####
        self.username_label = Label(self.login_frame, text='Mail', bg='#040405', font=('yu gothic ui', 13, 'bold'), fg='#4f4e4d')
        self.username_label.place(x=550, y=300)

        self.username_entry = Entry(self.login_frame, highlightthickness=0, relief=FLAT, bg='#040405', fg='#6b6a69', font=('yu gothic ui', 12, 'bold'))
        self.username_entry.place(x=590, y=335, width=270)

        self.username_line = Canvas(self.login_frame, width=300, height=2.0, bg='#bdb9b1', highlightthickness=0)
        self.username_line.place(x=550, y=359)

        ####IKONA PRZY LOGOWANIU####
        self.username_icon = Image.open('mail.jpg')
        self.username_icon = self.username_icon.resize((30, 30))
        photo = ImageTk.PhotoImage(self.username_icon)
        self.username_icon_label = Label(self.login_frame, image=photo, bg='#040405')
        self.username_icon_label.image = photo
        self.username_icon_label.place(x=550, y=325)

        self.next_button = Button(self.login_frame, text='Dalej', bg='#6b6a69', fg='#bdb9b1', font=('yu gothic ui', 12, 'bold'), relief=FLAT, command=self.rules_page)
        self.next_button.place(x=620, y=400, width=140, height=40)

    def rules_page(self):
        mail = self.username_entry.get()
        if not mail:
            messagebox.showerror("Błąd", "Proszę podać adres e-mail.")
            return
    
        self.mail = mail 

        self.login_frame.destroy()
        self.next_frame = Frame(self.window, bg='#bdb9b1', width='950', height=600)
        self.next_frame.place(x=200, y=70)
        label_rules = Label(self.next_frame, text='Przeczytaj zasady:', font=('yu gothic ui', 13, 'bold'), bg='#bdb9b1', fg='black')
        label_rules.place(x=400, y=20)

        rules_text = """
        
        1. Wyświetlone zostaną zdjęcia, pod którymi wpisz liczbę widoczną na zdjęciu i naciśnij przycisk dalej.
        
        2. W przypadku problemu z rozpoznaniem liczb, naciśnij przycisk dalej.
        
        3. Wynik zostanie wyświetlony po zakończonym teście.
        
        4. Po zakończeniu można zapisać swój wynik do bazy.
        
        5. Kliknij start aby rozpocząć test.
        """

        rules_label = Label(self.next_frame, text=rules_text, font=('yu gothic ui', 12), bg='#bdb9b1', fg='black', justify=LEFT)
        rules_label.place(x=20, y=50)

        self.start_button = Button(self.next_frame, text='Start', bg='#6b6a69', fg='#bdb9b1', font=('yu gothic ui', 12, 'bold'), relief=FLAT, command=self.start_test)
        self.start_button.place(x=410, y=450, width=140, height=40)

    def start_test(self):
        self.next_frame.destroy()
        self.used_images = []  
        self.used_images_count = 0
        self.correct_answers = 0  
        self.test_frame = Frame(self.window, bg='#bdb9b1', width='950', height=600)
        self.test_frame.place(x=200, y=70)
        self.show_next_image()


    def show_next_image(self):
        if self.used_images_count == 15: 
            self.show_result()
            return

        while True:
            image_files = [file for file in os.listdir('dane') if file not in self.used_images]
            if not image_files:
                return

            random_image = random.choice(image_files)
            random_image_path = os.path.join('dane', random_image)

            if random_image not in self.used_images:
                break

        self.used_images.append(random_image)
        self.used_images_count += 1

        image = Image.open(random_image_path)
        image = image.resize((320, 300))
        self.photo = ImageTk.PhotoImage(image)

        self.image_label = Label(self.test_frame, image=self.photo, bg='black')
        self.image_label.image = self.photo
        self.image_label.place(x=325, y=50)

        self.result_entry = Entry(self.test_frame, highlightthickness=0, relief=FLAT, bg='#040405', fg='white', font=('yu gothic ui', 12, 'bold'), justify='center')
        self.result_entry.place(x=325, y=380, width=323)
        self.result_entry.focus_set() #ustawienie kursora w polu aby nie trzeba bylo klikac
        self.result_entry.bind("<Return>", lambda event: self.evaluate_answer()) #zeby enter dzialal jak dalej

        self.next_button = Button(self.test_frame, text='Dalej', bg='#6b6a69', fg='#bdb9b1', font=('yu gothic ui', 12, 'bold'), relief=FLAT, command=self.evaluate_answer)
        self.next_button.place(x=410, y=450, width=140, height=40)


    def show_result(self):

        self.test_frame.destroy()

        self.result_frame = Frame(self.window, bg='#040405', width='950', height='600')
        self.result_frame.place(x=200, y=70)

        self.result_left = Image.open('zapisywanie.jpg')
        photo_left = ImageTk.PhotoImage(self.result_left)
        self.result_left_label = Label(self.result_frame, image=photo_left, bg='#040405')
        self.result_left_label.image = photo_left
        self.result_left_label.place(x=65, y=100)

        result_text_label = Label(self.result_frame, text='Twój wynik to:', font=('yu gothic ui', 22, 'bold'), bg='#040405', fg='white')
        result_text_label.place(x=580, y=180)

        result_label = Label(self.result_frame, text=f'{self.correct_answers}/15', font=('yu gothic ui', 22, 'bold'), bg='#040405', fg='white')
        result_label.place(x=650, y=240)

        back_button = Button(self.result_frame, text='Wróć', bg='#6b6a69', fg='#bdb9b1', font=('yu gothic ui', 12, 'bold'), relief=FLAT, command=self.go_back_to_login)
        back_button.place(x=470, y=390, width=120, height=40)

        save_button = Button(self.result_frame, text='Zapisz', bg='#6b6a69', fg='#bdb9b1', font=('yu gothic ui', 12, 'bold'), relief=FLAT, command=self.save_results)
        save_button.place(x=620, y=390, width=120, height=40)

        send_email_button = Button(self.result_frame, text='Wyślij na maila', bg='#6b6a69', fg='#bdb9b1', font=('yu gothic ui', 12, 'bold'), relief=FLAT, command=self.send_email)
        send_email_button.place(x=770, y=390, width=120, height=40)

    def evaluate_answer(self):
        user_answer = self.result_entry.get()
        current_image = self.used_images[self.used_images_count - 1]  
        if user_answer == current_image.split('.')[0]:
            self.correct_answers += 1

        self.result_entry.delete(0, END)

        self.show_next_image()

        if self.used_images_count == 15:
            self.show_result()

    def go_back_to_login(self):
        self.result_frame.destroy()
        self.__init__(self.window)  

    def save_results(self):
        if not hasattr(self, 'mail'):
            return

        mail = self.mail
        now = datetime.now()
        current_time = now.strftime("%Y-%m-%d %H:%M:%S")
        wynik = f'Wynik: {self.correct_answers}/15'
        result_string = f'{current_time} - {mail} - {wynik}\n'
        
        with open('maile.txt', 'a') as file:
            file.write(result_string)
    
    #pamiętaj o wpisaniu maila i hasła aby wysyłanie maila było możliwe
    def send_email(self):
        if not hasattr(self, 'mail'):
            return

        mail = self.mail
        wynik = f'{self.correct_answers}/15'

        port = 465
        smtp_server = "smtp.gmail.com"
        sender_email = "mail"
        receiver_email = mail
        password = 'password'

        message = EmailMessage()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = "Wynik testu na daltonizm"
        message.set_content(f"Twój wynik testu na daltonizm to: {wynik}")

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, password)
            server.send
            server.send_message(message)

def page():
    window = tk.Tk()
    LoginForn(window)
    window.mainloop()

if __name__ == '__main__':
    page()
