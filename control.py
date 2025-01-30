
#Imports
#For file management
import os

#For maintaining file upload times
import datetime


#Handles the creation of vertions of file
class Version_Control():
    
    def __init__(self, name):
        self.name = name
        self.dir_path =  os.path.join("decks", name)
        self.full_path = os.path.join(os.path.dirname(__file__), self.dir_path)
        #Checks if a directory for this deck exists yet
        #If not create one
        if not os.path.isdir(self.full_path):
            os.mkdir(self.full_path)

    #Commits a new version of the deck list
    #Path is the path to the file to be commited
    def commit(self, path):

        #Saves the contents of the commited file
        with open(path, 'r') as f:
            content = f.read()

        #Writes the contents into the correct new file
        date = datetime.datetime.now()
        with open(os.path.join(self.full_path, f'{self.name}-[{date.day}-{date.month}-{date.year}][{date.hour}-{date.minute}].txt'), 'w') as f:
            f.write(content)

    #Lists all the versions associated with this file



a = Version_Control("test")
a.commit("test.txt")