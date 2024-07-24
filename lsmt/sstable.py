from dataclasses import dataclass
from loguru import logger
import glob
import json
from utils.model import Data

DATA_DIR = "/tmp"

@dataclass
class SSTable:

    def get_data(self, key):
        logger.info("Getting the data from SSTables for key: {}", key)
        # Step 1: Get all the index files -- ending in *.index
        for index_file in glob.glob(f"{DATA_DIR}/*.index"):
            logger.info("Reading file: {}", index_file)
            with open(index_file, "r") as fp_index_file:
                index_data = json.load(fp_index_file)
                if key in index_data:
                    logger.info("Found the {} in {}, starting at {} ending at {}", 
                                key, index_file, index_data[key]["start"], index_data[key]["end"])
                    data_file_name = str(index_file).split(".")[0] + ".data"
                    return self.read_data_file(data_file_name, index_data[key]["start"], index_data[key]["end"])
    

    def read_data_file(self, data_file, start_offset, end_offset):
        with open(data_file, "rb") as fp_data_file:
            fp_data_file.seek(start_offset)
            data_bytes = fp_data_file.read(end_offset - start_offset + 1)
            logger.info("Read {}", data_bytes.decode())
            data_split = data_bytes.decode().split(":")
            return Data(data_split[0], data_split[1], data_split[2])


    
