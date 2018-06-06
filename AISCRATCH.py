#-------------------------------------
#python -m pip install pypiwin32
#python -m pip install tensorflow
#python -m pip install tflearn
#python -m pip install -U scikit-learn
#python -m pip install scipy
#python -m pip install pip
#python -m pip install certifi
#python -m pip install pymongo
#python -m pip install dnspython
#python -m pip install --upgrade pymongo
#-------------------------------------
#Esto era para el nodejs
#npm install mongodb
#-------------------------------------
import idna
import pymongo
import ssl
import certifi
from pymongo import MongoClient
import tflearn
import numpy as np
import array
import tensorflow as tf
import os

#================================================================================
#================================================================================
class MongoDB:	
	client=None
	db=None
	
	#----------------------------------------------------------------------------
	#Establecer Conexión con MongoDB en una Base de Datos
	def __init__(self,uri,database):
		self.client = MongoClient(uri)	#Conexión de MongoDB
		self.db= self.client[database]	#Selección de Base de Datos	
		
	#----------------------------------------------------------------------------
	#Insertar un documento en una tabla de la Base de Datos de MongoDB
	def query_insert_data(self,table,data):
		collection =self.db[table] 	#Seleccionar la Tabla
		collection.insert_one(data)	#Query de Insert
		
	#----------------------------------------------------------------------------
	#Insertar un documento en una tabla de la Base de Datos de MongoDB
	def query_update_data(self,table,data,newdata):
		collection =self.db[table]						#Seleccionar la Tabla
		collection.update_one(data,{"$set":newdata})	#Query de Update	
	
	#----------------------------------------------------------------------------
	#Buscar un documento o varios documentos segun la información dada en una tabla de la Base de Datos de MongoDB
	def query_find_data(self,table,data):
		collection =self.db[table]						#Seleccionar la Tabla
		cursor = collection.find_one(data)					#Buscar Documento/Query Select    
		return cursor
		'''
		for document in cursor:		
			print("\n\r-------------------------------------------")
			print("_id: ",document['_id'])								#Desplegado 
			print("NAME_MODEL: ",document['NAME_MODEL'])				#De
			print("CONFIG_MODEL: ",document['CONFIG_MODEL'])			#Información de
			print("ARCHIVE_PATH: ",document['ARCHIVE_PATH'])			#Documento(s)
		'''
	
	#----------------------------------------------------------------------------
	#Buscar un Documento y regresar CONFIG_MODEL
	def query_return_config(self,table,data):	
		collection =self.db[table]				#Seleccionar la Tabla
		cursor = collection.find_one(data)		#Buscar Documento/Query Select
		config= cursor['CONFIG_MODEL']			#Seleccionar CONFIG_MODEL
		return config	
	
	#----------------------------------------------------------------------------
	#Buscar un Documento y regresar ARCHIVE_PATH
	def query_return_filepath(self,table,data):
		collection =self.db[table]				#Seleccionar la Tabla
		cursor = collection.find_one(data)		#Buscar Documento/Query Select
		filepath=cursor['ARCHIVE_PATH']			#Seleccionar ARCHIVE_PATH
		return filepath	
	
	#----------------------------------------------------------------------------
	#Buscar un Documento y regresar NAME_MODEL
	def query_return_name_model(self,table,data):
		collection =self.db[table]				#Seleccionar la Tabla
		cursor = collection.find_one(data)		#Buscar Documento/Query Select
		name_model=cursor['NAME_MODEL']			#Seleccionar NAME_MODEL
		return name_model
	
	#----------------------------------------------------------------------------	
	#Buscar un Documento y eliminarlo de la table de la Base de Datos de MongoDB
	def query_delete_data(self,table,data):
		collection =self.db[table]				#Seleccionar la Tabla
		collection.delete_one(data)				#Eliminar Documento

#================================================================================
#================================================================================	
class MyCallback(tflearn.callbacks.Callback):
    def __init__(self):
        self.accs = []
        self.loss =[]
    
    def on_epoch_end(self, training_state):
        """ """
        self.accs.append(training_state.acc_value)
        self.loss.append(training_state.global_loss)
			
class Red_Neuronal:
	model=None
	configuracion=None		
	
	#----------------------------------------------------------------------------
	#Ensamblado de un Modelo de Red Neuronal
	def __init__(self,config):	
		self.configuracion=config		
		
		tnorm = tflearn.initializations.uniform(minval=-1., maxval=1.)
		
		NN = tflearn.input_data(shape=[None, int(self.configuracion[0])])		#Configuración de la Capa de Entrada
		
		parameters_hiddens=self.configuracion[1].split(',')						#Separar el String para la Configuración de las Capas Ocultas
		
		for i in range(len(parameters_hiddens)):				
			aux=parameters_hiddens[i].split(':')								#Separar el String para obtener la neuronas y función de activación
			NN=self.conectar(NN,int(aux[0]),aux[1],tnorm)						#Configuración de las Capas Ocultas
			
		NN= tflearn.fully_connected(NN, n_units=int(self.configuracion[2]),activation=None, name='output',  weights_init=tnorm) #Configuración de la Capa de Salida
		
		regression = tflearn.regression(NN, optimizer='sgd', loss='mean_square',
								metric='R2', learning_rate=0.65)
		self.model= tflearn.DNN(regression)
		
	#----------------------------------------------------------------------------
	#Ensamblado entre Capas	
	def conectar(self,capa_ant,neuronas,func_activacion,tnorm):
		return tflearn.fully_connected(capa_ant, n_units=neuronas, activation=func_activacion, weights_init=tnorm)
		
	#----------------------------------------------------------------------------
	#Entrenamiento de un Modelo de Red Neuronal
	def entrenar(self,X,Y,epocas):  
		cb= MyCallback() 
		self.model.fit(X,Y,n_epoch=epocas,show_metric=True, snapshot_epoch=False,callbacks=cb)
		acc=cb.accs[-1]
		loss=cb.loss[-1]
		cb=None        
		#print("\n\r Acc ",acc)
		#print("\n\r Loss ",loss) 
		return loss,acc      
        
	#----------------------------------------------------------------------------
	#Evaluación de un Modelo de Red Neuronal
	def evaluar(self,Y):
		return self.model.predict(Y)
		
	#----------------------------------------------------------------------------
	#Guarda un Modelo de Red Neuronal
	def guardar(self,filepath):
		self.model.save(filepath)
		
	#----------------------------------------------------------------------------
	#Cargar un Modelo de Red Neuronal
	def cargar(self,filepath):
		self.model.load(filepath)		

#================================================================================
#================================================================================
	
class Back_End:
    mongo_database=None
    my_model=None
	
	#----------------------------------------------------------------------------
	
    def __init__(self):	
        uri="mongodb+srv://Usuario:12345@clusteria-higk8.mongodb.net/"			#Link/Ruta con el Host de la Base de Datos de MongoDB
        self.mongo_database=MongoDB(uri,"AISCRATCH")
        print("\n\r---------------------------------------\n\r")
        print("BACK_END INIT")
        print("\n\r---------------------------------------")

	#----------------------------------------------------------------------------
	
    def database_insert_model(self,model_name,model_config):
        default_path="C:/Users/"+os.environ.get('USERNAME')+"/AISCRATCH/MODELS/"+model_name+"/"		#Ruta Default para guardar los archivos
        if not os.path.exists(default_path):									#Comprobar si existe la Ruta
            os.makedirs(default_path)											#Crear la Ruta (Carpetas) 
		
        document={"NAME_MODEL":model_name,"CONFIG_MODEL":model_config,"ARCHIVE_PATH":default_path+model_name+".tfl"} 	#Auxiliar de para Insertar el Documento
		
        try:
            self.mongo_database.query_insert_data("MODELS",document)													#Query de Insert
        except Exception as e:
            #print (str(e))
            prev_config=self.mongo_database.query_return_config("MODELS",{"NAME_MODEL":model_name})						#En caso de Existir hacer un Update
            if prev_config!=model_config:
                self.mongo_database.query_update_data("MODELS",{"NAME_MODEL":model_name},{"CONFIG_MODEL":model_config})	#En caso de que se Modifico
                for file in os.listdir(default_path):																	#la configuracion
                    file_path = os.path.join(default_path, file)														#eliminar los datos anteriores para evitar conflictos	
                    try:																								#cuando se quiera cargar un modelo
                        if os.path.isfile(file_path):
                            os.unlink(file_path)
                        #elif os.path.isdir(file_path): shutil.rmtree(file_path)
                    except Exception as f:
                        print(f)
						
	#----------------------------------------------------------------------------
	#Ensamblado/Generación de un Modelo de Red Neuronal				
    def generar_modelo(self,model_name):		
        tf.reset_default_graph()
        model_config= self.mongo_database.query_return_config("MODELS",{"NAME_MODEL":model_name})
        self.my_model= Red_Neuronal(model_config)	
		
	#----------------------------------------------------------------------------
	#Entrenamiento de un Modelo de Red Neuronal	
    def entrenar_modelo(self,model_name,model_config,X,Y,epocas):	
        tf.reset_default_graph()
        if model_name is not None:
            if model_config == self.mongo_database.query_return_config("MODELS",{"NAME_MODEL":model_name}):
                if self.cargar_modelo(model_name)==0:
                    self.my_model= Red_Neuronal(model_config)
            else:
                self.my_model=Red_Neuronal(model_config)
        else:       
            self.my_model= Red_Neuronal(model_config)	
        flag=1
        try:
            loss,acc=self.my_model.entrenar(X,Y,epocas)
        except Exception as e:
            flag=0
        return flag,loss,acc

	#----------------------------------------------------------------------------
	#Evaluacion de un Modelo de Red Neuronal
    def evaluar_modelo(self,Y):
        return self.my_model.evaluar(Y)
	
	#----------------------------------------------------------------------------
	#Preprocesamiento de un Dataset
    def modificar_dataset(self):
        #FALTA AGREGAR ESTO
        print("")	
		
	#----------------------------------------------------------------------------
	#Guardar un Modelo de Red Neuronal	
    def guardar_modelo(self,model_name,model_config):
        if self.database_find_model(model_name) is None:
            self.database_insert_model(model_name,model_config)
        if self.my_model is not None:
            self.my_model.guardar(self.mongo_database.query_return_filepath("MODELS",{"NAME_MODEL":model_name}))
            return 1
        else:
            return 0
        
	
	#----------------------------------------------------------------------------
    #Cargar un Modelo de Red Neuronal    
    def cargar_modelo(self,model_name):	
        if self.database_find_model(model_name) is not None:
            dir=self.mongo_database.query_return_filepath("MODELS",{"NAME_MODEL":model_name})
            dir=dir.replace(model_name+".tfl","")
            list=os.listdir(dir)
            if len(list):#Comprobar si existen archivos                
                self.generar_modelo(model_name)
                self.my_model.cargar(self.mongo_database.query_return_filepath("MODELS",{"NAME_MODEL":model_name}))		#Si existen, cargar el Modelo de Red Neuronal
                return 1
            else:
                return 0
        else:
            return 0

	#----------------------------------------------------------------------------			
    def database_find_model(self,model_name):
        return self.mongo_database.query_find_data("MODELS",{"NAME_MODEL":model_name})
        
	#----------------------------------------------------------------------------	
    def database_return_config(self,model_name):
        return self.mongo_database.query_return_config("MODELS",{"NAME_MODEL":model_name})
     

		
#================================================================================
#================================================================================	


'''
#--------------------------------------------------
#Iniciar BacbEnd y sus funcionalidades
BD= Back_End()

#--------------------------------------------------
#Insertar un documento
model_name="OR_MODEL"
model_config=["2","2:linear","1"]
BD.database_insert_model(model_name,model_config)

#--------------------------------------------------
#Información de prueba
X = [ [0,0], [1,0], [0,1], [1,1]]
Y = [[0], [1], [1], [1] ]

#--------------------------------------------------

#BD.generar_modelo(model_name)
if BD.cargar_modelo(model_name):
    print("SUCCESSFUL")
else:	
    print("UNSUCCESSFUL")
BD.entrenar_modelo(model_config,X,Y,50)
input()
print("0 or 0:", BD.evaluar_modelo([[0., 0.]]))
print("0 or 1:", BD.evaluar_modelo([[0., 1.]]))
print("1 or 0:", BD.evaluar_modelo([[1., 0.]]))
print("1 or 1:", BD.evaluar_modelo([[1., 1.]]))
input()
if BD.guardar_modelo(model_name,model_config):
    print("SUCCESSFUL")
else:	
    print("UNSUCCESSFUL")
BD.cargar_modelo(model_name)
BD.entrenar_modelo(model_config,X,Y,50)
'''
#--------------------------------------------------
#Otros Documentos
#{"NAME_MODEL":"XOR_MODEL","CONFIG_MODEL":["2","5:sigmoid","1"],"ARCHIVE_PATH":"C:/Users/Alberto/AISCRATCH/XOR_MODEL.tfl"}
#{"NAME_MODEL":"AND_MODEL","CONFIG_MODEL":["2","1:linear","1"],"ARCHIVE_PATH":"C:/Users/Alberto/AISCRATCH/AND_MODEL.tfl"}

#--------------------------------------------------








