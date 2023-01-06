import json
import main.db_service as dbs
from abc import *


class environment(metaclass=ABCMeta):
    @classmethod
    def __start__(self):
        self.STATUS = "INIT"
        self.db = dbs.db()
        self.global_tick_cnt = 0

    @classmethod
    def __init__(self):
        self.__reset__()

    @classmethod
    def __reset__(self):
        self.STATUS = "RUNNING"
        return(self.__output__())

    #@abstractmethod
    #def reset(self):
     #   return

    @classmethod
    def __step__(self):
        return(self.__output__())

    #@abstractmethod
    #def step(self):
     #   return

    @classmethod
    def __get_state__(self):
        self.state = self.db.read_db('STATE')
        return self.state.head()

    @classmethod
    def __write_state__(self, data):
        return self.db.write_db('STATE', data)

    @classmethod
    def __output__(self):
	self.global_tick_cnt += 1    
    	return({'status': self.STATUS, 'output': [str(self.global_tick_cnt)]})

    @classmethod
    def __end__(self):
        self.STATUS = "DONE"


if __name__ == '__main__':
    e = environment()
