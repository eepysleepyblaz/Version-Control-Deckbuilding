
#Imports
#Imports the control.py file for its functionality
from control import Version_Control

#For repo access
import os

#To check methods parameter sizes
import inspect

#Grants functionality for the user to use the methods of control
class Ui():

    def __init__(self):
        #Defines the command list
        self.command_dict = {'cr': self.create_repo,
         'lr': self.list_repo,
         'commit': self.commit_deck,
         'pull': self.pull_deck,
         'show': self.show_deck}
        
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
            if param.default != inspect._empty:
                extra += 1

        #Checks the number of paramters is correct
        if len(inspect.signature(self.command_dict[command[0]]).parameters) > len(command[1:]) + extra:
            return f"{command[0]} takes {len(inspect.signature(self.command_dict[command[0]]).parameters)} parameters. You provided {len(command[1:])}"

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
    def pull_deck(self, name, version=None):
        temp = Version_Control(name)
        return temp.get(version)

    #Opens a visual display of a deck
    def show_deck(self, name, deckname=None):
        temp = Version_Control(name)

        #If the deckname is nothing use the most recent deck
        if deckname == None:
            deckname = temp.most_recent()
        else:
            deckname = deckname + ".txt"

        temp.webshow(deckname)


#Main body of the program
exit = False
interface = Ui()

print("version conroled deck building ready...")

#Main loop
while not exit:
    user_input = input("|>>->")
    result = interface.parse(user_input)

    #Prints a result to the screen if it needs printing
    if result != None:
        if type(result ) == list:
            result = ", ".join(result)

        print(result)
    
    

