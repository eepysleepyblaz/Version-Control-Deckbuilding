
#Imports
#For file management
import os

#For maintaining file upload times
import datetime

#For get card images
import webbrowser

#Handles the creation of vertions of file and viewing of the versions
class Version_Control():
    
    def __init__(self, name):
        self.name = name
        self.dir_path =  os.path.join("decks", name)
        self.full_path = os.path.join(os.path.dirname(__file__), self.dir_path)
    
    def make_repo(self):
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

        #Removes any blank lines
        content = content.split("\n")
        temp_content = []
        for line in content:
            if line != "":
                temp_content.append(line)
        content = "\n".join(temp_content)

        #Writes the contents into the correct new file
        date = datetime.datetime.now()
        filename = f'{self.name}-[{date.day:02}-{date.month:02}-{date.year:04}][{date.hour:02}-{date.minute:02}].txt'
        with open(os.path.join(self.full_path, filename), 'w') as f:
            f.write(content)

        #Returns the files new name
        return filename

    #Lists all the versions associated with this file
    def list(self):
        files = os.listdir(self.full_path)
        for i in range(len(files)):
            files[i] = "-".join(files[i].split("-")[1:]).split(".")[0]
        return files
    
    #Returns a specific deck list
    #By default the most recently commited
    def get(self, version=None):
        files = os.listdir(self.full_path)

        #If a specific date is given
        #The form is (d)d-(m)m-yyyy-(h)h-(m)m
        if version != None:
            version = version.split("-")
            filename = f"{self.name}-{'-'.join(version)}.txt"
            with open(os.path.join(self.full_path, filename), "r") as f:
                contents = f.read()
        
        #If no date is given
        else:
            filename = self.most_recent()
            with open(os.path.join(self.full_path, filename), "r") as f:
                contents = f.read()
        
        return "-".join(filename.split("-")[1:]).split(".")[0], contents
    
    #Gets the most recent file
    def most_recent(self):
        newest_version = None
        files = os.listdir(self.full_path)

        #Finds the most recent day of commits
        #recent_day = (day, month, year)
        recent_day = [0, 0, 0]
        for file in files:
            if int(file.split("]")[0].split("-")[-1]) >= recent_day[2]:
                if int(file.split("]")[0].split("-")[-2]) >= recent_day[1]:
                    if int(file.split("]")[0].split("-")[-3][1:]) >= recent_day[0]:
                        recent_day = [int(file.split("]")[0].split("-")[-3][1:]),
                                        int(file.split("]")[0].split("-")[-2]),
                                        int(file.split("]")[0].split("-")[-1])]
        #recent_time = (hour, min)
        recent_time = [0, 0]
        #Finds the most recent file in the most recent day
        for file in files:
            if [int(file.split("]")[0].split("-")[-3][1:]),
                int(file.split("]")[0].split("-")[-2]),
                int(file.split("]")[0].split("-")[-1])] == recent_day:

                time = [int(file.split("[")[2].split("-")[0]), int(file.split("[")[2].split("-")[1][:-5])]
                
                if time[0] > recent_time[0]:
                    recent_time = [int(file.split("[")[2].split("-")[0]), int(file.split("[")[2].split("-")[1][:-5])]
                    newest_version = file
                elif time[0] == recent_time[0] and time[1] > recent_time[1]:
                    recent_time = [int(file.split("[")[2].split("-")[0]), int(file.split("[")[2].split("-")[1][:-5])]
                    newest_version = file

        return newest_version
    
    #Creates a webpage of a specific deck list and opens it
    def webshow(self, filename):
        with open(os.path.join(self.full_path, filename), "r") as f:
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
        input("Press enter to quit viewing the deck")
        os.remove('temp.htm')



