import os , sys
from Project.logger import logging
from Project.exception import BikeException
from Project.entity import input, output
from Project.predictor import ModelResolver
from Project import utils
class ModelPusher:
    def __init__(self,
                 model_pusher_input: input.model_pusher_input,
                 data_tranformation_output:output.data_tranformation_output,
                 model_training_output: output.model_training_output):
        try:
            logging.info(f"{'--'*20} MODEL PUSHER {'--'*20}")
            self.model_pusher_input = model_pusher_input
            self.data_tranformation_output = data_tranformation_output
            self.model_training_output = model_training_output
            self.model_resolver = ModelResolver()
        except Exception as e:
            print(BikeException(e, error_detail = sys))

    def start_model_pusher(self,):
        try:

            logging.info("pushing model and transformer to saved model folder")
            logging.info("getting new model folder path")
            model_path = self.model_resolver.create_new_model_dir()
            logging.info("getting new tranformer folder path")
            tranformer_path = self.model_resolver.create_new_transformer_dir()

            logging.info("loading tranformer and model")
            tranformer = utils.load_object(self.data_tranformation_output.tranfomer_path)
            model = utils.load_object(self.model_training_output.model_file_path)

            logging.info("saving both model and transformer")
            utils.save_object(tranformer_path, tranformer)
            utils.save_object(model_path, model)

            model_pusher_output = output.model_pusher_output(saved_models_dir = self.model_pusher_input.Saved_models_dir)
            logging.info(f"Model pusher output: {model_pusher_output}")
            return model_pusher_output
            
        except Exception as e:
            print(BikeException(e, error_detail = sys))