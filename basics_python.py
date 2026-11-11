
if (2 < 3):
    print("2 is less than 3")
for i in range(5):
    print(i)
print("-----------")
a=[19, 222, 53, 77, 500]
for i in a:
    print(i)

for name in ["Alice", "Bob", "Charlie"]:
    print(name)



b=0
while b < 5:
    print(b)
    b += 1

for i in range(3):
    x=int(input("Enter a number > 0 : "))
    if x < 0:
        break
    print("Super")

for i in range(5):
    if i % 2 == 0:
        continue
    print("You entered:", x)

def unfertige_function():
    pass

try:
    zahl = int(input("Zahl: "))    
    print(10 / zahl)               
except ValueError:                 
    print("Das war keine Zahl.")
except ZeroDivisionError:          
    print("Nicht durch 0 teilen!")
else:                              
    print("Alles ok")
finally:                         
    print("Fertig")



while True:                        
    try:
        alter = int(input("Alter: "))
        if alter < 0:
            print("Negativ geht nicht.")
            continue               
        break                     
    except ValueError:
        print("Bitte eine Zahl eingeben.")
print("Dein Alter:", alter)