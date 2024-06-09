#!/usr/bin/env python
# -*- coding: utf-8 -*-

#LIBRERIAS
from random import seed
from random import random
from math import exp
import csv
import copy


#MODIFICAR outputfile PARA MODIFICAR EL NOMRE DEL FICHERO DE SALIDA
outputfile='resultado_entrenamiento.txt'
opf=open(outputfile,'w+')

# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- #

# 0.FILE READING
def load_csv(filename):
    datasetVP = list()
    archivo=open(filename)
    reader=csv.reader(archivo, delimiter=',')
    for row in reader:
        if not row:
            continue
        datasetVP.append(row) 
        #print(row)
    return datasetVP

    
def str_column_to_float(datasetVP,column):
    for row in datasetVP:
        row[column]=float(row[column].strip())
       

def str_column_to_int(datasetVP, column):
    class_values = [row[column] for row in datasetVP]
    unique = set(class_values)
    lookup = dict()
    for i, value in enumerate(unique):
        lookup[value] = i
    for row in datasetVP:
        row[column] = lookup[row[column]]
        #print(row)
    return lookup

# Find the min and max values for each column
def dataset_minmax(datasetVP):
    stats = [[min(column), max(column)] for column in zip(*datasetVP)]
    
    opf.write('VALORES MAX Y MIN PARA CADA PARÁMETRO DEl PATRÓN ENTRADA:\n')
    for values in stats:    
        opf.write(str(values[:]))

    return stats
 
# Rescale datasetVP columns to the range 0-1 
def normalize_dataset(datasetVP, minmax):
    for row in datasetVP:
        for i in range(len(row)-1):
            row[i] = (row[i] - minmax[i][0]) / (minmax[i][1] - minmax[i][0])  

# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- #

# 1.INITIALIZE A NETWORK
# Creates a new neural network ready for training. It accepts three parameters:
# 1. The number of inputs
# 2. The number of neurons to have in the hidden layer
# 3. The number of outputs
#
# For the hidden layer we create n_hidden neurons and each neuron in the hidden layer has n_inputs + 1 weights, 
# one for each input column in a data-set and an additional one for the bias.
# The output layer that connects to the hidden layer has n_outputs neurons, each with n_hidden + 1 weights. This means
# that each neuron in the output layer connects to (has a weight for) each neuron in the hidden layer.
def initialize_network(n_inputs, n_hidden, n_outputs):
    network = list()
    hidden_layer = [{'weights':[random() for i in range(n_inputs)]} for i in range(n_hidden)]
    network.append(hidden_layer)
    output_layer = [{'weights':[random() for i in range(n_hidden)]} for i in range(n_outputs)]
    network.append(output_layer)  


    #ESCRIBIMOS EN FICHERO LOS PESOS INICIALES (ALEATORIOS) EN LA ANN   
    opf.write('PESOS INICIALES CAPA OCULTA(Wij) - CAPA DE SALIDA (Wjk):\n')
    for layer in network:    
        opf.write(str(layer[:])+'\n')
    
    return network

# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- #

# 2.FORWARD PROPAGATE  
# 2.1 CALCULATE NEURON ACTIVATION FOR AN INPUT
def activate(weights, inputs):
    activation = weights[-1]
    for i in range(len(weights)-1):
        activation += weights[i] * inputs[i]    # Neuron activation is calculated as the weighted sum of the inputs. Where: 
                                                # - weight is a network weight
                                                # - input is an input
                                                # - i is the index of a weight or an input
                                                # The function assumes that the bias is the last weight in the list of weights.
    return activation

# 2.2 TRANSFER NEURON ACTIVATION
# transfer() function implements sigmoid function.
# The sigmoid activation function looks like an S shape, it's also called the logistic function. It can take any input value and produce
# a number between 0 and 1 on an S-curve. It is also a function of which we can easily calculate the derivative (slope) that we will need 
# later when backpropagating error.
def transfer(activation):
    return 1.0 / (1.0 + exp(-activation))

# 2.3 FORWARD PROPAGATE INPUT TO A NETWORK OUTPUT
# Function forward_propagate() implements the forward propagation for a row of data from our datasetVP with our neural network.
# Neuron's output value is stored in the neuron with the name 'output'. We collect the outputs for a layer in an array named
# new_inputs that becomes the array inputs and is used as inputs for the following layer.
def forward_propagate(network, row):
    inputs = row
    for layer in network:
        new_inputs = []
        for neuron in layer:
            activation = activate(neuron['weights'], inputs)
            neuron['output'] = transfer(activation)
            new_inputs.append(neuron['output'])
        inputs = new_inputs
    return inputs

# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- #

# 3.BACK PROPAGATE ERROR
# 3.1 CALCULATE THE DERIVATIVE OF AN NEURON OUTPUT
def transfer_derivative(output):
    return output * (1.0 - output)  # Error calculation for a given neuron.

# 3.2 ERROR BACKPROPAGATION
# Backpropagate error and store in neurons. Error signal calculated for each neuron is stored with the name 'delta'
def backward_propagate_error(network, expected):
    for i in reversed(range(len(network))):
        layer = network[i]
        errors = list()
        if i != len(network)-1:
            for j in range(len(layer)):
                error = 0.0
                for neuron in network[i + 1]:
                    error += (neuron['weights'][j] * neuron['delta'])
                errors.append(error)
        else:
            for j in range(len(layer)):
                neuron = layer[j]
                errors.append(expected[j] - neuron['output'])
        for j in range(len(layer)):
            neuron = layer[j]
            neuron['delta'] = errors[j] * transfer_derivative(neuron['output'])

# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- #

# 4.TRAIN NETWORK
# 4.1 UPDATE NETWORK WEIGHTS WITH ERROR
# Function update_weights() updates the weights for a network given an input row of data, a learning rate and assume that 
# a forward and backward propagation have already been performed.
def update_weights(network, row, l_rate):
    for i in range(len(network)):
        inputs = row[:-1]
        if i != 0:
            inputs = [neuron['output'] for neuron in network[i - 1]]
        for neuron in network[i]:
            for j in range(len(inputs)):
                neuron['weights'][j] += l_rate * neuron['delta'] * inputs[j]               
            neuron['weights'][-1] += l_rate * neuron['delta']

# 4.2 TRAIN A NETWORK FOR A FIXED NUMBER OF EPOCHS
# train_network() function implements the training of an already initialized neural network with a given training dataset, 
# learning rate, fixed number of epochs and an expected number of output values.
def train_network(network, datasetVP, l_rate, n_epoch, n_outputs):
    for epoch in range(n_epoch):
        sum_error = 0
        for row in datasetVP:
            outputs = forward_propagate(network, row)
            expected = [0 for i in range(n_outputs)]
            expected[row[-1]] = 1
            sum_error += sum([(expected[i]-outputs[i])**2 for i in range(len(expected))])
            backward_propagate_error(network, expected)
            update_weights(network, row, l_rate)
        opf.write('>>epoch=%d, error=%.3f\n' % (epoch, sum_error))


# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- #

# 5.PREDICT
# Make a prediction with a network
# Forward-propagate an input pattern to get an output is all we need to do to make a prediction.
# Function named predict() implements this procedure. It returns the index in the network output that has the largest probability.
def predict(network, row):
    outputs = forward_propagate(network, row)
    return outputs.index(max(outputs))

# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- #

# GETTERS PARA LA INTEGRACION CON LA INTERFAZ
def getOutputFile():
    return outputfile

# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- #

# Función ann_MAIN() donde se realiza el ENTRENAMIENTO COMPLETO, llamando al resto de funciones definidas previamente en este modulo de python
def complete_training(n_hidden,l_rate,n_epoch,dataset_selected):
    # Test training back-prop algorithm
    seed(1)
    
    datasetVP=list(dataset_selected)
    dataset_init=copy.deepcopy(dataset_selected)   #Este dataset_init contiene el dataset de entrada original sin normalizar que utilizaremos para mostrar las datos de las predicciones con las ubicaciones de los lanzamientos sin normalizar.
                                                #Hay que copiarlo de esta forma puesto que una lista es un objeto mutable y al normalizar datasetVP tambien lo hariamos con dataset_init
                                                #Ademas hay que tener en cuenta que cada elemento de la lista dataset_init es otra lista con los parametros de cada patron, por eso .deepcopy()
    
    opf.write('\n-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n')
    opf.write('RED NEURONAL ARTIFICIAL PARA EL ENTRENAMIENTO DE PORTEROS DE BALONMANO\n')
    opf.write('Autor: Inigo Rodriguez Sanchez\n')
    opf.write('-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n')
    opf.write('-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n\n')
    
    opf.write('PATRONES DE ENTRADA A LA RED NEURONAL [DISTANCIA(m), VELOCIDAD(km/h), x(m), y(m), RESULTADO DESEADO(0,1)]):\n') 
    
    for row in datasetVP:
        opf.write('[%s,%s,%s,%s,%s]' % (row[0],row[1],row[2],row[3],row[4]))     
    opf.write('\n\n-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n\n') 
    
    
    # PROCESAMOS LOS DATOS LEIDOS DEL .csv
    for k in range(len(datasetVP[0])-1):
        str_column_to_float(datasetVP, k)

    str_column_to_int(datasetVP, len(datasetVP[0])-1)
    
    # normalize input variables
    minmax = dataset_minmax(datasetVP)
    normalize_dataset(datasetVP, minmax)
    
    opf.write('\n\n-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n\n') 
    opf.write('PATRONES DE ENTRADA NORMALIZADOS A LA RED NEURONAL [DISTANCIA, VELOCIDAD, x, y, RESULTADO DESEADO]:\n')

    for row in datasetVP:
        opf.write('[%s,%s,%s,%s,%s]' % (row[0],row[1],row[2],row[3],row[4]))
    
    opf.write('\n\n-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n\n')
    opf.write('PARÁMETROS ESPECIFICADOS:\n')
    
    # INPUTS
    n_inputs = len(datasetVP[0])
    opf.write(' - Numero de neuronas en la capa de entrada: %d\n' %(n_inputs))
    
    # NEURONS OF THE HIDDEN LAYER
    #n_hidden = 3
    opf.write(' - Numero de neuronas en la capa oculta: %d\n' %(n_hidden))
    
    # OUTPUTS
    #n_outputs = len(set([row[-1] for row in datasetVP]))
    n_outputs = 2
    opf.write(' - Numero de neuronas en la capa de salida: %d\n' %(n_outputs))
    
    # LEARNING RATE
    #l_rate = 0.5    
    opf.write(' - Coeficiente de aprendizaje: %s\n' %(l_rate))
    
    # NUM OF EPOCHS
    #n_epoch = len(datasetVP)
    #n_epoch = 500
    opf.write(' - Numero de epochs (veces que ajustamos pesos): %d\n' %(n_epoch))
    
    opf.write('\n-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n\n')
    
    network = initialize_network(n_inputs, n_hidden, n_outputs)
    
    opf.write('\n-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n')
    
    
    opf.write('\nEVOLUCION DEL TÉRMINO DE ERROR COMETIDO A LA SALIDA DE LA RED\n')
    
    train_network(network, datasetVP, l_rate, n_epoch, n_outputs)
    
    opf.write('\n-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n')    
        
    #ESCRIBIMOS EN FICHERO LOS PESOS FINALES AJUSTADOS EN LA ANN
    opf.write('\nPESOS FINALES CAPA OCULTA(Wij) - CAPA DE SALIDA (Wjk):\n')
    for layer in network:    
        opf.write(str(layer[:])+'\n')  
         
    
    #ESCRIBIMOS EN FICHERO LAS PREDICCIONES REALIZADAS POR LA ANN
    opf.write('\n-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n')
    opf.write('\nPREDICCIONES REALIZADAS POR LA RED:\n')
    k=0     #Contador que se hara coincidir con el contador de rows del siguiente bucle for para situar en la misma posicion las listas datasetVP[] y dataset_init[] y poder sacar los resultados correctamente sin normalizar    
    cuentalanzamientos = 1
    cuentafallos = 0           #Variable para calcular el numero de predicciones erroneas
    dist_total = 0.00          #Variable para calcular el sumatorio de distancias y que posteriormente usaremos para calcular la distancia media
    vel_total = 0.00           #Variable para calcular el sumatorio de velocidades y que posteriormente usaremos para calcular la velocidad media

    for row in datasetVP:    
        prediction = predict(network, row)
        if row[-1]!=prediction:
            opf.write('(%d)--[x,y]: %f,%f  |  Distancia: %f  |  Velocidad: %f  |  Esperado: %d  |  Prediccion: %d  Predicción ERRÓNEA\n' % (cuentalanzamientos, float(dataset_init[k][2]), float(dataset_init[k][3]), float(dataset_init[k][0]), float(dataset_init[k][1]), row[-1], prediction))
            cuentafallos=cuentafallos+1
            
        else:
            opf.write('(%d)--[x,y]: %f,%f  |  Distancia: %f  |  Velocidad: %f  |  Esperado: %d  |  Prediccion: %d\n' % (cuentalanzamientos, float(dataset_init[k][2]), float(dataset_init[k][3]), float(dataset_init[k][0]), float(dataset_init[k][1]), row[-1], prediction))
            #opf.write('Expected=%d, Got=%d\n' % (row[-1], prediction))
        
        
        cuentalanzamientos = cuentalanzamientos+1
        dist_total = dist_total + float(dataset_init[k][0])
        vel_total = vel_total + float(dataset_init[k][1])
        k=k+1

       
    cuentalanzamientos = cuentalanzamientos-1   #Restamos 1 a cuentalanzamientos puesto que en el ultimo lanzamiento realizado le vuelve a sumar 1 debido al bucle implementado
    
    opf.write('\n-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n')
    
    opf.write('\nRESULTADOS FINALES:\n')
    opf.write(' ~ NÚMERO DE LANZAMIENTOS REALIZADOS: %d\n' % cuentalanzamientos)
    
    dist_media = dist_total / cuentalanzamientos    
    vel_media = vel_total / cuentalanzamientos
    opf.write('    ~ DISTANCIA MEDIA: ' + str(round(dist_media,2)) + ' metros\n')    
    opf.write('    ~ VELOCIDAD MEDIA: ' + str(round(vel_media,2)) + ' km/h\n\n')

    opf.write(' ~ PREDICCIONES REALIZADAS POR LA RED: %d\n' % cuentalanzamientos)
    cuentaaciertos = cuentalanzamientos - cuentafallos
    opf.write('    ~ ACERTADAS: %d\n'  % cuentaaciertos)
    opf.write('    ~ FALLIDAS: %d\n'  % cuentafallos)
    
    porcentaje_aciertos = round((100-((cuentafallos/cuentalanzamientos)*100)),2)
    porcentaje_fallos = round(((cuentafallos/cuentalanzamientos)*100),2)
 
    opf.write(' ~ PORCENTAJE DE ACIERTO: ' + str(porcentaje_aciertos) + '%\n')
    opf.write(' ~ PORCENTAJE DE FALLO: ' + str(porcentaje_fallos) + '%\n\n')
      
    opf.write('\n-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n')
    opf.write('-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n\n')
    
    opf.close()  #CERRAMOS FICHERO DE SALIDA CON LOS RESULTADOS DEL ENTRENAMIENTO
    
    '''
    print('----------------------------------------------------------------------------------------------------------------------------------------')
    print('¡Entrenamiento de la Red Neuronal Artificial realizado!')
    print('Consulta el fichero resultado_entrenamiento.txt para ver los resultados...'  )
    print('----------------------------------------------------------------------------------------------------------------------------------------')
    '''
# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- #
    
#PARA EJECUTAR SOLO LA RED NEURONAL ARTIFICIAL DESCOMENTAR LA SIGUIENTE LINEA ASI COMO LAS LINEAS INICIALIZACION DE LAS VARIABLES n_hidden, l_rate, n_epoch CONTENIDAS EN LA PROPIA FUNCION
#complete_training()

