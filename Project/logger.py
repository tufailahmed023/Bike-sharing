import logging
import os
from datetime import datetime

#File name 
Log_file_name =  f"{datetime.now().strftime('%m%d%Y__%H%M%S')}.log"

#Directory
Log_file_dir = os.path.join(os.getcwd(),"logs")

#Making the Dir
os.makedirs(Log_file_dir,exist_ok=True)

#Log file path
Log_file_path = os.path.join(Log_file_dir,Log_file_name)


logging.basicConfig(
    filename=Log_file_name,
    format= "[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)