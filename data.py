#!/usr/bin/env python
import wget
import os
import json
import pystyle
import winreg
from tkinter import filedialog
from configparser import ConfigParser
from PIL import Image
from customtkinter import *

config = ConfigParser()

def get_reg(name,REG_PATH):
    try:
        registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_PATH, 0,
                                       winreg.KEY_READ)
        value, regtype = winreg.QueryValueEx(registry_key, name)
        winreg.CloseKey(registry_key)
        return value
    except WindowsError:
        return None

def set_reg(name, REG_PATH, val):
    try:
        regkey = winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_PATH, 0, winreg.KEY_ALL_ACCESS)
        registry_key = winreg.SetValueEx(regkey, name, 0, winreg.REG_DWORD, val)
        winreg.CloseKey(regkey)
        print(f"{registry_key=}")
        return registry_key
    except WindowsError:
        return None

class Framework:
    def __init__(self, Theme : str, title : str) -> None:
        self.Theme = Theme
        self.title = title
    def Menu(self):
        f = open("config.json")
        data = json.loads(f.read())
        f.close()
        Games = data["Games"]
        AppId = data["AppId"]
        set_default_color_theme(self.Theme)
        root = CTk()
        root.title(self.title)
        root.geometry("500x400")
        Frame = CTkScrollableFrame(root,width=350,height=250,corner_radius=25,orientation="vertical")
        Frame.pack(pady=15)
        CurPath = os.getcwd()
        count = -1

        for i in Games:
            count += 1
            if not os.path.exists("icons"):
                os.mkdir("icons")
            os.chdir("icons")
            try:
                if not os.path.exists("custom.png"):
                    wget.download("https://areajugones.sport.es/wp-content/uploads/2015/01/Steam-OS-Planet-Steam-Logo-780x440.jpg",out="custom.png")
                if not os.path.exists(str(i).replace(":","").replace(",","")+".jpg"):
                    i2 = str(i).replace(":","").replace(",","")
                    wget.download("https://steamcdn-a.akamaihd.net/steam/apps/"+str(AppId[count])+"/header.jpg",out=str(i2)+".jpg")
            except: pass

            print("Game = ",i+"\nId = ",AppId[count])
            File = str(i).replace(":","").replace(",","")+".jpg"
            try: 
                Img = Image.open(File)
                Img.save(File,"JPEG", quality=88)
                Img.close()
                Img = Image.open(File)
            except: 
                Img = Image.open("custom.png")
                Img.save(File,"JPEG", quality=100)

            def Start(Id):
                Run = "steam://rungameid/"
                os.system("start "+Run+Id)
            Img = CTkImage(Img,size=[120,80])
            image = CTkLabel(Frame, text="", width=100,height=100,image=Img)
            image.grid(row=count,column=0,padx=5,pady=5)
            Btn = CTkButton(Frame,text="Start",command= lambda: Start(str(AppId[count])))
            Text = CTkLabel(Frame,text=i)
            Text.grid(row=count, column=2)
            Btn.grid(row=count,column=2)
            os.chdir(CurPath)

        root.mainloop()
    def print(self, other : str | list):
        if other != str:
            print(str(other).replace("[","").replace("]","").replace("\'","").replace(",",""))
        else:
            print(other)

class SystemConsole:
    def __init__(self, title : str | None = "Main", close : bool | None = False, **kwargs) -> None:
        kwargs.setdefault("color","0f")
        color = kwargs.get("color")
        self.color = color
        self.title = title
        self.close = close
        os.system("cls")
    def Main(self):
        while self.close == True:
            sys.exit(0)
        def Library(Games : list) -> None:
            os.system("color "+self.color); os.system("cls")
            print("\n---LIBRARY---")
            count = -1
            config.read("configs.ini")
            if config.has_section("ExtraGames"):
                for i in config.items("ExtraGames"):
                        if not Games.__contains__(i[0]):
                            Games.append(str(i[0]).replace("_"," "))
            count = -1
            for i in Games:
                if count == -1: print()
                count += 1
                print(str(count)+" "+i)
            print()
            os.system("pause")
            os.system("cls")
            SystemConsole.Main(self)
        def Add() -> None:
            os.system("cls & color "+self.color)
            print("\n---ADD-INFO---")
            print("Here you can add custom games who are\nnot in the library !")
            print()
            pystyle.Write.Print("Press enter to start !",pystyle.Colors.green_to_cyan,interval=0.0025)
            os.system("pause > nul")
            print(pystyle.Colors.green+"\nSelect the .exe file to add it !"+pystyle.Colors.reset)
            path = filedialog.askopenfilename(title="Select Exe File",filetypes=[("File .exe")])

            if path == "" or path == " ":
                os.system("cls")
                SystemConsole.Main(self)
            else:
                print()
                print(pystyle.Colors.blue+"Wich name should it have?"+pystyle.Colors.reset)
                I = pystyle.Write.Input("Name -> ",pystyle.Colors.green_to_cyan,interval=0.025)
                if I != None or I != " " or I != "":
                    config.read("configs.ini")
                    if not config.has_section("ExtraGames") == True: config.add_section("ExtraGames")
                    config.set("ExtraGames",I.replace(" ","_"),path)
                    with open("configs.ini","w") as f:
                        config.write(f)
                        f.close()
            os.system("cls")
            SystemConsole.Main(self)
        def Configurations() -> None:
            os.system("cls & color "+self.color)
            print("\n---CONFIGURATIONS---")
            print("\n1. Set Auto-Login (temporary) !")
            print("2. Set Gui mode (BETA) DO NOT USE")
            print("E. Go Back\n")
            I = pystyle.Write.Input("Number -> ",pystyle.Colors.green_to_cyan,interval=0.025)
            if I == "1":
                os.system("reg delete HKCU\SOFTWARE\Valve\Steam /v RememberPassword /f")
                os.system("reg add HKCU\SOFTWARE\Valve\Steam /v RememberPassword /d 1 /t REG_DWORD /f")
            elif I == "2":
                config.read("configs.ini")
                config.set("Mode","GuiMode","True")
                with open("configs.ini","w") as c:
                    config.write(c)
                os.startfile("NoConsole.py")
                os._exit(0)
            elif (I == "E") or (I == "Go Back"):
                os.system("cls")
                SystemConsole.Main(self)
            Configurations()
        def Delete(Games : list) -> None:
            os.system("cls & color "+self.color)
            print("\n---DELETE---")
            Game = []

            config.read("configs.ini")
            
            if config.has_section("ExtraGames") and (len(config.items("ExtraGames")) == 0): config.remove_section("ExtraGames"); f = open("configs.ini","w"); config.write(f); f.close()
            count = -1
            if config.has_section("ExtraGames"):
                for i in config.items("ExtraGames"):
                    Game.append(str(i[0]).replace("_"," "))
                    if count == -1: print()
                    count += 1
                    print(str(count)+" "+str(i[0]).replace("_"," "))
            else: print(pystyle.Colors.red+"No Custom Games were found !"+pystyle.Colors.reset)

            print(pystyle.Colors.green+str(len(Games))+" Go Back\n"+pystyle.Colors.reset)
            I = pystyle.Write.Input("Number : ",pystyle.Colors.blue_to_cyan,interval=0)
            try: 
                if int(I) == len(Games): os.system("cls"); SystemConsole.Main(self)
            except: pass
            config.read("configs.ini")
            try: CurrentGame = Game[int(I)] 
            except: print(pystyle.Colors.red+"\nIt should be numeric !"+pystyle.Colors.reset); print(); os.system("pause"); CurrentGame = None
            if CurrentGame == None:
                Delete(Games)
            CurrentGame = str(CurrentGame).lower().replace(" ","_").replace(":","").replace("+","").replace(",","")
            CurrentGame = config.remove_option("ExtraGames",CurrentGame)
            with open("configs.ini","w") as f:
                config.write(f)
            Delete(Games)
        def StartGames(Games : list):
            os.system("color "+self.color); os.system("cls")
            print("\n---GAMES TO START---")
            Game = []
            config.read("configs.ini")
            if config.has_section("ExtraGames"):
                for i in config.items("ExtraGames"):
                        if not Games.__contains__(str(i[0]).replace("_"," ")):
                            Games.append(str(i[0]).replace("_"," "))
            count = -1
            for i in Games:
                if count == -1: print()
                count += 1
                print(str(count)+" "+i)
                Game.append(i)
            print(str(len(Game))+" Go Back\n")
            I = pystyle.Write.Input("Number : ",pystyle.Colors.blue_to_cyan,interval=0)
            try: 
                if int(I) == len(Game): os.system("cls"); SystemConsole.Main(self)
            except: pass
            config.read("configs.ini")
            if (I != "") or (I != " "):
                try: CurrentGame = Game[int(I)] 
                except: print(pystyle.Colors.red+"\nIt should be numeric !"+pystyle.Colors.reset); print(); os.system("pause"); CurrentGame = None
            else:
                CurrentGame = None
            if CurrentGame == None:
                StartGames(Games)
            CurrentGame = str(CurrentGame).lower().replace(" ","_").replace(":","").replace("+","").replace(",","")+"_path"
            try: CurrentGame = config.get("ExtraGames",CurrentGame.replace("_path",""))
            except: CurrentGame = config.get("GamePath",CurrentGame)
            try:
                os.startfile(CurrentGame)
            except Exception as E:
                print()
                print(pystyle.Colors.red+str(E)+pystyle.Colors.reset)
                print()
                os.system("pause")
            StartGames(Games)
            SystemConsole.Main(self)
        os.system("title "+self.title); os.system("color "+self.color)
        print("\n---LAUNCHER---")
        print("\n1. Library")
        print("2. Start Game")
        print("3. Add Games")
        print("4. Delete Games")
        print("5. Configure\n")
        I = pystyle.Write.Input("Number -> ",pystyle.Colors.green_to_blue,interval=0.025)
        if I == "1":
            if os.path.exists("config.json"):
                try: f = open("config.json","r"); data = json.loads(f.read()); f.close()
                except: print("ERROR"); os.system("pause") 
                Library(data["Games"])
            else:
                print()
                pystyle.Write.Print("ERROR : 1C0\nRestart the program ! Or Press enter",pystyle.Colors.red, interval=0); print("\n"); os.system("pause")
        elif I == "2":
            if os.path.exists("config.json"):
                try: f = open("config.json","r"); data = json.loads(f.read()); f.close()
                except: print("ERROR"); os.system("pause") 
                StartGames(data["Games"])
            else:
                print()
                pystyle.Write.Print("ERROR : 1C0\nRestart the program ! Or Press enter",pystyle.Colors.red, interval=0); print("\n"); os.system("pause")
        elif I == "3":
            Add()
        elif I == "4":
            try: f = open("config.json","r"); data = json.loads(f.read()); f.close()
            except: print("ERROR"); os.system("pause") 
            Delete(data["Games"])
        elif I == "5":
            Configurations()
        else:
            os.system("cls")
            SystemConsole.Main(self)