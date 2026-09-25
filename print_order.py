with open('/Volumes/Juggernut_Assist/Projects/Kapi/Kapitoday/dash/models.py', 'r') as f:
    lines = f.readlines()
    in_order = False
    for line in lines:
        if line.startswith("class Order("):
            in_order = True
        elif line.startswith("class ") and in_order:
            break
        if in_order:
            print(line, end="")
