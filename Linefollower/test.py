path = ['B', 'B', 'B']
path_length = 3
total_angle = 0

def tot(argument):
    global total_angle
    if argument == "R":
        total_angle += 90
    elif argument == "L":
        total_angle += 270
    elif argument == "B":
        total_angle += 180
    else:
        total_angle +=0
        

def angle(argument):
        if argument == 0:
            path[path_length-3] = "S"
        elif argument == 90:
            path[path_length-3] = "R"
        elif argument == 180:
            path[path_length-3] = "B"
        elif argument == 270:
            path[path_length-3] = "L"

def simplify_path():
    global path_length
    global path
    if path_length<3 or path[path_length-2] != "B":
        return
    global total_angle
    
    for i in range(1,4):
        tot(path[path_length-i])
        print(path[path_length-i], total_angle)
        
    total_angle = total_angle%360
   
    angle(total_angle)
    path.pop()
    path.pop()
    path_length -=2


simplify_path()
print(path)
print(path_length)