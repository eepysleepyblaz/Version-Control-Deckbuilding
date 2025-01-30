
#Imports
#For file management
import os


#Handles the creation of vertions of file
class Version_Control():
    
    def __init__(self, name):
        self.name = name

        #Checks if a directory for this deck exists yet
        #If not create one
        if not os.path.isdir(f"decks/{name}"):
            os.mkdir(os.path.join(os.path.dirname(__file__), f'decks/{name}'))


a = Version_Control("test")