class openfile:
    def __init__(self,filename):
        self.filename = filename

    def open(self):
        return self.file
    def close(self):
        self.file.close()


class readefile(openfile):
    def __init__(self, filename):
        self.filename = filename
        self.file = openfile(self.filename)
        self.file = open(self.filename,'r')
    def read(self):
        return self.file.readlines()

class writetofile(openfile):
    def __init__(self, filename):
        self.filename = filename
        self.file = openfile(self.filename)
        self.file = open(self.filename,'w')
    def write(self, string):
        with self.file.open:
            self.file.write(string)
            self.file.flush()

