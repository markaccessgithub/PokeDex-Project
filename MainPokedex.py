from tkinter import *
import pandas as pd
from PIL import ImageTk,Image
import requests
import re

#this function downloads the pokemon image data as a png
def download(pokemon,search):#the search variable is used to choose official artwork for individual search, or sprites for type search
    x = requests.get("https://pokeapi.co/api/v2/pokemon/" + pokemon)
    try:
        j = x.json()
        if search == "type":
            url = (j["sprites"]["front_default"])
        else:
            url = (j["sprites"]["other"]["official-artwork"]["front_default"])
    except:
        return "error"
    jpg = (pokemon + ".png")
    y = requests.get(url)
    with open(jpg, "wb") as f:#saves the image data as a png
        f.write(y.content)
    return jpg #returns image name for individual search

def start():#this function is for the home window 
    root = Tk()#this is for the tkinter window
    root.geometry('520x300')#this resizes the window
    frame = Frame(root)#a frame is a container within the main window
    frame.pack()
    title = Label(text="Welcome to Pokedex ", width=18, height=8)
    title.pack()
    frame = Frame(root)
    frame.pack()

    button = Button(frame, text ='Log in', fg ='black',width=20, height=5, command=lambda: [root.destroy(), login()])#this creates a button that destroys the window and runs login function
    button.pack( side = RIGHT)
    buttontwo = Button(frame, text ='Create Account', fg ='black', width=20, height=5, command=lambda: [root.destroy(), create()])
    buttontwo.pack( side = LEFT)
    root.mainloop()

def create():#this function is for creating an account
    def enter():
        user = user_create.get()
        passw = passw_create.get()
        if " " in user or " " in passw or ""==user or ""==passw:#this ensures that no spaces or empty inputs are allowed
            error("null","create","null")
        else:
            userCreate(user,passw)
    root = Tk()
    user_create= StringVar(root)#defines a string variable for the entry box
    passw_create= StringVar(root)
    root.geometry('520x300')
    title = Label(text="Create Account", width=18, height=8)
    title.pack()
    frame = Frame(root)
    frame.pack()
    Label(frame, text='Username').grid(row=0)
    Label(frame,text='Password').grid(row=1)

    user_entry = Entry(frame,textvariable = user_create)
    passw_entry=Entry(frame, textvariable = passw_create, show = '*')
    user_entry.grid(row=0, column=1)
    passw_entry.grid(row=1, column=1)
    btn= Button(root, text = 'Submit', command=lambda: [root.destroy(), enter()])
    btn.pack() 
    root.mainloop()

def userCreate(user,passw):#this function takes the data from create() and validates it before updating the csv file
    df=pd.read_csv("UserData.csv")
    for i in df["Name"]:
        if i == user:
            root = Tk()
            root.geometry('520x300')
            title = Label(text="Username already taken", height=8, width = 20,font=("Calibri", 10))
            title.pack()
            frame = Frame(root)
            frame.pack()
            btn= Button(frame, height= 8, width= 40, text = 'Return to Homepage', 
                        font=("Calibri", 10), command=lambda: [root.destroy(), start()])
            btn.pack()
            root.mainloop()
    root = Tk()
    root.geometry('520x300')
    new_row = {"Name":user, "Password": passw,
                "Pokemon_1" : "","Pokemon_2" : "","Pokemon_3" : "",
                "Pokemon_4" : "","Pokemon_5" : "","Pokemon_6" : "",}
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv("UserData.csv", sep=",", index=False)
    title = Label(text="Account Created", height=8, width = 20,font=("Calibri", 10))
    title.pack()
    frame = Frame(root)
    frame.pack()
    btn= Button(frame, height= 8, width= 40, 
                text = 'Return to Homepage', font=("Calibri", 10), command=lambda: [root.destroy(), start()])
    btn.pack()
    root.mainloop()


def login():#this function is for when an existing user logs in 
    def enter():
        user = user_var.get()
        passw = passw_var.get()
        userp(user,passw)
    root = Tk()
    user_var= StringVar(root)
    passw_var= StringVar(root)
    root.geometry('520x300')
    title = Label(text="Enter Details ", width=18, height=8)
    title.pack()
    entframe = Frame(root)
    entframe.pack()
    Label(entframe, text='Username').grid(row=0)
    Label(entframe,text='Password').grid(row=1)

    user_entry = Entry(entframe,textvariable = user_var)
    passw_entry=Entry(entframe, textvariable = passw_var, show = '*')
    user_entry.grid(row=0, column=1)
    passw_entry.grid(row=1, column=1)
    
    btn= Button(root, text = 'Submit', command=lambda: [root.destroy(), enter()])
    btn.pack()
    root.mainloop()


def userp(user,passw):#this function checks if the user's details are correct
    df=pd.read_csv("UserData.csv")
    df.set_index('Name', inplace=False)
    count = 0
    for i in df['Name']:
        if i == user:
            location = count
        else:
            count+=1
    try:
         if passw == df["Password"][location]:
            select(user)
         else:
            print("Incorrect Username/Password")
            login()
    except:
        error(user,"login","null")

def select(user):#this is the choice menu for a logged in user, can choose between editing account, viewing pokemon and adding pokemon
    root = Tk()
    root.geometry('520x300')
    frame = Frame(root)
    frame.pack()
    title = Label(text="Select Option ", width=18, height=8)
    title.pack()
    frame = Frame(root)
    frame.pack()
    viewbutton = Button(frame, text ='View Pokemon', fg ='black',width=20, 
                        height=5, command=lambda: [root.destroy(), team(user,"null","view")])
    viewbutton.pack(side= LEFT)
    addbutton = Button(frame, text ='Add Pokemon', fg ='black',width=20, height=5, command=lambda: [root.destroy(), add(user)])
    addbutton.pack(side= LEFT)
    editbutton = Button(frame, text ='Edit Account', fg ='black',width=20, height=5, command=lambda: [root.destroy(), edit(user)])
    editbutton.pack(side= LEFT)
    root.mainloop()


def add(user):#this function is for adding pokemon to your team
    root = Tk()
    root.geometry('520x300')
    title = Label(text="Search by specific Pokemon or by Type?", width =200, pady=50)
    title.pack()
    frame = Frame(root)
    frame.pack()
    viewbutton = Button(frame, text ='Search By Pokemon', 
                        fg ='black',width=20, height=5, command=lambda: [root.destroy(), pokesearch(user,"mon")])
    viewbutton.pack(side= LEFT)
    addbutton = Button(frame, text ='Search By Type', fg ='black',width=20, height=5, command=lambda: [root.destroy(), pokesearch(user,"type")])
    addbutton.pack(side= RIGHT)
    root.mainloop()


def error(user,type,pokemon):#this function takes care of most errors in validation such as incorrect pokemon searches
    root = Tk()
    root.geometry("520x300")
    if type == "search":
            label = Label(root,pady=50, text="{} does not exist".format(pokemon))
            label.pack()
            button = Button(root, text ='Return to search ', 
                            fg ='black',width=20, height=5, command=lambda: [root.destroy(), pokesearch(user,"mon")])
            button.pack()
    if type == "login" or type=="create":
            if type == "create":
                text="Invalid"
            else:
                text="Incorrect"
            label = Label(root,pady=50, text=f"{text} Username/Password")
            label.pack()
            button = Button(root, text ='Return to Home ', fg ='black',width=20, height=5, command=lambda: [root.destroy(), start()])
            button.pack()
    if type =="change":
        label = Label(root,pady=50, text="Invalid Username")
        label.pack()
        button = Button(root, text ='Enter Different Username', fg ='black',width=20, height=5, command=lambda: [root.destroy(), change(user)])
        button.pack()
    root.mainloop()
    
    
def pokesearch(user,search):#this fucntion is for searching for a pokemon/type and allows the user to choose
    def enter(user):#this fucntion is for searching for a pokemon
        mon = mon_enter.get()
        if " " in mon  or ""== mon:
            error(user,"search",mon)
        elif search == "type":
            typeSearch(user,mon)
        else:
            pokemon = mon.lower()
            jpg = download(pokemon,"null")
            if jpg == "error":
                error(user,"search",pokemon)
            else:
                root = Tk()
                root.geometry("450x450")
                title = Label(text="You chose {}".format(pokemon.capitalize()))
                title.pack()
                canvas = Canvas(root, width = 150, height = 150)
                canvas.pack()
                img = Image.open(jpg)
                image1= img.resize((100,100), Image.LANCZOS)
                newimage = ImageTk.PhotoImage(image1)
                canvas.create_image(20, 20, anchor=NW, image=newimage)
                frame = Frame(root)
                frame.pack(side=BOTTOM)
                label = Label(frame, text="Do you wish to add {} to your team?".format(pokemon.capitalize()))
                label.pack()
                yesbutton = Button(frame, text ='Add To Team', fg ='black',width=20, height=5, command=lambda: [root.destroy(), team(user,pokemon,"add")])
                yesbutton.pack(side= LEFT)
                nobutton = Button(frame, text ='Return To Search', fg ='black',width=20, height=5, command=lambda: [root.destroy(), add(user)])
                nobutton.pack(side= RIGHT)
                root.mainloop()
    
    root = Tk()
    root.geometry('520x300')
    if search == "mon":
        title = Label(text="Search by pokemon name or ID", height=10, width=200)
    else:
        title = Label(text="Search by type", height=10, width=200)
    title.pack()
    entry = Frame(root)
    entry.pack()
    mon_enter = StringVar(root)
    Label(entry, text='').grid(row=0)
    user_entry = Entry(entry, textvariable = mon_enter)
    user_entry.grid(row=0, column=1)
    btn= Button(root, text = "Enter", command=lambda: [root.destroy(), enter(user)])
    btn.pack()
    root.mainloop()




def edit(user):#this function is for editing your account
    root = Tk()
    root.geometry('520x300')
    frame = Frame(root)
    frame.pack()
    title = Label(text="Which option?", width=18, height=8)
    title.pack()
    frame = Frame(root)
    frame.pack()
    changebutton = Button(frame, text ='Change Username', fg ='black',width=20, height=5, command=lambda: [root.destroy(), change(user)])
    changebutton.pack(side= LEFT)
    delbutton = Button(frame, text ='Delete Account', fg ='black',width=20, height=5, command=lambda: [root.destroy(), delete(user)])
    delbutton.pack(side= LEFT)
    exitbutton = Button(frame, text ='Exit', fg ='black',width=20, height=5, command=lambda: [root.destroy(), select(user)])
    exitbutton.pack(side= LEFT)
    root.mainloop()

def delete(user):#this function is for the"delete account" option
    def erase(user):
        df = pd.read_csv("UserData.csv")
        row = df.index.get_loc(df[df['Name'] == user].index[0])
        df = df.drop(row)
        df.to_csv("UserData.csv", index = False)
        start()
    root = Tk()
    root.geometry('520x300')
    title = Label(text="Are you sure you want to Delete Account?")
    title.pack()
    select = Frame(root)
    select.pack()
    changebutton = Button(select, text ='Delete Account', fg ='black',width=20, height=5, command=lambda: [root.destroy(), erase(user)])
    changebutton.pack(side= LEFT)
    exitbutton = Button(select, text ='Exit', fg ='black',width=20, height=5, command=lambda: [root.destroy(), edit(user)])
    exitbutton.pack(side= 'right')

    root.mainloop()

def change(user):#this function is for the "change username" function
    def enter(user):
        newuser = user_enter.get()
        df=pd.read_csv("UserData.csv")
        for i in df["Name"]:
            if i == newuser:
                error(user, "change", "null")
                break
        if " " in newuser or newuser=="":
            error(user, "change", "null")
        else:
            row = df.index.get_loc(df[df['Name'] == user].index[0])
            df["Name"][row] = newuser
            df.to_csv("UserData.csv", index = False)
            root = Tk()
            root.geometry('520x300')
            title = Label(text="Username Changed", height=8, width = 20,font=("Calibri", 10))
            title.pack()
            frame = Frame(root)
            frame.pack()
            btn= Button(frame, height= 8, width= 40, text = 'Return to Homepage', font=("Calibri", 10), command=lambda: [root.destroy(), start()])
            btn.pack()
            root.mainloop()

    root = Tk()
    root.geometry('520x300')
    title = Label(text="Change Username", height=10, width=20)
    title.pack()
    entry = Frame(root)
    entry.pack()
    user_enter = StringVar(root)
    Label(entry, text='New Username').grid(row=0)
    user_entry = Entry(entry, textvariable = user_enter)
    user_entry.grid(row=0, column=1)
    btn= Button(root, text = "Change Username", command=lambda: [root.destroy(), enter(user)])
    btn.pack()
    root.mainloop()

    
def team(user,pokemon,flag):#this function displays all pokemon in a user's party, and then does something different -
    #- depending on how the user got here, e.g displays an option to add the searched pokemon if the user chose add pokemon
    def replace(user,pokemon):#this function is for when the user is trying to replace a current pokemon
        target = number.get() 
        print(target)
        x = re.findall("[123456]", target)
        if x and len(target)==1:
            num=int(target)
            df = pd.read_csv("UserData.csv")
            row = df.index.get_loc(df[df['Name'] == user].index[0])
            df.iloc[row][num+1]=pokemon.lower()
            df.to_csv("UserData.csv", index=False)
            text=f"{pokemon.capitalize()} added to team"
        else:
            text="Incorrect Pokemon Entered"
        root = Tk()
        root.geometry('520x300')
        title = Label(root, text=text, height=10, width=20)
        title.pack()
        btn= Button(root, height= 8, width= 40, text = 'Return to Account Page', font=("Calibri", 10), command=lambda: [root.destroy(), select(user)])
        btn.pack()
        root.mainloop()

    df = pd.read_csv("UserData.csv")
    row = df.index.get_loc(df[df['Name'] == user].index[0])
    test = df.iloc[row,2:8]
    for i in test:
        if type(i)==str:
            download(i,"null")
    root = Tk()
    root.geometry('850x700')
    title = Label(text=f"{user}'s Pokemon Team", width=18, height=8)
    title.pack()
    frame = Frame(root,borderwidth=2, relief="solid")
    frame.pack()
    names = []
    for i in range(6):
        if type(test[i])!=str:
            names.append("empty")
        else:
            names.append(test[i])
    imgs = []
    full=1
    for i in range(6):
        if names[i] == "empty" and full==1 and flag =="add":#this statement adds a pokemon to the first empty slot if user is adding a pokemon 
            names[i] = pokemon
            image = Image.open(f"{pokemon}.png")
            image = image.resize((50, 50))
            imgs.append(ImageTk.PhotoImage(image))
            Label(frame, image=imgs[i], borderwidth=2, relief="solid").grid(row=i,column=2, pady=5, padx=5)
            full=0
            df.loc[row][i+2]=pokemon.lower()
            df.to_csv("UserData.csv", index = False)
        elif names[i]=="empty":
            Label(frame, text ="", borderwidth=2, height=3,width=7, relief="solid").grid(row=i,column=2, pady=5, padx=5)
            imgs.append("")
        else:
            image = Image.open(f"{names[i]}.png")
            image = image.resize((50, 50))
            imgs.append(ImageTk.PhotoImage(image))
            Label(frame, image=imgs[i], borderwidth=2, relief="solid").grid(row=i,column=2, pady=5, padx=5)
        Label(frame,text=f"{names[i].capitalize()}").grid(row=i,column=1, padx=10)
        Label(frame, text=f"Pokemon {i+1}").grid(row=i, column=0, padx=10)
    if flag == "add":#this condition displays additional options if the user is adding a pokemon 
        if full==0:
            msg = Label(root,text=f"{pokemon.capitalize()} added to Team", height=2)
            msg.pack()
        else:
            msg = Label(root,text=f"Team Full - if you wish to add {pokemon.capitalize()} enter which pokemon number to replace 1-6", height=2)
            msg.pack()
            number = StringVar(root)
            user_entry = Entry(root, textvariable = number)
            user_entry.pack()
            btn= Button(root, text = "Replace", command=lambda: [root.destroy(), replace(user,pokemon)])
            btn.pack()
    returnbtn= Button(root, text = "Return to Account Menu", command=lambda: [root.destroy(), select(user)])
    returnbtn.pack()
    root.mainloop()



def typeSearch(user,type):#this function is for when the user is searching for a type
    def enter(user):
        pokemon = chosen.get()
        team(user,pokemon,"add")

    x = requests.get("https://pokeapi.co/api/v2/type/" + type)
    j = x.json()
    mons = (j["pokemon"])
    names = []
    imgs=[]
    for i in range(10):#this takes the first 10 pokemon results 
        names.append(mons[i]["pokemon"]["name"])
    for i in range(10):
        download(names[i],"type")
    root = Tk()
    root.geometry('1000x850')
    title = Label(text="{} Type Pokemon:".format(type.capitalize()), width=18, height=8)
    title.pack()

    frame1 = Frame(root,borderwidth=2, relief="solid")
    frame1.pack(anchor=CENTER)
    frame2 = Frame(root,pady=20)
    frame2.pack()


    for i in range(5):#this displays 2 columns beside each other so that it looks good
        image = Image.open(f"{names[i]}.png")
        image = image.resize((70, 70))
        imgs.append(ImageTk.PhotoImage(image))
        Label(frame1, image=imgs[i], borderwidth=2, relief="solid").grid(row=i,column=2, pady=5, padx=5)
        Label(frame1,text=f"{names[i].capitalize()}").grid(row=i,column=1, padx=10)
    for i in range(5):
        image = Image.open(f"{names[i+5]}.png")
        image = image.resize((70, 70))
        imgs.append(ImageTk.PhotoImage(image))
        Label(frame1, image=imgs[i+5], borderwidth=2, relief="solid").grid(row=i,column=4, pady=5, padx=5)
        Label(frame1,text=f"{names[i+5].capitalize()}").grid(row=i,column=3, padx=10)
    msg = Label(frame2, pady=10,text="Choose a pokemon to add to team")
    msg.pack()
    chosen = StringVar(root)
    user_entry = Entry(frame2,textvariable=chosen)
    user_entry.pack()
    btn= Button(frame2, text = "Choose", command=lambda: [root.destroy(),enter(user) ])
    btn.pack()
    returnbtn= Button(root, pady=20, text = "Return to Account Menu", command=lambda: [root.destroy(), select(user) ])
    returnbtn.pack()
    root.mainloop()
#----------------------------MAIN PROGRAM------------------------------------------------------------------------------
   
start()