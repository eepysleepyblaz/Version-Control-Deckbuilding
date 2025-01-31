
#Imports
#For file management
import os

#For maintaining file upload times
import datetime

#For get card images
import webbrowser

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
    def list(self):
        files = os.listdir(self.full_path)
        return files
    
    #Creates a webpage of a specific deck list and opens it
    def webshow(self, filename):
        with open(os.path.join(self.full_path, filename)) as f:
            contents = f.read()
        
        contents = contents.split("\n")

        #Temporaily creates an html file to view the page with
        with open('temp.htm', 'w') as f:
            f.write("<!DOCTYPE html>\n")
            f.write("<html>\n")
            f.write("<head>\n")
            f.write(f"<title>{self.name}</title>\n")
            f.write("</head>\n")
            f.write("<body>\n")

            #Loops to add all the card images
            for card in contents:
                if card != "":
                    amount = int(card.split(" ")[0])
                    cardname = card.split(" ")[1:]
                    cardname_formatted = "+".join(cardname)
                    for i in range(amount):
                        f.write(f'<img src="https://api.scryfall.com/cards/named?exact={cardname_formatted}&format=image" width="252" height="352">\n')

            f.write("</body>\n")
            f.write("</html>\n")
        
        #Opens the file
        webbrowser.open('temp.htm')
        input()
        os.remove('temp.htm')








#Test code
a = Version_Control("test")
a.commit("C:/Users/myaccount/Downloads/mono-blue.txt")
print(a.list())
a.webshow("test-[30-1-2025][23-38].txt")