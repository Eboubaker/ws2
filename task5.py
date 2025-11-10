from abc import ABC, abstractmethod

class TextTransformation(ABC):
    @abstractmethod
    def transform(self, text):
        pass

class NormalText(TextTransformation):
    def transform(self, text):
        return text

class UpperCaseText(TextTransformation):
    def transform(self, text):
        return text.upper()

class LowerCaseText(TextTransformation):
    def transform(self, text):
        return text.lower()

class ReverseText(TextTransformation):
    def transform(self, text):
        return text[::-1]

class FileSystemItem(ABC):
    def __init__(self, name):
        self.name = name
    
    @abstractmethod
    def display(self, indent=0):
        pass
    
    @abstractmethod
    def get_size(self):
        pass

class TextFile(FileSystemItem):
    def __init__(self, name, content=""):
        super().__init__(name)
        self.content = content
        self.transformation = NormalText()
    
    def set_transformation(self, strategy):
        self.transformation = strategy
        print(f"Applied transformation to {self.name}")
    
    def get_content(self):
        return self.transformation.transform(self.content)
    
    def display(self, indent=0):
        spaces = "  " * indent
        print(f"{spaces}📄 {self.name}")
        print(f"{spaces}   Content: {self.get_content()}")
    
    def get_size(self):
        return len(self.content)

class Directory(FileSystemItem):
    def __init__(self, name):
        super().__init__(name)
        self.items = []
    
    def add(self, item):
        self.items.append(item)
        print(f"Added {item.name} to {self.name}")
    
    def remove(self, item):
        self.items.remove(item)
        print(f"Removed {item.name} from {self.name}")
    
    def display(self, indent=0):
        spaces = "  " * indent
        print(f"{spaces}📁 {self.name}/")
        for item in self.items:
            item.display(indent + 1)
    
    def get_size(self):
        return sum(item.get_size() for item in self.items)


root = Directory("MyDocuments")

# Create text files
file1 = TextFile("hello.txt", "Hello World")
file2 = TextFile("test.txt", "Python Programming")
file3 = TextFile("readme.txt", "This is a README file")

# add files 
root.add(file1)
root.add(file2)

# subdirectory
projects = Directory("Projects")
root.add(projects)

# add file to subdirectory
projects.add(file3)

# nested directory
python_dir = Directory("Python")
projects.add(python_dir)

file4 = TextFile("code.txt", "def hello(): print('Hi')")
python_dir.add(file4)

print("\n--- display file system ---")
root.display()

print("\n--- apply transformations ---")
file1.set_transformation(UpperCaseText())
file2.set_transformation(LowerCaseText())
file3.set_transformation(ReverseText())

print("\n--- after transformations ---")
root.display()

print(f"\n--- total: {root.get_size()} characters ---")
