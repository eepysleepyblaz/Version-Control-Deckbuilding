
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
         'mkrepo':self.create_repo,
         'cr': self.enter_repo,
         'exr': self.exit_repo}
        
        #Saves the repository that is currently open
        self.current_repo = None
        
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

        #Checks if the user is currently in a repo
        #Ignored if the user is listing, creating a repo, or entering a repo
        if self.current_repo == None and not (command[0] == "mkrepo" or command[0] == "cr", command[0] == "lr"):
            return "Not in a repository"

        #Trys to run the command
        try:
            return self.command_dict[command[0]](*command[1:])
        except:
            return "Command failed. Bad arguments."
    

    #Lets the user creates new repository for deck lists and then can enter that repo
    def create_repo(self, name, *args):
        if name not in self.list_repo():
            temp = Version_Control(name)
            temp.make_repo()

        #Checks for extra aruments
        #Checks if the user wants to enter that repo too
        if "-e" in args or "-E" in args:
            self.enter_repo(name)
        
    #Lists the existing repos
    def list_repo(self):
        if self.current_repo == None:
            repos = os.listdir(os.path.join(os.path.dirname(__file__), 'decks'))
            repos = [x for x in repos if x[0] != '.']
            return repos
        else:
            test = Version_Control(self.current_repo)
            return test.list()

    #Lets the user move into a repo
    def enter_repo(self, name):
        if name in self.list_repo():
            self.current_repo = name

    #Lets the user commit to a repo they have created
    def commit_deck(self, path):
        temp = Version_Control(self.current_repo)
        temp.commit(path)

    #Pulls the most recent or a specific version of a deck
    def pull_deck(self, *args):
        temp = Version_Control(self.current_repo)

        #Handling the extra arguments
        #Checks if a version of the deck has been provided
        version = None
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

        #Check is the user wants to skip the text output of the deck list
        if "-h" in args or "-H" in args:
            return

        return "\n".join(deck)

    #Opens a visual display of a deck
    def show_deck(self, *args):
        temp = Version_Control(self.current_repo)

        #Checks if the deckname of the deck has been provided
        deckname = None
        for arg in args:
            if arg + ".txt" in temp.list():
                deckname = arg + ".txt"

        #If the deckname is nothing use the most recent deck
        if deckname == None:
            deckname = temp.most_recent()


        temp.webshow(deckname)
    
    #Exits the current repo
    def exit_repo(self):
        self.current_repo = None 

#Main body of the program
exit = False
interface = Ui()

print("Version controled deck building ready...")

#Main loop
while not exit:
    repo_display = [interface.current_repo if interface.current_repo != None else '']
    user_input = input(f"|>>-{repo_display[0]}>")
    result = interface.parse(user_input)

    #Prints a result to the screen if it needs printing
    if result != None:
        if type(result ) == list:
            result = ", ".join(result)

        print(result)
    
    

