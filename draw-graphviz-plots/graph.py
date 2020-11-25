import chevron, graphviz, copy


def file_node(data):
    if data['visible']:
        style = "filled"
    else:
        style = "invis"

    rendered_lines = file_node_lines(data['lines'], data['line_colors'])
        
    with open('mustache/file.dot', 'r') as f:
        return chevron.render(f, {'style': style,
                                 'label_color' : data['label_color'],
                                 'filename' : data['filename'],
                                 'lines' : rendered_lines,
                                  'source' : data['source']})

def file_node_lines(lines, colors):
    return "".join([file_node_line(line, colors[i]) for i, line in enumerate(lines)])

def file_node_line(line_text, line_color):
    if(line_color is None):
        line_color = "darkgray"
        
    return f'<i><font color="{line_color}">{line_text}</font></i><br align="left"/>'

def render_node(data):
    if data['type'] == "file":
        return file_node(data)
    else:
        return folder_node(data)

def graph(label, files):
    file_lines = "".join([render_node(file) for file in files])

    with open('mustache/graph.dot', 'r') as f:
        return chevron.render(f, {'files': file_lines,
                                  'label' : label})

def folder_node(data):
    if data['visible']:
        style="filled"
    else:
        style="invis"
    
    return f"{data['label']} [shape=folder fillcolor=yellow style={style}]\n{data['source']} -> {data['label']} [style={style}]"

# original data structure without commit
orig = [{ 'filename': "red.txt",
           'type': "file",
          'label_color': "red",
          'lines': ["Apples", "Strawberries", "Roses,"],
          'line_colors': [None, None, None],
          'visible': True,
           'source': "root" },
         { 'filename': "green.txt",
           'type': "file",
          'label_color': "darkgreen",
          'lines': ["Grapes", "Cucumbers", "Avocados"],
          'line_colors': [None, None, None],
          'visible': True,
           'source': "root" },
         { 'filename': "blue.txt",
           'type': "file",
          'label_color': "blue",
          'lines': ["Blueberries", "Smurfs", "Cookie Monsters"],
          'line_colors': [None, None, None],
          'visible': True,
           'source': "root" },
         { 'filename': "orange.txt",
           'type': "file",
          'label_color': "brown",
          'lines': ["Oranges", "Pumpkins", "Goldfish"],
          'line_colors': [None, None, None],
          'visible': True,
           'source': "other" },
         { 'type' : "folder",
           'label' : "other",
           'visible' : True,
           'source' : "root"}
]

# git same tree, all hidden
hidden = copy.deepcopy(orig)

for i, v, in enumerate(orig):
    hidden[i]['visible'] = False

## Working directory
lines = graph("Working Directory", orig)
graphviz.Source(lines, format="png").view(filename="../assets/img/0-working-directory")
    
# We're adding Red
add_red = copy.deepcopy(hidden)
add_red[0]['visible'] = True

lines = graph("Staging Area (Index)", add_red)
graphviz.Source(lines, format="png").view(filename="../assets/img/1-add-red")

# Create an empty commit
lines = graph("HEAD (Not set yet)", hidden)
graphviz.Source(lines, format="png").view(filename="../assets/img/1-empty-commit")

## add red.txt + green.txt
add_green = copy.deepcopy(hidden)
add_green[0]['visible'] = True
add_green[1]['visible'] = True

lines = graph("Staging Area (Index)", add_green)
graphviz.Source(lines, format="png").view(filename="../assets/img/2-add_green")

# commit red.txt + green.txt
commit_green = copy.deepcopy(hidden)
commit_green[0]['visible'] = True
commit_green[1]['visible'] = True

lines = graph("Last Commit  (Add lists of red and green objects)", add_green)
graphviz.Source(lines, format="png").view(filename="../assets/img/3-commit_red_and_green")

# Add blue to the staging area
add_blue = copy.deepcopy(hidden)
add_blue[0]['visible'] = True
add_blue[1]['visible'] = True
add_blue[2]['visible'] = True

lines = graph("Staging Area (Index)", add_blue)
graphviz.Source(lines, format="png").view(filename="../assets/img/4-add_blue")

# Make changes to two files in the working directory
edit_add_color = "darkgreen"
edit_add_colors = copy.deepcopy(orig)
edit_add_colors[0]['lines'][0] = f'<font color="{edit_add_color}">Red Apples</font>'
edit_add_colors[1]['lines'][0] = f'<font color="{edit_add_color}">Green Grapes</font>'
edit_add_colors[0]['lines'][2] = f'<font color="{edit_add_color}">Roses</font>'

lines = graph("Working Directory", edit_add_colors)
graphviz.Source(lines, format="png").view(filename="../assets/img/5-edit_original")

# Git add specific Red (note - OUT OF SYNC NOW)
add_specific = copy.deepcopy(add_blue)

edit_add_color = "darkgreen"
add_specific[0]['lines'][0] = f'<font color="{edit_add_color}">Red Apples</font>'

lines = graph("Staging Area (Index)", add_specific)
graphviz.Source(lines, format="png").view(filename="../assets/img/6-stage_colors_red")

# Add specific green
add_specific[1]['lines'][0] = f'<font color="{edit_add_color}">Green Grapes</font>'

lines = graph("Staging Area (Index)", add_specific)
graphviz.Source(lines, format="png").view(filename="../assets/img/7-stage_colors_green")

# Commit stuff
lines = graph("Last Commit  (Specify ambiguous colours)", add_specific)
graphviz.Source(lines, format="png").view(filename="../assets/img/8-commit_colors_red_green")

# Commit everything (including roses and terracotta) [ git commit -a]
lines = graph("Staging Area (Index)", edit_add_colors)
graphviz.Source(lines, format="png").view(filename="../assets/img/9-stage_everything_else")

lines = graph("Last Commit  (Committed everything else)", edit_add_colors)
graphviz.Source(lines, format="png").view(filename="../assets/img/10-commit_everything_else")

# Got a few things to undo later (the monster last-commit and the blue + other commit in the middle)


#graphviz.Source(lines, format='svg').pipe().decode('utf-8').view()
#src = graphviz.Source(lines, format='png').pipe()


#graphviz.Source(lines, format="png").render(filename="assets/img/10-commit_everything_else")

# import cv2 library 
#import cv2 
  
# read the images 
#img1 = cv2.imread('images/10-commit_everything_else.png')
#cv2.hconcat(img1, img1, img1).show()
