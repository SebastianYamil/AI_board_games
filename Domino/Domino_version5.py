# -*- coding: utf-8 -*-
import copy
from scipy.stats import hypergeom


class Ficha:
    _id_counter = 0

    def __init__(self, numero1, numero2):
        Ficha._id_counter += 1
        self.id = Ficha._id_counter  # Identificador único de la ficha
        self.numero1 = numero1
        self.numero2 = numero2

    # Getter para ID
    def get_id(self):
        return self.id

    # Getter para el primer número de la ficha
    def get_numero1(self):
        return self.numero1

    # Setter para el primer número de la ficha
    def set_numero1(self, numero1):
        self.numero1 = numero1

    # Getter para el segundo número de la ficha
    def get_numero2(self):
        return self.numero2

    # Setter para el segundo número de la ficha
    def set_numero2(self, numero2):
        self.numero2 = numero2

    # Representación en cadena de la ficha
    def __str__(self):
        return f"ID: {self.id}, Ficha: [{self.numero1}, {self.numero2}]"


class Domino:
    def __init__(self):
        self.cont1 = 0  # Cuenta las fichas que tiene el jugador 1
        self.cont2 = 0  # Cuenta las fichas que tiene el jugador 2
        self.fichas = [] #Numero de fichas que no están en nuestra posesión
        self.fichasjugador1 = []  # Conjunto de fichas de jugador1 (Que somos nosotros)
        self.extremos = []  # Este arreglo contiene los números que están en los extremos y por lo tanto son los lugares en los que podemos poner
        self.fichas_usadas = []  # Fichas que ya jugamos
        self.jugador = 0  # Definimos esta variable para saber el turno de qué jugador es
        
    def inicializar(self):
        #Creamos las 28 fichas
        for i in range(7):
            for j in range(i, 7):
                ficha = Ficha(i, j)
                self.fichas.append(ficha)
                

    def robar_ficha_j1(self, id):
        try:
            # Creamos un objeto de la clase ficha que represente la que robó el jugador
            ficha = self.fichas[id]
            # Con la siguiente instrucción eliminamos la ficha que estaba en el pozo
            self.fichas[id] = None
            # Agregamos la ficha a la lista de fichas que tiene el jugador 1
            self.fichasjugador1.append(ficha)
            # Aumentamos el contador que indica la cantidad de fichas que tiene el jugador 1
            self.cont1 += 1
        except (IndexError, TypeError):
            print("No hay tal ficha disponible para robar")
            
    def robar_ficha_j2(self):
        self.cont2=self.cont2+1
        #Solo podemos aumentar el contador del j2 ya que no sabemos la ficha en específico

    
    
    def encontrar_id(self, num1, num2):
    # Esta función busca el ID de una ficha dadas sus dos mitades (números)
    # Primero busca la ficha en el pozo general
        for i in range(len(self.fichas)):
            if self.fichas[i] is not None and ((self.fichas[i].numero1 == num1 and self.fichas[i].numero2 == num2) or (self.fichas[i].numero2 == num1 and self.fichas[i].numero1 == num2)):
                return self.fichas[i].id
    # Busca la ficha en las fichas que tiene el jugador 1
        for i in range(len(self.fichasjugador1)):
            if (self.fichasjugador1[i].numero1 == num1 and self.fichasjugador1[i].numero2 == num2) or (self.fichasjugador1[i].numero2 == num1 and self.fichasjugador1[i].numero1 == num2):
                return self.fichasjugador1[i].id
    # Si no está ni en el pozo ni en las fichas del jugador 1, ya fue usada en la mesa
        for i in range(len(self.fichas_usadas)):
            if (self.fichas_usadas[i].numero1 == num1 and self.fichas_usadas[i].numero2 == num2) or (self.fichas_usadas[i].numero2 == num1 and self.fichas_usadas[i].numero1 == num2):
                return self.fichas_usadas[i].id
    # Si no se encuentra, devuelve -1 para indicar que no se encontró
        return -1
    
    
    def robar_inicial_j1(self):
        print("Jugador 1 ingrese sus fichas")
    
    # Creamos un conjunto para rastrear las fichas ya agregadas
        fichas_agregadas = set()

        while len(self.fichasjugador1) < 7:
            num_ficha = input("Ingrese las coordenadas de una ficha en formato x,y: ")
            try:
                num1, num2 = map(int, num_ficha.split(","))
                ficha = self.encontrar_ficha(num1, num2)
                if ficha is not None and ficha not in self.fichasjugador1 and ficha.id not in fichas_agregadas:
                    self.fichasjugador1.append(ficha)
                    self.cont1 += 1
                    fichas_agregadas.add(ficha.id)
                
                    # Aquí eliminamos la ficha de self.fichas
                    self.fichas.remove(ficha)
                    
                else:
                    print("Ficha inválida o ya agregada, intente de nuevo.")
            except ValueError:
                print("Formato incorrecto, ingrese dos números enteros separados por coma.")

        print("Fichas del Jugador 1:")
        for ficha in self.fichasjugador1:
            print(ficha.__str__())
        self.cont2=7

    #justar cont2 a 7 después de robar las fichas iniciales
      


    
     


    def mod_fichas_j1(self, ficha):
        # Esta función recibe una ficha y la elimina del conjunto de fichas que
        # sabemos que tiene el jugador 1 (nosotros)
        # Usaríamos esta función si el jugador 1 quiere poner una ficha y hay que borrarla de la lista de fichas que dice cuales tiene
        for i in range(len(self.fichasjugador1)):
        
            if self.fichasjugador1[i] is not None:
                if self.fichasjugador1[i].get_numero1() == ficha.get_numero1() and self.fichasjugador1[i].get_numero2() == ficha.get_numero2():
                    self.fichasjugador1[i] = None
                    #print('Se borró exitosamente')
                    # Encuentra la ficha y la borra del arreglo
                    return
        return

    def usarficha(self, ficha, pos):
    # pos es el índice del extremo en el que quiero poner la ficha
     ######print(ficha.__str__())
     #Esto se hizo para facilitarle la busqueda al minimax
     if self.jugador==2:
         ficha_usable= self.encontrar_ficha(ficha.numero1, ficha.numero2)
         
     else:
         ficha_usable= self.encontrar_ficha(ficha.numero1, ficha.numero2)
         
     try:
            if len(self.fichas_usadas) == 0:  # Si no hay fichas jugadas hasta el momento, guardará ambos lados de la ficha que vamos a poner como los extremos en los que podemos colocar fichas
                self.extremos.append(ficha.numero1)
                self.extremos.append(ficha.numero2)
                self.fichas_usadas.append(ficha)
                # A continuación, debemos ver cuál es el jugador que pone la ficha para cambiar los contadores
                if self.jugador == 1:
                    self.cont1 -= 1
                    self.mod_fichas_j1(ficha)
                else:
                    self.cont2 -= 1
                    #Se remueve la ficha del arrglo de fichas.
                    self.fichas.remove(ficha)
                    
            elif self.ficha_jugable(ficha):  # Comprobamos si se puede colocar la ficha
    
                if self.jugador == 1:
                    # Significa que es el turno del jugador 1
                    # Primero debemos comprobar que sea posible que el jugador tenga esa ficha
                    
                    if ficha_usable not in self.fichasjugador1:
                        print("No se puede colocar una ficha que no tienes")
                        return False
                    self.mod_fichas_j1(ficha_usable)
                    self.cont1 -= 1
                else:
                    # Significa que es el turno del jugador 2
                    
                    
                    if not ficha_usable:
                        print("No se puede colocar una ficha que no tienes")
                        return False
                    # Elimina esa ficha de las que están en el pozo ya que ya fue jugada
                    self.fichas.remove(ficha_usable)
                    self.cont2 -= 1
    
                # Para cambiar los valores de los extremos con los que se puede jugar
                if self.extremos[pos] == ficha.numero1:
                    self.extremos[pos] = ficha.numero2
                elif self.extremos[pos] == ficha.numero2:
                    self.extremos[pos] = ficha.numero1
                #Primero intentamos con la posición dada, pero como para llegar aquí ya es una ficha jugable,
                #atribuímos a error humano y la jugamos en el otro lado
                elif self.extremos[(pos+1)%2]==ficha.numero1:
                    self.extremos[(pos+1)%2]=ficha.numero2
                elif self.extremos[(pos+1)%2]==ficha.numero2:
                    self.extremos[(pos+1)%2]=ficha.numero1 #¿Qué está pasando?
                else:
                    print("La ficha no se puede colocar en ninguno de los extremos del juego")
                    return False
    
                # Agrega la ficha que el jugador puso al arreglo de las fichas que están acomodadas
                self.fichas_usadas.append(ficha_usable)
                return True
     except Exception as e:
            print("La ficha indicada no se puede utilizar:", str(e))

    
    def ficha_jugable(self, ficha):
        #Esta función determina si la ficha se puede colocar en el tablero en su estado actual
        
        #Primero verificamos que se haya jugado al menos una ficha en el tablero
        if(len(self.fichas_usadas)!=0):
            if ficha.numero1 in self.extremos: 
                return True
            elif ficha.numero2 in self.extremos:
                return True
            else:
                return False
        else:
            return True
        

    def usabilidad_j1(self):
        # Determina las fichas que puede poner el jugador 1
        # Este método analiza los valores en los extremos y regresa un arreglo con las fichas que se pueden usar en ese turno
         usables = []
         for i in range(len(self.fichasjugador1)):
             if self.fichasjugador1[i] is not None:
                # print(self.fichasjugador1[i])
                # print(self.fichasjugador1[i+1]) 
                if self.ficha_jugable(self.fichasjugador1[i]):
                    usables.append(self.fichasjugador1[i])
            
                
        
         return usables

    def usabilidad_j2(self):
        # Determina las fichas que puede poner el jugador 2
        # Este método analiza los valores en los extremos y regresa un arreglo con las fichas que se pueden usar en ese turno
        # Como no sabemos exactamente las fichas que tiene este jugador, buscamos en todas las fichas disponibles
        usables = []
        for i in range(len(self.fichas)):
            if(self.fichas[i] is not None):
                if self.ficha_jugable(self.fichas[i]):
                    usables.append(self.fichas[i])
        return usables
    def encontrar_ficha_roba(self, num1, num2):
        for ficha in self.fichas:
            if ficha and ((ficha.numero1 == num1 and ficha.numero2 == num2) or (ficha.numero2 == num1 and ficha.numero1 == num2)):
                return ficha

    def encontrar_ficha(self, num1, num2):
    # Esta función con tan solo darle los números de una ficha nos la regresa en forma de objeto ficha y con el id correcto
        if self.jugador == 1:
            for ficha in self.fichasjugador1:
                if ficha and ((ficha.numero1 == num1 and ficha.numero2 == num2) or (ficha.numero2 == num1 and ficha.numero1 == num2)):
                    return ficha
        else:
            for ficha in self.fichas:
                if ficha and ((ficha.numero1 == num1 and ficha.numero2 == num2) or (ficha.numero2 == num1 and ficha.numero1 == num2)):
                    return ficha
        return None
    
    

    #Esta función nos da al ganador
    def ganador(self):
        if self.cont1 == 0:
            return 2
        elif self.cont2 == 0:
            return -2
        else:
            return 0
        
        
    #Esta función nos rive mucho para que sepamos desde la consola qué estamos haciendo
    def imprime_ultima_jugada(self):
        if self.fichas_usadas:
            ultima_ficha = self.fichas_usadas[-1]
            print("ultima jugada:", ultima_ficha.__str__())
            return ultima_ficha.__str__()
        else:
            print("No se ha realizado ninguna jugada todavía.")
            
                
    def bloquea(self):
        if(len(self.fichas_usadas)!=0):
            if(self.extremos[0]==self.extremos[1]):
                return True
            else:
                return False
            #Así sabemos si el juego está bloqueado.
        else:
            return False
            
        #Esta función es para saber cuántas fichas tenemos de algún numero    
    def num_fichas_esp_j1(self, numero):
        arr_fichas= []
        for ficha in self.fichasjugador1:
            if ficha is not None:
                if(ficha.numero1== numero or ficha.numero2== numero):
                    arr_fichas.append(ficha)
        return arr_fichas
    
    #Función para saber el numero de fichas con un numero específico que podrían estar en el pozo o 
    #la mano de nuestro rival
    def num_fichas_esp_pozo(self, numero):
        arr_fichas = []
        for ficha in self.fichas:
            if ficha and (ficha.numero1 == numero or ficha.numero2 == numero):
                arr_fichas.append(ficha)
        return arr_fichas
    
    
    #Esto es para darle el parámetro a la función de probabilidad, conseguimos las fichas de un num específico
    #dentro de conjunto de jugables
    def numeros_fichas_usables(self):
        numeros= set()
        for ficha in self.usabilidad_j1():
            numeros.add(ficha.numero1)
            numeros.add(ficha.numero2)
            
        return numeros
    
    #Aquí sabemos si hay un empate
    def empate(self, jugador):
        if jugador==1:
            if(len(self.usabilidad_j2())==0):
                return True
        elif jugador==2:
            if(len(self.usabilidad_j1())==0):
                return True
        else:
            return False
        
    #Método para contar las mulas que tiene el jugador_!    
    def mulas_j1(self):
        mulas=[]
        for ficha in self.fichasjugador1:
            if ficha is not None:
                if ficha.numero1==ficha.numero2:
                    mulas.append(ficha)
        return mulas
    
        



class nodo_minimax:
    def __init__(self, estado_domino):
        self.estado_domino = estado_domino  # Instancia de la clase Domino que representa el estado del juego
        self.hijos = []  # Lista de nodos hijos
        self.valor_utilidad = 0  # El valor de utilidad asignado a este nodo
        self.bloquea = 0  # Valor booleano que indica si este nodo bloquea el juego
        self.probabilidad = 1.0  # Valor de probabilidad asociado al nodo
        self.dicc_pasa = {0: False, 1: False, 2: False, 3: False, 4: False, 5: False, 6: False} #Fichas con las que ha pasado
        self.jugadas_inteligentes=0 #Jugadas que determinamos son favorables estratégicamente
        self.mulas_estrategicas=0  #Valor positivo o negativo para retener una mula

    # Getter para bloquea
    def get_bloquea(self):
        return self.bloquea

    # Setter para bloquea
    def set_bloquea(self, bloquea):
        self.bloquea = bloquea

    # Getter para probabilidad
    def get_probabilidad(self):
        return self.probabilidad

    # Setter para probabilidad
    def set_probabilidad(self, probabilidad):
        self.probabilidad = probabilidad
        
        
    def valor_utilidad_final(self):
        #Con esto le damos la utilidad a cada nodo final
        ganador_estado = (self.estado_domino).ganador()
        if ganador_estado != 0:
            self.valor_utilidad = ganador_estado + self.evaluar()/2.5
        else:
            self.valor_utilidad = self.evaluar()
        return self.valor_utilidad
    
    #Queremos saber si es conveniente o no tener mulas dependiendo del juego y del momento
    def mulas_ponderadas(self):
        mulas=self.estado_domino.mulas_j1()
        if(len(mulas)!=0):
            for ficha in mulas:
                num_fichas=len(self.estado_domino.num_fichas_esp_j1(ficha.numero1))
                
                if(num_fichas>=3):
                    self.mulas_estrategicas+=0.5
                elif(num_fichas==2): 
                    self.mulas_estrategicas+= -0.4
                elif(num_fichas==1):
                    #Queremos castigar de forma muy dura el que te quedes solo con una mula de ese número!
                    self.mulas_estrategicas+= -1.1
    
        
                    
                    
     
      
     #Actualiza el diccionario
    def actualizar_dicc_pasa(self, num1, num2):
        if self.estado_domino.jugador == 2:
            # Reiniciar todos los valores a False
            self.dicc_pasa = {0: False, 1: False, 2: False, 3: False, 4: False, 5: False, 6: False}
            
            # Actualizar los valores correspondientes a los números recibidos
            self.dicc_pasa[num1] = True
            self.dicc_pasa[num2] = True



    def expandir(self):
        #La función expandir nos permite hacer el arbol de busqueda
        if self.estado_domino.jugador == 1:
            usables = self.estado_domino.usabilidad_j1()
            
        else:
            usables = self.estado_domino.usabilidad_j2()
            self.roba_todo_y_pasa(usables)
            #Queremos favorecer escenarios clave

        # Crear nodos hijos para cada movimiento jugable y agregarlos a la lista de hijos
        for ficha in usables:
            
                
            nuevo_estado = copy.deepcopy(self.estado_domino)
            nuevo_nodo = nodo_minimax(nuevo_estado)
            nuevo_nodo.bloquea+= nuevo_nodo.bloqueo_ponderado()
            #La incertidumbre sobre la siguiente jugada solo existe cuando tiramos nosotros, por eso
            #solo se modifica la probabilidad si tira el jugador2
            if(nuevo_nodo.estado_domino.jugador==1):
                nuevo_nodo.set_probabilidad(self.get_probabilidad()*nuevo_nodo.probabilidad_respuesta(ficha))
                
            nuevo_nodo.estado_domino.usarficha(ficha, 0)  # Simulamos el movimiento en el nuevo estado 
            #Queremos ver si el tablero se está manteniendo con las piezas que nos favorecen
            if self.dicc_pasa.get(nuevo_nodo.estado_domino.extremos[0]) or self.dicc_pasa.get(nuevo_nodo.estado_domino.extremos[1]):
                nuevo_nodo.jugadas_inteligentes = self.jugadas_inteligentes+1
            self.mulas_ponderadas()
            nuevo_nodo.estado_domino.jugador=nuevo_nodo.estado_domino.jugador%2+1
            self.hijos.append(nuevo_nodo)
        
    #Esto nos ayuda a darle un peso a los escenarios en donde tenemos mas o menos fichas que el adversario        
    def diferencia_ponderada(self,cont1, cont2):
     diferencia_fichas = cont2 - cont1

     if diferencia_fichas < -2:
        resta_ponderada = -0.5
     elif diferencia_fichas == -1:
        resta_ponderada = 0.35
     elif diferencia_fichas == -2:
        resta_ponderada = 0
     elif diferencia_fichas == 0:
        resta_ponderada = 0.5
     elif diferencia_fichas == 1:
        resta_ponderada = 0.88
     elif diferencia_fichas == 2:
        resta_ponderada = 1
     else:
        resta_ponderada = 1.1

     return resta_ponderada
 
    def roba_todo_y_pasa(self,usabilidad):
        if(len(usabilidad)==0):
        #Esta función tiene como único propósito modelar el escenario en que el rival de alguna forma 
        #no tuvo fichas usables porque todas las tenemos nosotros así que deberá robar todas las fichas del pozo
            self.jugadas_inteligentes=100
            self.estado_domino.cont2=len(self.estado_domino.fichas)
            #Queremos favorecer MUCHO estos escenarios, por lo que le damos un gran peso.
        elif(len(usabilidad)==1):
            self.jugadas_inteligentes=5
            
         
        
 
    #Esta función nos ayuda a saber si el juego está bloqueado y, lo más importante, si nos conviene que esté
    #bloqueado
    def bloqueo_ponderado(self):
        if(self.estado_domino.bloquea()):
            punt_bloqueo_j1=len(self.estado_domino.usabilidad_j1())
            punt_bloqueo_j2=len(self.estado_domino.usabilidad_j2())
            if(punt_bloqueo_j1==0):
                return -0.1
            if(punt_bloqueo_j1==1 and punt_bloqueo_j2>=3):
                return 0.3
            if(punt_bloqueo_j1==1 and punt_bloqueo_j2<3):
               return 0.65
            
            elif(punt_bloqueo_j1==2 and punt_bloqueo_j2<4):
                return 0.85
            elif(punt_bloqueo_j1==2 and punt_bloqueo_j2>=4):
                return 0.6
            elif(punt_bloqueo_j1>2):
                return 1.05
            
        else:
            return 0
    
    # x :   Número de fichas con el número especificado
    # y :   Número de fichas del mismo número que tú tienes
    # z :   Número de fichas que tiene el rival en total
    # a :  Número de fichas que quedan en el pozo
    
    #Aquí obtendremos la probabilidad de que se juegue una ficha con un num específico
    def probabilidad_numero(self,numero):
        #Numero de fichas con el num especificado
        num_fichas_disp= len(self.estado_domino.num_fichas_esp_pozo(numero)) 
        #Numero de fichas del mismo numero que nosotros tenemos
        num_fichas_j1=len(self.estado_domino.num_fichas_esp_j1(numero))
        #Numero de fichas que tiene el rival en total
        num_fichas_rival=self.estado_domino.cont2
        #Numero de fichas que quedan en el pozo
        num_fichas_pozo=len(self.estado_domino.fichas) - num_fichas_rival
        
        w= num_fichas_disp
        x= num_fichas_rival+num_fichas_pozo
        y= 7- num_fichas_j1
        z= num_fichas_rival
        proba=hypergeom.cdf(w,x,y,z)-hypergeom.pmf(0,x,y,z)
        #Restamos la función de masa de f(0) porque queremos medir la probabilidad de que 
        #el rival tenga una o más de las fichas con ese numero!
        
        return proba
    
    #Aquí calculamos la probabilidad de respuesta del adversario
    def probabilidad_respuesta(self,ficha):
        num1=ficha.numero1
        num2=ficha.numero2
        if(len(self.estado_domino.fichas_usadas)!=0):
            #min_prob= float('inf')
            num3=self.estado_domino.extremos[0]
            num4=self.estado_domino.extremos[1]
            if(num1==num3):
                return self.probabilidad_numero(num2)
            elif(num2==num3):
                return self.probabilidad_numero(num1)
            elif(num1==num4):
                return self.probabilidad_numero(num2)
            else:
                return self.probabilidad_numero(num1)
        else:
            #Calculamos la probabilidad de que responda
            prob=max(self.probabilidad_numero(num1), self.probabilidad_numero(num2))
            return prob
            
            
    
        
        
        

    def evaluar(self):
        #Esto es nuestra función heurística
        cont_jugador1 = self.estado_domino.cont1
        cont_jugador2 = self.estado_domino.cont2

        resta_ponderada = self.diferencia_ponderada(cont_jugador1, cont_jugador2)
        bloqueo_ponderado = self.bloqueo_ponderado()
        proba=self.probabilidad
        
        
        eval = proba*(resta_ponderada * 0.4 +bloqueo_ponderado*0.5)+self.bloquea*.5 + self.jugadas_inteligentes*.3 + self.mulas_estrategicas/2
        
        

        return eval
    
    



class minimax_domino:
    
    def __init__(self, estado_inicial):
        self.raiz = nodo_minimax(estado_inicial)
        self.profundidad_max=4 #Esto dependerá de la capacidad de cada ordenador!
        
        
        
    def minimax(self, nodo, profundidad, es_maximizante):
        
        nodo.expandir()
        if profundidad == self.profundidad_max or len(nodo.hijos) == 0:
            
            #Medimos la probabilidad de respuesta, queremos beneficiar a los escenarios donde es baja la 
            #probabilidad de respuesta, por eso la modificamos.
            proba=nodo.get_probabilidad()
            nodo.set_probabilidad(1-proba*.5)
            nodo.valor_utilidad_final()
            return nodo.valor_utilidad

        if es_maximizante:
            #Aquí empezamos a maximizar
            max_eval = float("-inf")
            for hijo in nodo.hijos:
                eval = self.minimax(hijo, profundidad + 1, False)
                max_eval = max(max_eval, eval)
            return max_eval
        else:
            #Aquí minimizamos
            min_eval = float("inf")
            for hijo in nodo.hijos:
                eval = self.minimax(hijo, profundidad + 1, True)
                min_eval = min(min_eval, eval)
            return min_eval
        

    def encontrar_mejor_jugada(self, profundidad):
        #Primero expandimos el nodo para tener de dónde hacer nuestro análisis
        self.raiz.expandir()
        mejor_jugada = None
        
            #Para que busque en los hijos, primero expandimos el nodo
        mejor_eval=float('-inf')
        for hijo in self.raiz.hijos:
           
               eval = self.minimax(hijo, profundidad+1, True)
               if eval > mejor_eval:
                    mejor_eval = eval
                    mejor_jugada = hijo.estado_domino
          
        return mejor_jugada
    
    
    
    
    
    
    
    
#######################################################################################################
#######################################################################################################
#Pruebas
# Inicializar el juego
juego_domino = Domino()
juego_domino.inicializar()

#Esto es para la prueba
#fichas_jugador1= [0,2,4,12,15,20,18]
juego_domino.robar_inicial_j1()
jugador = int(input("¿Qué jugador inicia? "))
juego_domino.jugador = jugador

#Estos serán los numeros con los que tenemos registrados que el jugador pasó
num_pasa=[]

# Realizar una simulación de juego
while(True):
    
    if(juego_domino.jugador==1):
        # Obtener el estado actual del juego
        while(len(juego_domino.usabilidad_j1())==0):
            ficha_str=input("No tienes fichas jugables, roba 1 y dime qué ficha robaste en formato x,y ")
            num1, num2 = map(int, ficha_str.split(","))
            ficha = juego_domino.encontrar_ficha_roba(num1, num2)
            juego_domino.fichas.remove(ficha)
            juego_domino.fichasjugador1.append(ficha)
            juego_domino.cont1+=1
            if(len(juego_domino.fichas)-juego_domino.cont2==0):
                if(juego_domino.empate(1)):
                    print("El juego ha llegado a un empate, ámbos jugadores tendrán un punto.")
                    break
                    
            
        estado_actual = juego_domino
    
        # Crear un nodo minimax con el estado actual
        #nodo_actual = dm.nodo_minimax(estado_actual)
     
        # Determinar el mejor movimiento usando minimax
        minimax = minimax_domino(estado_actual)
        #Queremos saber en qué fichas el jugador 2 ha pasado y queremos que las recuerde cada vez que lo llamamos.
        if(len(num_pasa)!=0):
            minimax.raiz.actualizar_dicc_pasa(num_pasa[0],num_pasa[1])
        mejor_movimiento = minimax.encontrar_mejor_jugada(0)
    
        #Imprimir el estado actual del juego
        print("Estado actual del juego (antes de que jugador 1 haga su movimiento):", estado_actual.extremos)

        print("Mejor movimiento es jugar ", mejor_movimiento.imprime_ultima_jugada())
    
        # Realizar el mejor movimiento
        juego_domino.usarficha(mejor_movimiento.fichas_usadas[-1],0)
        juego_domino.jugador=2
            
        print("Última jugada realizada:")
        mejor_movimiento.imprime_ultima_jugada()
    else:
        if(len(juego_domino.usabilidad_j2())!=0):
            if len(juego_domino.fichas_usadas)!=0:
                robo=input("¿El jugador 2 robó? (y/n)")
                if(robo== 'Y' or robo== 'y'):
                   if(len(num_pasa)!=0): 
                        num_pasa[0]=juego_domino.extremos[0]
                        num_pasa[1]=juego_domino.extremos[1]
                   else:
                        num_pasa.append(juego_domino.extremos[0])
                        num_pasa.append(juego_domino.extremos[1])
                   cuantas=int(input("¿Cuántas veces? "))
                   for i in range(cuantas):
                       juego_domino.robar_ficha_j2()
                   tira=input("¿Pudo tirar? (y/n)")
                   if tira=='y' or tira=='Y':
                       tira=True
                   else:
                       tira=False
                       
                   if not tira:
                       if(juego_domino.empate(2)):
                            print("El juego ha llegado a un empate, ámbos jugadores tendrán un punto.")
                            break
        
        
            try:
                ficha_str=input('¿Qué ficha jugó el jugador 2? Escribela en formato x,y ')
                num1, num2 = map(int, ficha_str.split(","))
                ficha = juego_domino.encontrar_ficha(num1, num2)
                posicion=0
                if(len(juego_domino.fichas_usadas)!=0):
                    print('tablero es [0]=',juego_domino.extremos[0],' y [1]=',juego_domino.extremos[1])
                    posicion=int(input('¿En qué jugó? (1 o 0) '))
                    
                juego_domino.usarficha(ficha, posicion)        #Aquí debemos de jugar la ficha!
                juego_domino.jugador=1
                    
            except:
                print('Esa ficha no está dipsonible o no existe')
        else:
            juego_domino.cont2=len(juego_domino.fichas)
            juego_domino.jugador=1
            print("Jugador 2 no tiene ningúna ficha jugable, de haber fichas en el pozo robará todas y después va a pasar")
            
                
        print("Ultima jugada realizada: ",juego_domino.fichas_usadas[-1].__str__())
    
        # Verificar si hay un ganador
    
    ganador = juego_domino.ganador()
    if ganador == 2:
        print("¡Has ganado el juego!")
        break
    elif ganador == -2:
        print("El contrincante ha ganado el juego.")
        break
    print('Estado del tablero : ',juego_domino.extremos[0],',',juego_domino.extremos[1])

   



