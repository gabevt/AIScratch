#=================================================================================
#=================================================================================
#Imports para el servidor
from __future__ import print_function
from __future__ import unicode_literals

import logging
import json
import os.path
import pprint
import uuid

import tornado.auth
import tornado.escape
import tornado.ioloop
from tornado.options import define, options
import tornado.web

from tornado import websocket
#---------------------------------------------------------------------------------
#Import BackEnd
from AISCRATCH import Back_End

from sklearn import datasets
import numpy as np
#---------------------------------------------------------------------------------

 
X = [ [0,0], [1,0], [0,1], [1,1]]
Y = [[0], [1], [1], [1] ]

_BE = Back_End()
#---------------------------------------------------------------------------------

PORT = 8888

define("port", default=PORT, help="run on the given port", type=int)

#=================================================================================
#=================================================================================

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html", messages=None) #Aqui pon la ruta del archivo


#=================================================================================
#=================================================================================

class AjaxHandler(tornado.web.RequestHandler):
    """Ajax handler"""
	#----------------------------------------------------
    
    def get(self):
        example_response = {}
        example_response['name'] = 'example'
        example_response['width'] = 1020

        self.write(json.dumps(example_response))
    
	#----------------------------------------------------
	
    def post(self):
        """AJAX POST"""
        #dic = tornado.escape.json_decode(self.request.body)
        dic= json.loads(self.request.body)
        print("\n\r---------------------------------------\n\r")
        response_to_send={}
        #----------------------------------------------------
        """TRAIN MODEL"""
        """TERMINADO"""		
        if dic['action'] == "Train_Model":
            print("ACTION -> ",dic['action'])
            model_config_aux= dic['model_config'].split(',')
            model_name=dic['model_name']
            dataset_name=dic['dataset_name']
            #####
            dataset_name= dataset_name.replace(" ","")
            aux= dataset_name.split('|')
            dataset_name= aux[0]
            features= aux[1]
            features= features.replace("Features:","")
            #print("DATASET ",dataset_name)
            #print("DATASET ",features)
            #input()
            ######
            try:
                epoch=int(dic['epoch'])
            except Exception as e:
                epoch=0
            if epoch:
                metric=dic['metric']
                config_validate,model_config=self.validate_model_config(model_config_aux)               
                if config_validate:
                    if model_config[0]==features and model_config[2]=="1":
                        X,Y=self.get_dataset(dataset_name)
                        if len(model_name):
                            train_validate,loss,acc=_BE.entrenar_modelo(model_name,model_config,X,Y,epoch)   
                        else:
                            train_validate,loss,acc=_BE.entrenar_modelo(None,model_config,X,Y,epoch)                        
                        if train_validate: 
                            print("\n\rMODEL_CONFIG -> ",model_config)
                            response_to_send['response']="TRAIN MODEL SUCCESSFUL" 
                            response_to_send['acc']=acc*100
                            response_to_send['loss']=loss*100 
                            #print("\n\rTRAIN MODEL SUCCESSFUL")                    
                        else:
                            response_to_send['response']="TRAIN MODEL UNSUCCESSFUL" 
                            #print("\n\rTRAIN MODEL UNSUCCESSFUL")
                    else:
                            response_to_send['response']="NUMBER OF NEURONS OF THE FIRST LAYER DOESN'T MATCH WITH THE NUMBER OF FEATURES" 
                            #print("\n\rNUMBER OF NEURONS OF THE FIRST LAYER DOESN'T MATCH WITH THE NUMBER OF FEATURES")
                else:
                    response_to_send['response']="NOT A VALID MODEL"
                    #print("\n\rNOT A VALID MODEL")
            else:
                response_to_send['response']="NOT A VALID EPOCH"
                #print("\n\rNOT A VALID EPOCH")
                
        #----------------------------------------------------
        """LOAD MODEL IN VIEW"""
        """TERMINADO"""		
        if dic['action'] == "Load_Model_View":
            print("ACTION -> ",dic['action'])
            model_name=dic['model_name']
            if _BE.database_find_model(model_name) is not None:            
                print("MODEL_NAME -> ",model_name)
                response_to_send['response']="LOAD MODEL IN VIEW SUCCESSFUL"
                response_to_send['config_model']= _BE.database_return_config(model_name)
                #print("LOAD MODEL IN VIEW SUCCESSFUL")                
            else:
                response_to_send['response']="MODEL DOESN'T EXIST"
                #print("MODEL DOESN'T EXIST")
        #----------------------------------------------------
        """LOAD MODEL GRAPH"""	
        """TERMINADO"""	
        if dic['action'] == "Load_Model_Graph":
            print("ACTION -> ",dic['action'])
            model_name=dic['model_name']		
            print("MODEL_NAME -> ",model_name)
            load_response=_BE.cargar_modelo(model_name)	
            if load_response:
                response_to_send['response']="LOAD GRAPH SUCCESSFUL"                
                #print("\n\rLOAD GRAPH SUCCESSFUL")
            else:
                response_to_send['response']="FILES DOESN'T EXIST"
                #print("\n\rFILES DOESN'T EXIST")
        #----------------------------------------------------	
        """SAVE MODEL IN MONGO DB"""
        """TERMINADO"""	
        if dic['action'] == "Save_Model_Mongo":
            print("ACTION -> ",dic['action'])            
            model_name=dic['model_name']
            if len(model_name):
                model_config_aux= dic['model_config'].split(',')
                config_validate,model_config=self.validate_model_config(model_config_aux)
                if config_validate:
                    model_name=dic['model_name']					
                    print("MODEL_NAME -> ",model_name)
                    print("MODEL_CONFIG -> ",model_config)	
                    _BE.database_insert_model(model_name,model_config)	
                    response_to_send['response']="SAVE MODEL IN MONGO DB SUCCESSFUL"
                    #print("\n\rSAVE MODEL IN MONGO DB SUCCESSFUL")
                else:
                    response_to_send['response']="NOT A VALID MODEL"
                    #print("\n\rNOT A VALID MODEL")		
            else:
                response_to_send['response']="NOT A VALID NAME"
               #print("\n\rNOT A VALID NAME")            
		#----------------------------------------------------
        """SAVE MODEL GRAPH"""
        """TERMINADO"""		
        if dic['action'] == "Save_Model_Graph":
            print("ACTION -> ",dic['action'])           
            model_name=dic['model_name']
            if len(model_name):
                model_config_aux= dic['model_config'].split(',')
                config_validate,model_config=self.validate_model_config(model_config_aux)
                if config_validate:					
                    print("MODEL_NAME -> ",model_name)
                    print("MODEL_CONFIG -> ",model_config)	
                    _BE.guardar_modelo(model_name,model_config)	
                    response_to_send['response']="SAVE MODEL GRAPH SUCCESSFUL"                   
                    #print("\n\rSAVE MODEL GRAPH SUCCESSFUL")
                else:
                    response_to_send['response']="NOT A VALID MODEL"
                    #print("\n\rNOT A VALID MODEL")
            else:
                response_to_send['response']="NOT A VALID NAME"
                #print("\n\rNOT A VALID NAME")
                

		#----------------------------------------------------
        print ("RESPONSE TO RETURN")
        pprint.pprint(response_to_send)
        print("\n\r---------------------------------------")
        # useful code goes here
        self.write(json.dumps(response_to_send))
        #self.finish()	
	#----------------------------------------------------
    """VALIDATE MODEL CONFIG"""	
    def validate_model_config(self,model_config_aux):
        if len(model_config_aux) >= 3:
            if ":" in model_config_aux[-1]:
                return 0,None
            else:		   
                model_config=["1","","1"]
                model_config[0]=model_config_aux[0]
                model_config[2]=model_config_aux[-1]
                del model_config_aux[0]
                del model_config_aux[-1]
				
                for i in range(len(model_config_aux)):
                    if i == 0:
                        model_config[1]+=model_config_aux[i]
                        if len(model_config_aux) >1:
                            model_config[1]+=","
                    if i>0 and i<(len(model_config_aux)-1):
                        model_config[1]+=model_config_aux[i]
                        model_config[1]+=","						
                    if i == (len(model_config_aux)-1) and i!=0:
                        model_config[1]+=model_config_aux[i]
                return 1,model_config		
        else:
            return 0,None
    #----------------------------------------------------
    """DATASET SELECT"""
    def get_dataset(self,dataset_name):
        if dataset_name == "Boston":
            dset = datasets.load_boston()
            X = dset.data
            Y = dset.target
        if dataset_name == "Iris":
            dset = datasets.load_iris()
            X = dset.data
            Y = dset.target
        if dataset_name == "Diabetes":
            dset = datasets.load_diabetes()
            X = dset.data
            Y = dset.target
        if dataset_name == "Digits":
            dset = datasets.load_digits()
            X = dset.data
            Y = dset.target
        if dataset_name == "Wine":
            dset = datasets.load_wine()
            X = dset.data
            Y = dset.target
        if dataset_name == "Breast_Cancer":
            dset = datasets.load_breast_cancer()
            X = dset.data
            Y = dset.target
        if dataset_name == "Or":
            X = np.array([ [0,0], [1,0], [0,1], [1,1]])
            Y = np.array([[0], [1], [1], [1] ])
        if dataset_name == "And":
            X = np.array([ [0,0], [1,0], [0,1], [1,1]])
            Y = np.array([[0], [0], [0], [1] ])
        if dataset_name == "Xor":
            X = np.array([[0., 0.], [0., 1.], [1., 0.], [1., 1.]])
            Y = np.array([[0.], [1.], [1.], [0.]])
        return X,Y.reshape(len(Y),1)
			
#=================================================================================
#=================================================================================

class Application(tornado.web.Application):

    def __init__(self):
        handlers= [
            (r'/', IndexHandler),
            (r'/ajax/',AjaxHandler)
        ]
        settings = dict(
            debug=True,
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static")
        )
        tornado.web.Application.__init__(self, handlers, **settings)			

#=================================================================================
#=================================================================================

def main():
    """start server"""
    tornado.options.parse_command_line()
    app = Application()
    app.listen(options.port)
    #print(PORT)
    tornado.ioloop.IOLoop.instance().start()
		
if __name__ == "__main__":
    main()
#=================================================================================
#=================================================================================