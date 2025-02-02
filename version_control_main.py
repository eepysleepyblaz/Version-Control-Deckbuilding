
#Imports
#Imports the control.py file for its functionality
from control import Version_Control

#For repo access
import os

#To check methods parameter sizes
import inspect

#To allow clipboard access
from tkinter import Tk

#Grants functionality for the user to use the methods of control
class Ui():

    def __init__(self):
        #Defines the command list
        self.command_dict = {'cr': self.create_repo,
         'lr': self.list_repo,
         'commit': self.commit_deck,
         'pull': self.pull_deck,
         'show': self.show_deck,
         'mkrepo':self.create_repo}
        
    #Parses user commands and trys to run it
    def parse(self, command):
        try:
            command = command.split(" ")
        except:
            return "Empty commands are invalid"
        
        if command[0] not in list(self.command_dict.keys()):
            return "Invalid command"
        
        #If an input if missing some values that have defulat values added them
        sig = inspect.signature(self.command_dict[command[0]])
        extra = 0
        for name, param in sig.parameters.items():
            if name == "args":
                extra += 1

        #Checks the number of paramters is correct
        if len(inspect.signature(self.command_dict[command[0]]).parameters) > len(command[1:]) + extra:
            return f"{command[0]} takes {len(inspect.signature(self.command_dict[command[0]]).parameters) - extra} required parameters. You provided {len(command[1:])}"

        #Checks if the repo exists and if the command isn't to make that repository
        if command[1] not in self.list_repo() and command[0] != "mkrepo":
            return "That repository does not exists"

        #Trys to run the command
        try:
            return self.command_dict[command[0]](*command[1:])
        except:
            return "Command failed. Bad arguments."
    

    #Lets the user creates new repository for deck lists
    def create_repo(self, name):
        if name not in self.list_repo():
            temp = Version_Control(name)

        
    #Lists the existing repos
    def list_repo(self):
        repos = os.listdir(os.path.join(os.path.dirname(__file__), 'decks'))
        repos = [x for x in repos if x[0] != '.']
        return repos
    
    #Lets the user commit to a repo they have created
    def commit_deck(self, name, path):
        temp = Version_Control(name)
        temp.commit(path)

    #Pulls the most recent or a specific version of a deck
    def pull_deck(self, name, *args):
        temp = Version_Control(name)

        #Handling the extra arguments
        #Checks if a version of the deck has been provided
        version = None
        print(temp.list())
        for arg in args:
            if arg + ".txt" in temp.list():
                version = arg

        deck = temp.get(version)

        #Checks if the user wants the deck list copied to the deck list
        if "-c" in args or "-C" in args:
            t = Tk()
            t.withdraw()
            t.clipboard_clear()
            t.clipboard_append(deck[1])

        return "\n".join(deck)

    #Opens a visual display of a deck
    def show_deck(self, name, deckname=None):
        temp = Version_Control(name)

        #If the deckname is nothing use the most recent deck
        if deckname == None:
            deckname = temp.most_recent()
        else:
            deckname = deckname + ".txt"

        temp.webshow(deckname)
    
    #Makes a repository of a given name for decks
    def create_repository(self, name):
        temp = Version_Control(name)
        
        temp.make_repo()

#Main body of the program
exit = False
interface = Ui()

print("Version conroled deck building ready...")

#Main loop
while not exit:
    user_input = input("|>>->")
    result = interface.parse(user_input)

    #Prints a result to the screen if it needs printing
    if result != None:
        if type(result ) == list:
            result = ", ".join(result)

        print(result)
    
    

