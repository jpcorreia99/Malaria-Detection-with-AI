import numpy as np
import pickle
import cv2, os, pickle
import random
import sklearn.model_selection
import matplotlib.pyplot as plt



categories = ["Uninfected","Parasitized"]
IMG_SIZE= 100

ORIGINAL_DATA_DIR = os.path.join(os.getcwd(),"malaria_cell_data")

SAVING_DIR = os.path.join(os.getcwd(),"dados_pickle_malaria") #folder onde guardar as imagens
try:
    os.mkdir(SAVING_DIR)
except FileExistsError:
    pass


def create_data(data_dir):
    data = []
    for category in categories:
        i=0
        path = os.path.join(data_dir,category)
        class_num = categories.index(category) #nós queremos que a nossa label seja 0-uninfected 1-Parasitized. Esta função devolve o indice da categoria que estamos a tratar de momento, que é a label
        for img in os.listdir(path): # devolve o nome de cada ficheiro existente nesse diretório
            try:
                print(i,class_num)
                i=i+1;
                img_array = cv2.imread(os.path.join(path,img), cv2.IMREAD_COLOR)#IMREAD_COLOR #vai ao endereço de cada imagem e devolve-a, convertida num array RGB
                img_array = cv2.resize(img_array,(IMG_SIZE,IMG_SIZE))
                img_array=img_array/255
                data.append([img_array,class_num])
            except Exception as e:
                pass

    random.shuffle(data)
    data = np.array(data)
    return data



def save_data(data):
    data_purposes = ["train","test"]

    train,test = sklearn.model_selection.train_test_split(data,test_size=.1) #10% para o tesTe
    data = [train,test]

    i=0
    for batch in data:
        print("data dir: "+data_purposes[i],", len :",len(batch))
        x=[]
        y=[]
        for features,label in batch:
            x.append(features)
            y.append(label)

        x = np.array(x).reshape(-1, IMG_SIZE, IMG_SIZE, 3)
        y = np.array(y)

        print(x.shape,y.shape)

        dir_to_save = os.path.join(SAVING_DIR,data_purposes[i])
        try:
            os.mkdir(dir_to_save)
        except FileExistsError:
            pass

        print(x.shape)
        pickle_out = open(dir_to_save+"/x.pickle","wb")
        pickle.dump(x,pickle_out)
        pickle_out.close()

        pickle_out = open(dir_to_save+"/y.pickle","wb")
        pickle.dump(y,pickle_out)
        pickle_out.close()
        i=i+1

print(os.path.join(SAVING_DIR,"train"))
data = create_data(ORIGINAL_DATA_DIR)
save_data(data)

plt.imshow((data[0])[0])
plt.show()

