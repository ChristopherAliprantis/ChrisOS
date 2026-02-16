import json 
import platform
import os
import re
from datetime import datetime
import random

def date():
    now = datetime.now()
    return now.strftime("%Y-%m-%d")

time = 1
TLF = 10000
lines_taken = 0
vers = 'ChrisOS™ 2'
files = {}
dirlist = ['Tic-Tac-Toe.pre',]
filelist = []
templist = []
history = []
var = None


def usage():
    system_type = platform.system()

    if system_type == 'Windows':
        output = os.popen("wmic cpu get loadpercentage").read()
        match = re.search(r'\d+', output)
        if match:
            return f"{match.group()}%"
        else:
            return "Error parsing CPU usage(maybe try again)"

    elif system_type == 'Linux':
        output = os.popen("top -bn1 | grep 'Cpu(s)'").read()
        match = re.search(r'(\d+\.\d+)\s*id', output)
        if match:
            idle = float(match.group(1))
            usage_percent = 100 - idle
            return f"{int(usage_percent)}%"
        else:
            return "Error parsing CPU usage(maybe try again)"

    else:
        return f'Cannot search {system_type} for CPU stats'

class TTT:
    def __init__(self):
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.player_won = False
        self.bot_won = False

    def print_board(self):
        for row in self.board:
            print(row)

    def win_check(self, token):
        b = self.board
        return (
            any(all(cell == token for cell in row) for row in b) or
            any(all(b[r][c] == token for r in range(3)) for c in range(3)) or
            all(b[i][i] == token for i in range(3)) or
            all(b[i][2 - i] == token for i in range(3))
        )

    def is_draw(self):
        return all(cell in ['X', 'O'] for row in self.board for cell in row)

    def bot_turn(self):
        while True:
            row, col = random.randint(0, 2), random.randint(0, 2)
            if self.board[row][col] == ' ':
                self.board[row][col] = 'O'
                self.bot_won = self.win_check('O')
                break

    def player_turn(self):
        while True:
            self.print_board()
            try:
                row = int(input("Row (1-3): ")) - 1
                col = int(input("Column (1-3): ")) - 1
                if not (0 <= row < 3 and 0 <= col < 3):
                    print("Invalid input. Try again.")
                    continue
                if self.board[row][col] != ' ':
                    print("Occupied. Try again.")
                    continue
                self.board[row][col] = 'X'
                self.player_won = self.win_check('X')
                break
            except ValueError:
                print("Invalid input. Try again.")

    def start(self):
        print("You're X, the bot is O. Rows go top to bottom, columns left to right.")
        while not self.player_won and not self.bot_won:
            self.player_turn()
            if self.player_won:
                print("You won!")
                break
            if self.is_draw():
                print("It's a draw!")
                break
            self.bot_turn()
            if self.bot_won:
                print("The bot won!")
                break
            if self.is_draw():
                print("It's a draw!")
                break
        self.print_board()

def new(nam):
    global lines_taken
    print("make a line with 'F{stopwr}' then press enter to stop")
    templines = 0
    templist = []
    while True:
        ln = input('ln> ')
        if ln == 'F{stopwr}':
            break
        templist.append(ln)
        templines += 1
    print()
    if lines_taken + templines > TLF:
        excess = (lines_taken + templines) - TLF
        print(f'Error: adding {templines} lines exceeds limit by {excess} lines; file cannot be stored.')
        return
    nm = nam
    if f'{nm}' in filelist:
        print(f'the name \'{nm}\' is already taken')
        return ''
    if not templist:
        templist = [''] 
    return (templist, templines, nm)
    

def save_to_disk(check, skip):
    global var  
    if skip == False or var == True:       
        try:
            with open("chrisos2_mem.json", "w") as f:
                json.dump({
                    "files": files,
                    "filelist": filelist,
                    "dirlist": dirlist,
                    "lines_taken": lines_taken,
                    "time": time,
                }, f)
                if check:
                    return True
        except:
            print('memory storer not found! ChrisOS: data: unsaved')
            if check:
                return False
    else: 
        if var == False:
            return

def load_from_disk(end):
    global files, filelist, dirlist, lines_taken, time
    with open("chrisos2_mem.json", "r") as f:
        data = json.load(f)
        files = data.get("files", {})
        filelist = data.get("filelist", [])
        dirlist = data.get("dirlist", ["Tic-Tac-Toe.pre"])
        if 'Tic-Tac-Toe.pre' not in dirlist:
            dirlist.insert(0, 'Tic-Tac-Toe.pre')
        lines_taken = data.get("lines_taken", 0)
        time = data.get("time", 1)
        if end == 'y':
            print('ChrisOS: data: loaded')

def rename():
    global filelist, dirlist, files, command
    try:
        old = None
        new = None
        for fname in filelist:
            if command.startswith(f'rename {fname} as '):
                old = fname
                break
        if old is None:
            print('file not found')
            return
        new = command[len(f'rename {old} as '):].strip()
        if new.endswith((".im", ".txt")) == False:
            print("need '.txt' or '.im' in replacement name; renaming cannot be done")
            return
        for i in range(len(filelist)):
            if filelist[i].strip() == old.strip():
                filelist[i] = new
        for i in range(len(dirlist)):
            if dirlist[i].strip() == old.strip():
                dirlist[i] = new
        if old in files:
            files[new] = files[old]
            del files[old]
        if f'{old}.lines' in files:
            files[f'{new}.lines'] = files[f'{old}.lines']
            del files[f'{old}.lines']
        save_to_disk(False, True)
        print(f"renamed '{old}' to '{new}'")
    except:
        print(f'could not rename {old}')

def check():   
    if '(' in command or ')' in command: 
        print(f'Command \'{command}\' not found! Enter \'help\' to see the commands. or try removing parentheses')
        return
    else:
         if command == '': 
            return
         else: 
             print(f'Command \'{command}\' not found! Enter \'help\' to see the commands.')
             return
try:
    load_from_disk('n')
    var = True
except:
    files, filelist, dirlist, lines_taken, time = {}, [], ['Tic-Tac-Toe.pre'], 0, 1
    var = save_to_disk(True, False)

if var:
    load_from_disk('y')
time += 1
save_to_disk(False, True)
history = []
command = ''
while True:
    if var == False:
        print()
        print('reminder: no memory storer; changes like managing files can be made,\nbut next time you boot up the computer,\neverything will have reset,\ntry connecting an, HDD, SSD, or some portable storage device like SD or USB drive to the computer\nbut you will need to close the computer and turn it on again to save\nChrisOS: data: unsaved')
        print()
    if command != '':
            history.append(command)
    
    command = input('>> ').strip()
    if command == '+':
        try:
            num1 = float(input('num1 >> '))
            num2 = float(input('num2 >> '))
            print(f'= {num1 + num2}')
        except:
            print('invalid input')
    elif command == '*':
        try:
            num1 = float(input('num1 >> '))
            num2 = float(input('num2 >> '))
            print(f'= {num1 * num2}')
        except: 
            print('invalid input')
    elif command == '-':
        try:
            num1 = float(input('num1 >> '))
            num2 = float(input('num2 >> '))
            print(f'= {num1 - num2}')
        except:
            print('invalid input')
    elif command == '/':
        try:
            num1 = float(input('num1 >> '))
            num2 = float(input('num2 >> '))
            if num2 == 0:
                print('Can\'t do division by 0s!')
                continue
            print(f'= {num1 / num2}')
        except:
            print('invalid input')
    elif command == '^':
        try:
            num1 = float(input('num1 >> '))
            num2 = float(input('num2 >> '))
            print(f'= {num1 ** num2}')
        except:
            print('invalid input')
    elif command.startswith('new '):
        if (command[4:].endswith(".im")) or command[4:].endswith(".txt"):
            name = new(command[4:].lstrip())
            if name != '':
                templist, templines, nm = name
                lines_taken += templines
                files[f'{nm}'] = templist.copy()
                files[f'{nm}.lines'] = templines
                dirlist.append(f'{nm}')
                filelist.append(f'{nm}')
                save_to_disk(False, True)
                print(f'created {command[4:]}')
        else:
            print("file type not found!")
    elif command == 'dir' or command == 'ls':
        print(dirlist)
    elif command.startswith('read '):
        nme = command[5:].strip()
        if nme.endswith(".txt"):    
            content = files.get(nme)
            if content is not None:
                if isinstance(content, list):
                    print('\n'.join(content))
                else:
                    print(content)
            else:
                print('Name not found!')
        elif nme.endswith('im'):
            content = files.get(nme)
            if content is None:
                print('Name not found!')
                continue
            ncontent = []
            for i in range (len(content)):
                ncontent.append('')
            for i in range(len(content)):
                for j in range(len(content[i])):
                    th = content[i][j]
                    place = ncontent[i]
                    if th == 'R': place += "🟥"
                    elif th == 'O': place += '🟧'
                    elif th == 'Y': place += '🟨'
                    elif th == 'G': place += '🟩'
                    elif th == 'D': place += '🟦'
                    elif th == 'P': place += '🟪'
                    elif th == 'b': place += '🟫'
                    elif th == "B": place += '⬛'
                    elif th == "W": place += '⬜'
                    elif th == ' ': place += ' '
                    else:
                        print('problem reading image!')
                        ncontent.clear()
                        continue
                    ncontent[i] = place
            if isinstance(content, list):
                print('\n'.join(ncontent))
            else:
                print(ncontent)
        else:
            print('file type not found!')
    elif command == 'version':
        print(vers)
    elif command == 'files':
        print(filelist)
    elif command.startswith('delete '):
        nme = command[7:] 
        if nme in files:
            confirm = input(f'Are you sure you want to delete \'{nme}\'? (y/n)>> ').lower()
            if confirm == 'y':
                lines_taken -= files[f"{nme}.lines"]
                del files[nme]
                files.pop(f"{nme}.lines", None)
                for i in range(len(filelist)):
                    if filelist[i] == nme:
                        del filelist[i]
                        break
                for i in range(len(dirlist)): 
                    if dirlist[i] == nme:
                        del dirlist[i]
                        break
                save_to_disk(False, True)
                print(f'deleted {nme}')
            elif confirm == 'n':
                print('Deletion canceled.')
            else:
                print('invalid answer')
        else:
            print('Name not found!')
    elif command == 'help':
        print('+ : addition\n- : subtraction\n* : multiplication\n/ : division\n^ : power\nnew (file name) : make an initial new file(you can use the edit command to modify it)\nread (name file you want to read): reads a file\nversion : OS version\ndelete (name of thing you want to delete) : deletes a file\nfiles : view file names\ndir or ls : see the directory\nexit : shut down the computer\nhelp : shows commands and their actions\ndate : shows the date\ndata : shows the total amount of lines in files\nboots : shows how many times the system has been booted\nformats : shows formats that are used in the sytem\nhistory : shows command history(on the main prompt not like in applications) of the session\ncodes : gives you color codes for image editor\nCPUse : shows CPU usage percentage\nPrun (name of what ever pre you want to run) : runs applications with \'.pre\' ending\npres : displays .pre programs\nrename (name of file you want to rename) as (name you want to rename it to) : renames files\n(file name) : says if it\'s a file or not\nedit : edits a file\ncopy (file name) : copies  a file\nChrisOS: data: : shows state of memory')
    elif command == 'codes':
        print('R : red\nO : orange\nY : yellow\nG : green\nD : blue\nP : purple\nb : brown\nB : black\nW : white')
        print("hint: when you are making a new image file, if you want one row to have red color, red color, then black, type RRB, also you can put spaces in it")
    elif command == 'date':  
        print(date())
    elif command == 'data':
        print(f'{lines_taken}/{TLF} lines taken')
    elif command == 'boots':
        print(f'system has been booted {time - 1} times')
    elif command == 'formats':
        print('.txt : text file\n.pre : preinstalled application\n.im : image file')
    elif command == 'pres':
        print('Tic-Tac-Toe.pre')
    elif command == 'CPUse':
        var = usage()
        print(var)
    elif command == 'history':
        print(history)
    elif command == 'Prun Tic-Tac-Toe.pre':
        print()
        game = TTT()
        game.start()
        print()
    elif command.startswith('copy '):
        if command[5:] in filelist:
            new = f'copy of {command[5:].strip()}'
            old = command[5:].strip()
            dirlist.append(new)
            filelist.append(new)
            files[new] = files[old]
            files[f'{new}.lines'] = files[f'{old}.lines']
            print(f'copied {old}')
        else:
            print('file to copy not found')
    elif command.startswith('rename '):
        rename()
    elif command == 'ChrisOS: data:':
        if var == True:
            print('loaded')
        else:
            print('unsaved')
    elif command == 'exit':
        save_to_disk(False, True)
        break
    elif command.startswith('edit '):       
        if (command[5:].endswith(".txt") or command[5:].endswith(".im")): 
            try:
                file = files[command[5:]]            
                filename = command[5:]
                while True: 
                    print('add, to add line, edit to edit line, delete to delete line, exit to exit program:')
                    op = input()
                    if op == 'add':
                        ln = input('ln> ')
                        file.append(ln)
                    elif op == 'edit':
                    
                        for i in range(len(file)):
                            print(f'{i+1}: {file[i]}')
                        try:
                            line = int(input('line num: ')) - 1
                            print(f'replace {file[line]} with:')
                            nl = input('ln> ')
                            file[line] = nl
                        except:
                            print('line does not exist!')
                    elif op == 'delete':
                        for i in range(len(file)):
                            print(f'{i+1}: {file[i]}')
                        try:
                            line = int(input('line num: ')) - 1
                            del file[line]
                        except:
                            print('line does not exist!')            
                    elif op == 'exit':
                        print(f'{filename} edited')
                        lines_taken -= files[f'{filename}.lines']
                        files[f'{filename}.lines'] = len(file)
                        lines_taken += files[f'{filename}.lines']
                        files[filename] = file
                        save_to_disk(False, True)  
                        break
                    else:
                        print('invalid input!')
            except:
                print('name not found!')
            save_to_disk(False, True)
        else:
            print('file type not found!')
    elif command.startswith('rename') == False:
        if command.endswith('.txt'):
            if command in filelist:
                print(f'{command} is a file')
                continue
            else:
                print(f'{command} is not a file')
                continue
        else:
            check()
            continue
    else:
        check()



exit()  