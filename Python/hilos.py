from ast import arg
from itertools import islice 
import threading
import time

# def manejarCliente1():
#     while(True):
#         print("Esperando al cliente 1...")
#         time.sleep(3) # Espera 3 segundos     

# def manejarCliente2():
#     while(True):
#         print("Esperando al cliente 2...")
#         time.sleep(3) # Espera 3 segundos
# # Creacion de los hilos
# t = Timer(5.0, manejarCliente1)
# t2 = Timer(3.0, manejarCliente2)
# # Ejecutar los hilos
# t.start()
# t2.start()

def contar():
    contador = 0
    while contador<100:
        contador+=1
        print('Hilo:', 
              threading.current_thread().getName(), 
              'con identificador:', 
              threading.current_thread().ident,
              'Contador:', contador)

NUM_HILOS = 2

for num_hilo in range(NUM_HILOS):
    hilo = threading.Thread(name='hilo%s' %num_hilo,target=contar)    
    hilo.start()


# Clase hilo
# class MiHilo(threading.Thread):
#     def __init__(self,x):
#         self.__x = x
#         threading.Thread.__init__(self)
#     def run (self):  # run() se utiliza para definir el comportamiento del hilo
#           print(str(self.__x))

# # Inicia 10 hilos.
# for i in range(10):
#     MiHilo(i).start()


test_dict = {'gfg' : 6, 'is' : 4, 'for' : 2, 'CS' : 10,'w' : 6, 'q' : 4, 'r' : 2,'4' : 6, 'y' : 4, 'l' : 2,'ll' : 6, 'hh' : 4, 'n' : 2,'f' : 6, 'nh' : 4, 'fovdr' : 2} 
  
print("The original dictionary : " +  str(test_dict)) 
  
inc = iter(test_dict.items()) 
res1 = dict(islice(inc, len(test_dict) // 2))  
res2 = dict(inc) 

inc1 = iter(res1.items()) 
res11 = dict(islice(inc1, len(res1) // 2))  
res12 = dict(inc1) 

inc2 = iter(res2.items()) 
res21 = dict(islice(inc2, len(res2) // 2))  
res22 = dict(inc2) 
  
# print("The first half of dictionary : " + str(res1)) 
# print("The second half of dictionary : " + str(res2)) 


def mostrar(dic):
    for iter in dic :
        print('Hilo: ', 
              threading.current_thread().name, 
              'Valor: ', iter)
        time.sleep(3)


hilo1 = threading.Thread(name='hilo1',target=mostrar,args=(res11,))    
hilo2 = threading.Thread(name='hilo2',target=mostrar,args=(res12,))    
hilo3 = threading.Thread(name='hilo3',target=mostrar,args=(res21,))    
hilo4 = threading.Thread(name='hilo4',target=mostrar,args=(res22,))    

hilo1.start()
hilo2.start()
hilo3.start()
hilo4.start()

hilo1.join()
hilo2.join()
hilo3.join()
hilo4.join()