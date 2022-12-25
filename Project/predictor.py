import os
from Project.entity.input import MODEL_NAME,TRANSFORMER_NAME
from glob import glob 
from typing import Optional


class ModelResolver:
    def __init__(self, model_regestry = "Saved_models",
                       model_dir = "model" , transformer_dir= "transformer"):
        
        self.model_regestry = model_regestry
        self.model_dir = model_dir
        self.transformer_dir = transformer_dir
        os.makedirs(self.model_regestry, exist_ok=True)


    def latest_dir_path(self):
        """This function return the latest folder path in saved folder, if no folder
        exist it will resturn None

        Returns:
            if folder exist then path to that folder else None
        """
        try:
            dir_names = os.listdir(self.model_regestry)
            if len(dir_names) == 0:
                return None
            dir_names = list(map(int,dir_names))
            latest_dir = max(dir_names)
            return os.path.join(self.model_regestry,f"{latest_dir}")
        except Exception as e:
            print(e)
    
    def latest_model_path(self,):
        """ This function will call the latest_dir_path.It will return the model.pkl file inside it on model folder.
        if no dir exist inside the saved folder then it will raise an exception.

        Raises:
            Exception: if no folder inside the saved folder.

        Returns:
            path to the model.pkl file
        """
        try:
            get_dir = self.latest_dir_path()
            if not get_dir:
                raise Exception("NO MODEL EXIST")
            return os.path.join(get_dir,self.model_dir,MODEL_NAME)
        except Exception as e:
            print(e)
            
    def latest_transformer_path(self,):
        """ This function will call the latest_dir_path.It will return the transformer.pkl file inside  on tranformer folder.
        if no dir exist inside the saved folder then it will raise an exception.

        Raises:
            Exception: if no folder inside the saved folder.

        Returns:
            path to the transformer.pkl file
        """
        try:
            get_dir = self.latest_dir_path()
            if not get_dir:
                raise Exception("NO TRANSFORMER EXIST")
            return os.path.join(get_dir,self.transformer_dir,TRANSFORMER_NAME)
        except Exception as e:
            print(e)
        
    def create_new_dir(self,):
        try:
            get_dir = self.latest_dir_path()
            if not get_dir:
                return os.path.join(self.model_regestry,f"{0}")
            get_dir_base_name = int(os.path.basename(get_dir))
            return os.path.join(self.model_regestry,f"{get_dir_base_name + 1}")
        except Exception as e:
            print(e)

    def create_new_model_dir(self,):
        try:
            get_dir = self.create_new_dir()
            return os.path.join(get_dir,self.model_dir,MODEL_NAME)
        except Exception as e:
            print(e)


    def create_new_transformer_dir(self,):
        try:
            get_dir = self.create_new_dir()
            return os.path.join(get_dir,self.transformer_dir,TRANSFORMER_NAME)
        except Exception as e:
            print(e)