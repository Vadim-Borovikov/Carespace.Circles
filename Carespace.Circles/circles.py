from asyncio.windows_events import NULL
import json
from json import JSONEncoder

def process(string):
    string = string.strip()
    while not string[0].isalpha():
        string = string.replace(string[0], '')
    return string.capitalize()

class Encoder(JSONEncoder):
    def default(self, o):
        return o.__dict__

class Group:
    def __init__(self, label):
        self.label = label
        self.groups = []

    def color(self, color):
        self.gcolor = color

class Circle:
    def __init__(self, colors):
        self.groups = []
        self.colors = colors
    
    def generate(self, lines):
        for line in lines:
            tabs = line.count('\t')
            line = process(line)
            group = Group(line)
            if tabs == 0:
                top = group
                colors = self.colors.pop(0).copy()
                top.color(colors.pop(0))
                self.groups.append(top)
                middle_color = colors.pop(0) if len(colors) > 0 else NULL
                bottom_color = colors.pop(0) if len(colors) > 0 else NULL
            elif tabs == 1:
                middle = group
                middle.color(middle_color)
                top.groups.append(middle)
            else:
                group.color(bottom_color)
                middle.groups.append(group)

class CircleWrapper:
    def __init__(self, name, colors):
        self.source = name + '.txt'
        self.target = name + '.json'
        self.circle = Circle(colors)
    
    def generate(self):
        with open(self.source, 'r', encoding = 'utf8') as file:
            self.circle.generate(file.readlines())
    
    def save(self):
        with open(self.target, 'w+', encoding = 'utf8') as file:
            json.dump(self.circle, file, ensure_ascii = False, cls = Encoder, indent = 2)

def update(name, colors):
    circle = CircleWrapper(name, colors.copy())
    circle.generate()
    circle.save()

colors1 = [['#ff9c01', '#faa927', '#fab646'],
           ['#b43c97', '#ba56a5', '#c46db1'],
           ['#0158e5', '#436ee7', '#5c82eb'],
           ['#e50130', '#e12748', '#e54562']]

colors2 = [['#ff0000'],
           ['#ff00ff'],
           ['#00ffff'],
           ['#ffff00']]

update('feelings', colors1)
update('needs', colors1)
update('critics', colors2)