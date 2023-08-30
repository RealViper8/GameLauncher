#!/usr/bin/env python
import os, fnmatch
import json
from data import SystemConsole
from data import Framework
import winreg
import configparser

config = configparser.ConfigParser()

def find(pattern, path):
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
    return result

def get_reg(name,REG_PATH):
    try:
        registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_PATH, 0,
                                       winreg.KEY_READ)
        value, regtype = winreg.QueryValueEx(registry_key, name)
        winreg.CloseKey(registry_key)
        return value
    except WindowsError:
        return None

def main(GuiMode : bool):
    if (GuiMode == True):
        rt = Framework("dark-blue","Main")
        rt.Menu()
    elif (GuiMode == False):
        os.system("color 0a")
        Console = SystemConsole()
        Console.title = "Menu"
        Console.color = "0a"
        root = Console.Main()
    else:
        print("\nPlease open config.josn and set GuiMode to False And ConsoleMode to True")

def write_json(new_data, filename='config.json'):
    with open(filename,'r+') as file:
        file_data = json.load(file)
        file_data["GamePath"].append(new_data)
        file.seek(0)
        json.dump(file_data, file, indent = 4)


if __name__ == "__main__":
    os.chdir(os.getcwd())
    if os.path.exists("config.json"):
        try:
            f = open("config.json","r")
            data = json.loads(f.read())
            Path = get_reg("SteamPath","SOFTWARE\\Valve\Steam")
        
            result = find('*.acf', Path+"/steamapps")
            name = []
            for i in result:
                if str(i).__contains__("workshop") or str(i).__contains__("temp") or str(i).__contains__("workshop"):
                    result.remove(i)
                else:
                    i = open(i,"r")
                    Lines = i.readlines()
                    for line in Lines:
                        if line.__contains__("name"):
                            result1 = line.replace("name","").replace("\"","").replace("\t","").replace("\n","")
                            if result1 == "Garry's Mod":
                                result1 = "GarrysMod"
                            if not result1.__contains__("Redistributables"):
                                name.append(result1)
                            name1 = str(name).replace("\'","\"")
                        elif line.__contains__("installdir"):
                            resultp = line.replace("installdir","").replace("\"","").replace("\t","").replace("\n","")
                            GamePath = result1.replace(" ","_").replace(":","").replace(",","")+"_Path"
                            game_p = find('*.exe',Path+"/steamapps/common/"+resultp)

                            if os.path.exists("configs.ini"): config.read("configs.ini")
                            if not config.has_section("GamePath") == True: config.add_section("GamePath")

                            if os.path.exists(Path+"/steamapps/common/"+resultp+"/Release"):   
                                config.set("GamePath",str(GamePath),str(game_p[1]))
                            else:
                                config.set("GamePath",str(GamePath),str(game_p[0]))
                            with open("configs.ini","w") as f:
                                config.write(f)
                                f.close()
                    if not config.has_section("Mode"): config.add_section("Mode")
                    if not config.has_option("Mode","GuiMode"): config.set("Mode","GuiMode","False")
        except:
            data = None
        Mode = config.get("Mode","GuiMode")
        if (Mode == "True"):
            main(GuiMode=True)
        elif (Mode == "False"):
            main(GuiMode=False)
        elif (data == None):
            print("Please delete the config.json, config.ini and restart the program !")
    else:
        try:
            Path = get_reg("SteamPath","SOFTWARE\\Valve\Steam")
            
            result = find('*.acf', Path+"/steamapps")
            name = []
            AppId = []
            for i in result:
                if str(i).__contains__("workshop") or str(i).__contains__("temp") or str(i).__contains__("workshop"):
                    result.remove(i)
                else:
                    file = str(i).replace(Path,"").replace("steamapps","").replace("/","").replace("\\","")
                    Id = file.replace("appmanifest_","").replace(".acf","")
                    if Id != "228980":
                        AppId.append(Id)
                    i = open(i,"r")
                    Lines = i.readlines()
                    for line in Lines:
                        if line.__contains__("name"):
                            result1 = line.replace("name","").replace("\"","").replace("\t","").replace("\n","")
                            if result1 == "Garry's Mod":
                                result1 = "Garrys Mod"
                            if not result1.__contains__("Redistributables"):
                                name.append(result1)
                            name1 = str(name).replace("\'","\"")
                        elif line.__contains__("installdir"):
                            resultp = line.replace("installdir","").replace("\"","").replace("\t","").replace("\n","")
                            GamePath = result1.replace(" ","_").replace(":","").replace("+","").replace(",","")+"_Path"
                            game_p = find('*.exe',Path+"/steamapps/common/"+resultp)
                            if os.path.exists("configs.ini"): config.read("configs.ini")
                            if not config.has_section("GamePath") == True:
                                config.add_section("GamePath")
                            if os.path.exists(Path+"/steamapps/common/"+resultp+"Release"):    
                                config.set("GamePath",str(GamePath),str(game_p[1]))
                            else:
                                config.set("GamePath",str(GamePath),str(game_p[0]))
                            with open("configs.ini","w") as f:
                                config.write(f)
                    if not config.has_section("Mode"): config.add_section("Mode")
                    if not config.has_option("Mode","GuiMode"): config.set("Mode","GuiMode","False")
            f = open("config.json","w")
            f.writelines("{"+f"""
    \"Games\" : {name1},
    \"AppId\" : {str(AppId).replace("'","")}"""
    "\n}")
            f.close()
            f = open("config.json","r")
            data = json.loads(f.read())
            f.close()
        except:
            data = None
        Mode = config.get("Mode","GuiMode")
        if data != None:
            if (Mode == "True"):
                f.close()
                main(GuiMode=True)
            elif (Mode == "False"):
                f.close()
                main(GuiMode=False)
        else:
            print("Something unexpected happend make sure to use windows or try a package if you dont have windows !")