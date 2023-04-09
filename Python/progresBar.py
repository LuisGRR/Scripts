import math
import numbers
import colorama

def progres_bar(progres,total,color=colorama.Fore.YELLOW):
    percentage = 100*(progres/float(total))
    bar = '=' * int(percentage) + '-' * (100 - int(percentage))
    print(color + f"`\r|{bar}|{percentage:.2f}%", end="\r")

numbers = [x * 5 for x in range(2000,3000)]
result = []

progres_bar(0,len(numbers))
for i,x in enumerate(numbers):
    result.append(math.factorial(x))
    progres_bar(i +1,len(numbers))