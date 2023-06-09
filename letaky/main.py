from bs4 import BeautifulSoup
import requests
from tkinter import *
from tkinter import ttk
from tkinter.font import nametofont
import smtplib
from_email = "choose_mail"
penny_url = "https://www.akcniceny.cz/zbozi/penny-market/"
penny_list = []
lidl_url = "https://www.akcniceny.cz/zbozi/lidl/"
lidl_list = []
#funkce
#webscraping
def get_data(market_url, market_list):
    response = requests.get(market_url)
    web = response.text
    soup = BeautifulSoup(web, "html.parser")

    main_class = "main"
    product_class_name = "row"
    prise_class_name = "fs-20"
    articles_name = []
    articles_prise = []

    articles = soup.find_all(class_=product_class_name)
    prise = soup.find_all(class_=prise_class_name)


    for index in range(8, len(articles)-4):
        x = articles[index].find("h2")
        if x:

            app_list = []
            x = x.text.upper()
            app_list.append(x)
            sale = articles[index].find(class_="badge")
            if sale:
                sale = sale.getText().rstrip()
                sale = sale.replace(" ", "")
                sale = sale.replace("\n", "")
                sale = sale.replace("%", "")
                sale = int(sale)
                app_list.append(sale)

            if len(articles_name) > 0:
                if x != articles_name[len(articles_name)-1][0]:
                    articles_name.append(app_list)
            else:
                articles_name.append(app_list)

    for index in range(0, len(prise)):
        y = prise[index].getText().rstrip()
        if y:
            if " - " in y:
                y = y.split(" - ")
                y = y[0]
            y = y.strip()
            if len(y) < 14:
                last_prise = y.replace(" Kč", "")
                last_prise = last_prise.replace(",", ".")
                if len(articles_prise) > 0:

                    articles_prise.append(float(last_prise))
                else:
                    articles_prise.append(float(last_prise))

    all_page = soup.find(class_="my-3")
    all_page = all_page.find_all("a")

    max_page = all_page[len(all_page)-2]

    max_page = int(max_page.text)

    for index in range(2, max_page+1):
        res = (f"{market_url}/strana-{index}/")

        response = requests.get(res)
        web = response.text
        soup = BeautifulSoup(web, "html.parser")
        articles = soup.find_all(class_=product_class_name)
        prise = soup.find_all(class_=prise_class_name)

        for index in range(8, len(articles) - 4):

            x = articles[index].find("h2")
            link = ""
            link2 = ""

            if x:
                for linkx in x:
                    link = linkx.get("href")
                if articles[index-1].find("h2"):
                    for linkx2 in articles[index-1].find("h2"):
                        link2 = linkx2.get("href")

                app_list = []
                x = x.text.upper()
                app_list.append(x)
                sale = articles[index].find(class_="badge")
                if sale:
                    sale = sale.getText().rstrip()
                    sale = sale.replace(" ", "")
                    sale = sale.replace("\n", "")
                    sale = sale.replace("%", "")
                    sale = int(sale)
                    app_list.append(sale)

                if len(articles_name) > 0:
                    if  link != link2:
                        articles_name.append(app_list)
                else:
                    articles_name.append(app_list)

        for index in range(0, len(prise)):
            y = prise[index].getText().rstrip()
            if y:
                if " - " in y:
                    y = y.split(" - ")
                    y = y[0]
                y = y.strip()
                if len(y) < 14:
                    last_prise = y.replace(" Kč", "")
                    last_prise = last_prise.replace(",", ".")
                    last_prise = last_prise.replace(" ", "")
                    if len(articles_prise) > 0:

                        articles_prise.append(float(last_prise))
                    else:
                        articles_prise.append(float(last_prise))

    for index in range(len(articles_name)):
        one_list = []
        one_list.append(articles_name[index])
        one_list.append(articles_prise[index])
        market_list.append(one_list)
#tkinter

def start_find():
    result = user_input.get().upper()
    find_text = ""
    for one_list in penny_list:
        if result in one_list[0][0]:
            find_text = f"{one_list[0][0]} {one_list[1]} Kč "
            find_label.insert(END, f"{find_text} - PENNY")
    for one_list in lidl_list:
        if result in one_list[0][0]:
            find_text = f"{one_list[0][0]} {one_list[1]} Kč "
            find_label.insert(END, f"{find_text} - LIDL")
    user_input.delete(0, END)
def table_text(market_list, market_table):
    find_text = ""
    index = 0
    for one_list in market_list:
        find_text = one_list[0][0].replace(", ", "\n")
        if len(one_list[0]) > 1:
            market_table.insert(parent='', index='end', iid=index, text='', values=(find_text, f"{one_list[1]} Kč  {one_list[0][1]}%"))
        else:
            market_table.insert(parent='', index='end', iid=index, text='', values=(find_text, f"{one_list[1]} Kč"))
        index += 1
# Fce na přidání zboží PENNY
def add_penny_article():
    curItem = penny_table.focus()
    article_to_add = penny_table.item(curItem)["values"]
    result_label.insert(END, f"{article_to_add[0]} {article_to_add[1]} - PENNY")

# Fce na přidání zboží LIDL
def add_lidl_article():
    curItem = lidl_table.focus()
    article_to_add = lidl_table.item(curItem)["values"]
    result_label.insert(END, f"{article_to_add[0]} {article_to_add[1]} - LIDL")

# Vymzat položku
def delete_article():
    result_label.delete(ANCHOR)
#přidat položku z vyhledávaných
def add_from_find():
    article_to_add = find_label.get(ANCHOR)
    result_label.insert(END, article_to_add)

#Vyčšistit vyhledávání
def delete_all_find():
    find_label.delete(0, END)

#odeslaní mailu
def send_mail():
    email = mail_input.get()
    password = "choose_password"
    # předmět po subjeckt a pak \n\n
    subject = "Subject: Nakup\n\n"

    all_result = result_label.get(0, END)
    text = ""
    for one_result in all_result:
        if one_result[len(one_result)-1] == "Y":
            text = f"{text}{one_result} \n"
    for one_result in all_result:
        if one_result[len(one_result)-1] == "L":
            text = f"{text}{one_result} \n"

    for_send = f"{subject}{text}"

    with smtplib.SMTP(host="smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=from_email, password=password)
        connection.sendmail(from_addr=from_email, to_addrs=email, msg=for_send.encode('utf-8'))

get_data(penny_url, penny_list)
get_data(lidl_url, lidl_list)


# Okno
main_color = "#13678A"

window = Tk()
window.geometry("1250x800+30+140")
window.resizable(False, False)
window.title("Přehled akcí Penny/Lidl")
window.config(bg=main_color)
window2 = Tk()
window2.config(bg=main_color)
window2.geometry("600x400+0+0")
window2.resizable(False, False)
window2.title("Vybrané zboží")
window2.config(bg=main_color)

#fREmy

penny_frame = Frame(width=40, height=50, bg=main_color)
lidl_frame = Frame(width=20, bg=main_color)
penny_frame.grid(row=2, column=0)
lidl_frame.grid(row=2, column=1)
button_frame = Frame(width=30, height=30, bg=main_color)
button_frame.grid(row=4, column=1, sticky=S+W)
win2_but_frame = Frame(window2, bg=main_color)
win2_but_frame.grid(row=1, column=0, sticky=W)

#Uživatelský vstup
user_input = Entry(width=48, font=("Arial", 14))
user_input.insert(0, "")
user_input.grid(row=0, column=0, pady=(10, 0), padx=(10, 0))
mail_input = Entry(win2_but_frame, width=30, font=("Arial", 14))
mail_input.grid(row=0, column=2)

#Tlačítko
find_but = Button(text="Hledej", font=("Ariel", 10), command=start_find)
find_but.grid(row=0, column=1, pady=(10, 0), padx=2, sticky=W)
add_penny_but = Button(penny_frame, text="Přidej do vybraných PENNY", font=("Ariel", 12), command=add_penny_article)
add_penny_but.grid(row=1, column=0)
add_lidl_but = Button(lidl_frame, text="Přidej do vybraných LIDL", font=("Ariel", 12), command=add_lidl_article)
add_lidl_but.grid(row=1, column=0)
delete_one_article_but = Button(win2_but_frame, text="Odstraň ze seznamu", font=("Ariel", 12), command=delete_article)
delete_one_article_but.grid(row=0, column=0, sticky=W)
add_find_but = Button(button_frame, width=20, height=2, text="Přidej z vyhledávaných", font=("Ariel", 12), command=add_from_find)
add_find_but.grid(row=0, column=0, sticky=W+N)
delete_find_but = Button(button_frame, width=20, height=2, text="vymaž vše vyhledané", font=("Ariel", 12), command=delete_all_find)
delete_find_but.grid(row=1, column=0, sticky=W+N)
send_but = Button(win2_but_frame, text="pošli emailem", font=("Ariel", 12), command=send_mail)
send_but.grid(row=0, column=1, sticky=W)

# Label pro košík
result_label = Listbox(window2, height=17, width=70, bg=main_color, fg="#DEF0EE", font=("Arial", 12))
result_label.grid(row=0, column=0)

#Label pro vyhledávání
# Label pro zobrazení vyhledávání
find_label = Listbox(width=70, bg=main_color, fg="#DEF0EE", font=("Arial", 12))
find_label.grid(row=4, column=0, sticky=S+W)


# styly tabulky
style = ttk.Style()
style.configure("Treeview", background="silver", rowheight=50, fieldbackground="blue", font=("Arial", 12))
style.map("Treeview", background=[("selected", "green")])
#Label pro Penny
text_scrollbar = Scrollbar(penny_frame, width=8)
text_scrollbar.grid(row=0, column=1, sticky=N+S)
penny_table = ttk.Treeview(penny_frame, yscrollcommand=text_scrollbar.set)
penny_table.grid(row=0, column=0)
nametofont("TkHeadingFont").configure(size=14)
penny_table['columns'] = ('Název položky', 'Cena/sleva')
penny_table.column("#0", width=0,  stretch=NO)
penny_table.column("Název položky", anchor=W, width=480)
penny_table.column("Cena/sleva", anchor=CENTER, width=110)

penny_table.heading("#0", text="", anchor=CENTER)
penny_table.heading("Název položky", text="Název položky - PENNY", anchor=CENTER)
penny_table.heading("Cena/sleva", text="Cena/sleva", anchor=CENTER)

# Propojíme scrollbar s list_boxem
text_scrollbar.config(command=penny_table.yview)

#Label pro Lidl

text_scrollbar = Scrollbar(lidl_frame, width=8)
text_scrollbar.grid(row=0, column=1, sticky=N+S)
lidl_table = ttk.Treeview(lidl_frame, yscrollcommand=text_scrollbar.set)
lidl_table.grid(row=0, column=0)
nametofont("TkHeadingFont").configure(size=14)
lidl_table['columns'] = ('Název položky', 'Cena/sleva')
lidl_table.column("#0", width=0,  stretch=NO)
lidl_table.column("Název položky", anchor=W, width=480)
lidl_table.column("Cena/sleva", anchor=CENTER, width=110)

lidl_table.heading("#0", text="", anchor=CENTER)
lidl_table.heading("Název položky", text="Název položky - LIDL", anchor=CENTER)
lidl_table.heading("Cena/sleva", text="Cena/sleva", anchor=CENTER)

# Propojíme scrollbar s list_boxem
text_scrollbar.config(command=lidl_table.yview)

#doplnění tabulky penny a lidl
table_text(penny_list, penny_table)
table_text(lidl_list, lidl_table)

#Hlavní cyklus
window.mainloop()
