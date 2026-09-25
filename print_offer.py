with open('/Volumes/Juggernut_Assist/Projects/Kapi/Kapitoday/dash/models.py', 'r') as f:
    lines = f.readlines()
    in_offer = False
    for line in lines:
        if line.startswith("class Offer("):
            in_offer = True
        elif line.startswith("class ") and in_offer:
            break
        
        if in_offer:
            print(line, end="")
