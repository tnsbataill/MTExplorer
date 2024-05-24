"""general class for model"""
from model.bom import Bom
from model.boms import Boms

class Model:
    """Definition of main model class"""
    def __init__(self):
        self.bom = Bom()
        self.boms = Boms()
