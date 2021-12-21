from tkinter import *
import random
from tkinter import messagebox
from tkinter import ttk
import sqlite3


base = sqlite3.connect('players.db')
cur = base.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS players (name TEXT,lvl TEXT,score INT)')


words = []

lvl1 = ['пар', 'опора', 'пора', 'лава', 'алло', 'овал', 'два', 'вода', 'довод ', 'жажда',
     'лыжа', 'подвал', 'подрыв', 'жвало', 'повар', 'флора', 'порыв', 'форд'
    , 'роды', 'фора', 'дора', 'лавры', 'дрофа']
lvl2 = ['эквадорец', 'полвершка', 'гнездышко', 'недогрузка', 'глухаренок', 'предложный', 'предложный', 'выдержка',
        'глупышка', 'акуловые', 'жонглеры', 'зверушка', 'зверушка',
        'зернышко', 'опекунша', 'шнуровка', 'пролежка', 'пожарный', 'полкруга', 'продувка', 'погрузка', 'верхушка',
        'аэроузел', 'воздушка', 'курганец']
lvl3 = ['круговыми', 'горьковатый', 'экскурсия', 'растолковать', 'многозвучный', 'завывание',
        'контратаки', 'увядающе', 'обезлюдел', 'цивилизаторы',
        'безбрежный', 'лейкемией', 'невпопад', 'помповым', 'гудящий', 'увядший', 'кувшинки', 'искусным', 'чугунный']


name = ''


def game():
    global score,timeleft
    if comboUroven.get() == 'Легкий':
        words = lvl1[:]
    elif comboUroven.get() == 'Средний':
        words = lvl2[:]
    else:
        words = lvl3[:]

    def point(event):

        def vvv(event):
            global name
            name = s.get()
            rega = messagebox.askyesno('Создание игрока',
                                       'Вы действительно хотите создать игрока {}'.format(s.get()))
            if rega == True:
                w.destroy()


        w = Tk()
        w.geometry('300x100')
        w.iconbitmap('regis.ico')
        w.title('Регистрация участника')
        w.configure(bg='#ecc19c')

        q = Label(w, text='Введите имя участника',font=('arial', 14, 'italic bold'), bg='#ecc19c', fg='#1e847f')
        q.pack(pady=5)

        s = Entry(w, width=25)
        s.pack()

        bb = Button(w, text='Подтвердить',foreground='#ff6e40')
        bb.bind("<Button-1>", vvv)
        bb.pack(pady=8)


        w.mainloop()


    def start(event):

        global score, miss,score1

        if (timeleft == 30):
            time()
        Gamedetaillabel.configure(text='')
        if (wordEntry.get() == wordLabel['text']):
            score += 1
            scoreLabelCount.configure(text=score)
        else:
            miss += 1
            print("Пропуски:", miss)
        random.shuffle(words)
        wordLabel.configure(text=words[0])
        wordEntry.delete(0, END)
        score1=score - miss

    def sliders():
        global count, sliderwords
        text = 'Добро пожаловать!'
        if (count >= len(text)):
            count = 0
            sliderwords = ''
        sliderwords += text[count]
        count += 1
        fontLabel1.configure(text=sliderwords)
        fontLabel1.after(200, sliders)

    def time():
        global timeleft, score, miss
        if (timeleft >= 11):
            pass
        else:
            Timeleftlable.configure(fg='red')
        if (timeleft > 0):
            timeleft -= 1
            Timeleftlable.configure(text=timeleft)
            Timeleftlable.after(1000, time)
            if (timeleft==0):

                lvl_info = comboUroven.get()
                cur.execute("INSERT INTO players (name, lvl,score) VALUES (?,?,?)", (name, lvl_info, score1))
                base.commit()

        else:
            Gamedetaillabel.configure(
                text='Попаданий = {} | Пропусков = {} | Итоговый счет = {} '.format(score, miss, (score - miss)))
            rr = messagebox.askretrycancel('Предупрджение', 'Чтобы начать заново нажмите Повтор ')
            if (rr == True):
                score = 0
                timeleft = 30
                miss = 0
                Timeleftlable.configure(text=timeleft)
                wordLabel.configure(text=words[0])
                scoreLabelCount.configure(text=score)
                Gamedetaillabel.configure(text='Введите слово и нажмите Enter')
            else:
                messagebox.showinfo('Предупреждение', 'Для повторной игры в меню нажмите "Играть снова"')
                root.destroy()
                if (timeleft == 0):
                    timeleft = 30
                    score = 0
                    miss = 0



    root = Tk()
    root.geometry('800x600')
    root.configure(bg='#ecc19c')
    root.iconbitmap('ratatype.ico')
    root.title('Ratatype')
    root.resizable(width=False, height=False)

    fontLabel1 = Label(root, text='', font=('arial', 25, 'bold italic'), bg='#ecc19c', fg='#d71b3b', width=30)
    fontLabel1.place(x=105, y=10)
    sliders()
    random.shuffle(words)

    wordLabel = Label(root, text=words[0], font=('arial', 20, 'italic bold'), bg='#ecc19c', fg='black')
    wordLabel.place(x=250, y=200)

    wordEntry = Entry(root, font=('arial', 20, 'italic bold'), bd=5)
    wordEntry.place(x=250, y=250)

    scoreLabel = Label(root, text='Попаданий:', font=('arial', 25, 'italic bold'), bg='#ecc19c', fg='#1e847f')
    scoreLabel.place(x=10, y=100)

    scoreLabelCount = Label(root, text=score, font=('arial', 25, 'italic bold'), bg='#ecc19c', fg='#ff6e40')
    scoreLabelCount.place(x=80, y=140)

    Gamedetaillabel = Label(root, text='Введите слово и нажмите Enter', font=('arial', 20, 'italic bold'),
                            bg='#ecc19c', fg='grey')
    Gamedetaillabel.place(x=10, y=450)

    TimeLabel = Label(root, text='Оставшееся время:', font=('arial', 25, 'italic bold'), bg='#ecc19c', fg='#1e847f')
    TimeLabel.place(x=450, y=100)

    Timeleftlable = Label(root, text=timeleft, font=('arial', 25, 'italic bold'), bg='#ecc19c', fg='#ff6e40')
    Timeleftlable.place(x=600, y=140)

    root.bind("<Button-3>",point)
    root.bind('<Return>', start)
    wordEntry.focus_set()
    root.mainloop()



def exit(event):
    end = messagebox.askyesno('Выход', 'Вы действительно хотите выйти из игры?')
    if end == True:
        newWindow.destroy()


def printer(event):
    messagebox.showinfo('Правила игры', 'Для изучений правил игры в архиве откройте файл "Правила игры"')


def perehod(event):
    g = messagebox.askyesno('Переход', 'Желаете перейти к игре?')
    if g == True:
        game()


def sps(event):
    w=Tk()
    w.geometry('400x270')
    w.title('Список лидеров')
    w.iconbitmap('Lid.ico')
    w.configure(bg='#7fc3c0')
    tv = ttk.Treeview(w)
    tv['columns'] = ('Name', 'Lvl', 'Score')
    tv.column('#0', width=0, stretch=False)
    tv.column('Name', anchor=CENTER, width=100, stretch=False)
    tv.column('Lvl', anchor=CENTER, width=120, stretch=False)
    tv.column('Score', anchor=CENTER, width=120, stretch=False)



    tv.heading('#0', text='', anchor=CENTER)
    tv.heading('Name', text='Имя игрока', anchor=CENTER)
    tv.heading('Lvl', text='Уровень сложности', anchor=CENTER)
    tv.heading('Score', text='Набранные очки', anchor=CENTER)
    tv.pack()


    def updata(event):
        tv.delete()
        cur.execute("SELECT * FROM players")
        rows = cur.fetchall()
        for row in rows:
            tv.insert('', 'end', values=(row[0], row[1], row[2]))

    update=Button(w,text='Обновить таблицу')
    update.pack(pady=5)
    update.bind("<Button-1>",updata)

    w.mainloop()



score = 0
miss = 0
timeleft = 30
count = 0
sliderwords = ''


newWindow = Tk()
newWindow.title('Главное меню')
newWindow.geometry('270x220')
newWindow.iconbitmap('menu.ico')
newWindow.configure(bg='#ecc19c')
newWindow.resizable(width=False, height=False)


PravilaButton = Button(newWindow, text='Правила игры', )
PravilaButton.pack(pady=5)
PravilaButton.bind("<Button-1>", printer)


Uroven = Label(newWindow, text='Выберите уровень сложности', font=('arial', 10, 'bold italic'), bg='#ecc19c',
               fg='#ff6e40')
Uroven.pack(pady=5)

comboUroven = ttk.Combobox(newWindow, state="readonly",
                           values=[
                               "Легкий",
                               "Средний",
                               "Сложный"])
comboUroven.current(0)
comboUroven.pack(pady=5)


Play = Button(newWindow, text='Начать игру', foreground='green')
Play.pack(pady=5)
Play.bind("<Button-1>", perehod)


spisok=Button(newWindow,text='Список лидеров')
spisok.pack(pady=5)
spisok.bind("<Button-1>", sps)

Endd = Button(newWindow, text='Выйти из игры', foreground='red')
Endd.pack(pady=5)
Endd.bind("<Button-1>", exit)


newWindow.mainloop()