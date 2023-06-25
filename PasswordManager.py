from tkinter import *
from tkinter import messagebox
import random
import json

# ---------------------------- CHARACTERS ------------------------------- #
letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
           'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
           'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

nr_letters = 3
nr_symbols = 4
nr_numbers = 3


# ---------------------------- PASSWORD GENERATOR ------------------------------- #

def generatePassword():
    passwordEntry.delete(0, END)
    passwordList = []
    for index in range(0, nr_letters + 1):
        passwordList.append(random.choice(letters))
    for index in range(0, nr_symbols + 1):
        passwordList.append(random.choice(symbols))
    for index in range(0, nr_numbers + 1):
        passwordList.append(random.choice(numbers))
    random.shuffle(passwordList)

    password = "".join(passwordList)
    passwordEntry.insert(0, password)


# ---------------------------- SAVE PASSWORD ------------------------------- #

def savePassword():
    filled = True
    website = webSiteEntry.get()
    username = usernameEntry.get()
    password = passwordEntry.get()
    new_data = {
        website: {
            "username": username,
            "password": password
        }
    }

    if len(website) == 0 or len(username) == 0 or len(password) == 0:
        messagebox.showinfo(title="Ops", message="All the fields are required, please fill all.")
    else:
        isOkToSave = messagebox.askokcancel(title=website,
                                            message=f"These are the details entered: \nwebsite->{website}"
                                                    f"\n{username}\n{password}")
        if isOkToSave and filled:
            try:
                with open("data.json", "r") as json_file:
                    # reading old data
                    data = json.load(json_file)
            except FileNotFoundError:
                # create new data file
                with open("data.json", "w") as json_file:
                    # save the first data
                    json.dump(new_data, json_file, indent=4)
            else:
                # update old data with new data
                data.update(new_data)
                with open("data.json", "w") as json_file:
                    # update new data
                    json.dump(data, json_file, indent=4)
            finally:
                webSiteEntry.delete(0, END)
                passwordEntry.delete(0, END)


# ---------------------------- SEARCH ------------------------------- #

def searchPassword():
    passwordInDatabase = False

    if webSiteEntry.get() == "":
        messagebox.showinfo(title="White entry", message="First fill the Website field")
    else:
        try:
            with open("data.json", "r") as json_file:
                data = json.load(json_file)
                for row in data:
                    if row == webSiteEntry.get():
                        password = data[row]["password"]
                        messagebox.showinfo(title="Password finded", message=f"Password of {row} website: \n\n{password}")
                        passwordInDatabase = True

                if not passwordInDatabase:
                    messagebox.showinfo(title="Password not found",
                                        message=f"No password was found for {webSiteEntry.get()} website")
        except FileNotFoundError:
            messagebox.showinfo(title="Data not found")


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Manager")
window.config(pady=50, padx=50)

canvas = Canvas(height=200, width=200)
logoImage = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logoImage)
canvas.grid(column=1, row=0)

websiteLabel = Label(text="Website:")
websiteLabel.grid(column=0, row=1)

webSiteEntry = Entry(width=20)
webSiteEntry.grid(row=1, column=1)
webSiteEntry.focus()

searchButton = Button(text="Search", command=searchPassword)
searchButton.grid(row=1, column=2)

usernameLabel = Label(text="Email/Username")
usernameLabel.grid(column=0, row=2)

usernameEntry = Entry(width=35)
usernameEntry.grid(row=2, column=1, columnspan=2)
usernameEntry.insert(0, "email@email.com")

passwordLabel = Label(text="Password:")
passwordLabel.grid(column=0, row=3)

passwordEntry = Entry(width=21)
passwordEntry.grid(row=3, column=1)

passwordButton = Button(text="Generate Password", command=generatePassword)
passwordButton.grid(row=3, column=2, )

addPasswordButton = Button(text="Add", command=savePassword)
addPasswordButton.grid(row=4, column=1)

window.mainloop()
