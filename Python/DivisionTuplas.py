ini_tuple = (1, 2, 3, 4, 8, 12, 3, 34,67, 45, 1, 1, 43, 65, 9, 10) 
  
print ("initial list", str(ini_tuple)) 
  
# res = tuple(ini_tuple[x:x + 4]  
#       for x in range(0, len(ini_tuple), 4)) 

res = tuple(ini_tuple[n:n + 2] for n, i in enumerate(ini_tuple) if n % 2 == 0) 


print (str(res[1]))
print(str(len(res)))

for numerTuples in res:
    print(numerTuples)


print ("resultant tuples", str(res)) 