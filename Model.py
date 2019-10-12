import tensorflow as tf
from tensorflow import keras
import numpy as np
import matplotlib.pyplot as plt
import pickle
import os

DATA_DIR= os.path.join(os.getcwd(),"dados_pickle_malaria")

#função responsável por carregar os dados que estão guardados em ficheiros sob o formato .pickle
def load_data():
    categories = ["test","train"]
    data = []
    i=0
    for category in categories:
        print(i)
        i=i+1
        dir_to_load = os.path.join(DATA_DIR,category)
        pickle_in = open(dir_to_load + "/x.pickle", "rb")
        x = pickle.load(pickle_in)
        pickle_in.close()
        x = x / 255 #normalização dos dados, para facilitar o treino da rede
        data.append(x)

        pickle_in = open(dir_to_load + "/y.pickle", "rb")
        y = pickle.load(pickle_in)
        pickle_in.close()
        data.append(y)

    return data


print("A carregar os dados, pode demorar um pouco...")
train_data, train_labels, test_data, test_labels = load_data()

try :
    model = keras.models.load_model("malaria_detecting_convet.h5")
except OSError as err:
    #building the model
    model = keras.models.Sequential()

    #Conv2D - layer convolucional, onde se aplicam filtros 3x3, criando 32 imagens diferentes
    model.add(keras.layers.Conv2D(32,(3,3), activation = "relu", input_shape=train_data[0].shape))
    model.add(keras.layers.MaxPooling2D((2,2)))  #layer de pooling, cada imagen será reduzida para metade do tamanho

    model.add(keras.layers.Conv2D(64,(3,3),activation="relu"))
    model.add(keras.layers.MaxPooling2D((2,2)))

    model.add(keras.layers.Conv2D(64,(3,3),activation="relu"))
    model.add(keras.layers.MaxPooling2D((2,2)))

    model.add(keras.layers.Flatten())
    model.add(keras.layers.Dense(256, activation = "relu"))

    model.add(keras.layers.Dense(1,activation="sigmoid")) # layer final que indicará se a célula está ou não infetada

    model.compile(optimizer = "adam", #algoritmo adam, de momento o que apresenta melhores métricas no treino de redes neuronais
                  loss ="binary_crossentropy", # pois é um problema de classificação binária
                  metrics=["accuracy"])

    print(model.summary())

    history = model.fit(train_data,
              train_labels,
              batch_size = 128,
              epochs = 15,
              validation_split=0.1) #10% dos dados serão usados para validação


    model.save("malaria_detection_simple_convet.h5")


    acc = history.history['acc']
    val_acc = history.history['val_acc']
    loss = history.history['loss']
    val_loss = history.history['val_loss']

    # gráfico da accuracy ao longo do tempo
    epochs = range(1, len(acc) + 1)
    plt.plot(epochs, acc, 'bo', label='Training acc')
    plt.plot(epochs, val_acc, 'b', label='Validation acc')
    plt.title('Training and validation accuracy')
    plt.legend()

    plt.figure()
    # gráfico da loss ao longo do tempo
    plt.plot(epochs, loss, 'bo', label='Training loss')
    plt.plot(epochs, val_loss, 'b', label='Validation loss')
    plt.title('Training and validation loss')
    plt.legend()
    plt.show()

test_loss, test_accuracy = model.evaluate(test_data,test_labels)

print("Resultados da rede em dados nunca antes vistos: \nLoss: ", test_loss,"\nAccuracy: ", test_accuracy)

