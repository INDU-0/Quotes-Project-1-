import requests

url="http://[2405:201:900e:50b2:ecd7:c98c:44f9:f412]:8000"

choice=99
usernam=" "
ag="a"
passw= " "
tkn=""


def sign_up():
    try:
        global usernam, ag, passw
        while not(usernam.isalnum() and len(usernam)<=20 and len(usernam)>=3):
            usernam=input(" Enter Username ( Min Char:3, Max Char:20): ").strip()
        while not(ag.isdigit() and int(ag)>=18 and int(ag)<=120):
            ag=input(" Enter Your Age (Msg me at 9623171750 if age more than 36yr old, Please): ") #I just like older women deal with it
        ag=int(ag)
        while not(passw.isalnum() and len(passw)>=8):
            passw=input(" Enter A Password: ").strip()

        body1= {
            "username": usernam,
            "password": passw,
            "age": ag
        }
        s=requests.post(url+"/auth/signup", json=body1)

        if s.status_code>=400:
            print("The Dev Is A Dumbass Twin 🤞")
            print(s.text)
        else:
            print("Sign Up Successful 😊")
        
        body90={
            "username":usernam,
            "password":passw
        }
        jpg= requests.post(url+"/auth/signin", json=body90)
        olp=jpg.json()
        koi=olp['token']
        return koi, usernam
    
    except KeyError as e:
        print(e)
        return None, None

def sign_in():
    try:
        global usernam, tkn, passw
        while not(usernam.isalnum()):
            usernam=input(" Enter Username: ").strip()
        while not(passw.isalnum()):
            passw=input(" Enter Your Password: ").strip()

        body2= {
            "username": usernam,
            "password": passw
        }
        g= requests.post(url+"/auth/signin", json=body2)
        sap=g.json()
        tkn = sap["token"]
        print("Sign In Successful 💖")
        return tkn, usernam
    except KeyError as e:
        print(e)
        return None, None


def post_quote(tkn,usernam):
    quote=str(input("Enter Your Quote: "))

    body3={
        "quote": quote,
        "author": usernam
    }

    autho={
        "authorization": tkn
    }
    dat=requests.post(url+"/quotes/post", json= body3, headers= autho)
    p=dat.json()
    id1=p["id"]
    return id1, usernam, quote

def store_id(id1,author,quote):
    with open("ids.txt", "a") as f:
        f.write(f"{author}:{id1}:{quote}\n")

def delete_quote(author):
    author_quotes=[]
    ids=[]
    try:
        with open("ids.txt", 'r') as o:
            lines=o.readlines()
            for line in lines:
                splice=line.split(":", 2)
                if splice[0]==author:
                    author_quotes.append(splice[2])
                    ids.append(splice[1])
        print()
        print("Select Quote Number To Delete: ")

        for jl in range(len(author_quotes)):
            print(f" {jl}. {author_quotes[jl]}")

        choice=len(author_quotes)+2
        if len(author_quotes)==0:
            print()
            print("No Quotes By You")
            return

        while not(choice in range(len(author_quotes))):
                choice=int(input())
                if not(choice in range(len(author_quotes))):
                    print("Select A Valid Quote Number: ")
        chosen_quote=ids[choice]

        jim= requests.delete(url+f"/quotes/{chosen_quote}")

        if jim.status_code>=400:
            print(jim.text)
        else:
            print("Quote Successfully Deleted 👍")

        with open("ids.txt", "w") as f:
            for line in lines:
                splice = line.split(":", 2)
                if splice[1] != chosen_quote:
                    f.write(line)
    except FileNotFoundError:
        print()
        print("No Quotes Stored")

def show_all_quotes():
    d=requests.get(url+"/quotes/all")
    quotes1=d.json()
    k=quotes1["quotes"]
    c=1 
    print()
    for k1 in k:
        print(f" {c}.{k1["quote"]}")
        c+=1
    print()

def quotes_username():
    na=input("Enter The Name Of The Author: ")
    mn=requests.get(url+f"/quotes/{na}")
    fl=mn.json()
    fla=fl["quotes"]
    print("Quotes From The Author: ")
    for fin in fla:
        print(f"{fin['quote']}\n")


def main():
    global choice
    print(" Nga What Do You Wanna Do? \n Options:")
    print(" 1.Create New User \n 2.Sign In Already Existing User \n 3.Guest Login")
    print("Enter Your Choice: 1, 2 or 3")
    
    while choice not in [1,2,3]:  #Better way is using try and except
        choice=input()
        if choice.isdigit():
            choice=int(choice)
            if choice not in [1,2,3]:
                print("Wrong Input, Enter 1, 2 or 3")
        else:
            print("Enter A Valid Integer")
    
    if choice in [1,2]:
        if choice==1:
            tok, us=sign_up()

        if choice==2:
            tok, us= sign_in()

        while True:
            print("What Do You Want To Do Next Nga? \n Options:")
            print(" 1.Exit \n 2.Enter A Quote \n 3.Delete A Quote \n 4.Show All Quotes \n 5.Show Quotes Of A Specific Author")

            choice=99

            while choice not in [1,2,3,4,5]:   #Can use dict of functions when the number of choices are very large
                choice=input()
                if choice.isdigit():
                    choice=int(choice)
                    if choice not in [1,2,3,4,5]:
                        print("Wrong Input, Enter from the choices given above")
                else:
                    print("Enter A Valid Integer")

            if choice == 1:
                print("Bye Bye ✌️")
                exit()
            elif choice == 2:
                id6,aut,quo=post_quote(tok,us)
                store_id(id6,aut,quo)
            elif choice == 3:
                delete_quote(us)
            elif choice == 4:
                show_all_quotes()
            elif choice == 5:
                quotes_username()

    if choice==3:
        while True:
            print("What Do You Want To Do Next Nga? \n Options:")
            print(" 1.Exit \n 2.Show All Quotes \n 3.Show Quotes Of A Specific Author")

            choice=99

            while choice not in [1,2,3]:   #Can use dict of functions when the number of choices are very large
                choice=input()
                if choice.isdigit():
                    choice=int(choice)
                    if choice not in [1,2,3]:
                        print("Wrong Input, Enter from the choices given above")
                else:
                    print("Enter A Valid Integer")

            if choice == 1:
                print("Bye Bye ✌️")
                exit()
            elif choice == 2:
                show_all_quotes()
            elif choice == 3:
                quotes_username()


if __name__ == "__main__":
    main()