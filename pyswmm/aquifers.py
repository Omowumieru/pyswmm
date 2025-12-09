# ========================================================
# Some documentation and licensing info goes here probably
# ========================================================

# Local imports
from pyswmm.swmm5 import PYSWMMException
from pyswmm.toolkitapi import ObjectType

class Aquifers(object):
    def __init__(self, model):
        if not model._model.fileLoaded:
            raise PYSWMMException("SWMM Model Not Open")
        self._model = model._model
        self._cuindex = 0
        self._nAquifers = self._model.getProjectSize(ObjectType.AQUIFER.value)

    # Use this to verify that I know how python scripts work
    def check_py(self):
        print("Whoa. It's pretty wet in these voids!")
        
    def __len__(self):
        """
        Return number of aquifers.

        Use the expression 'len(Aquifers)'.

        :return: Number of Aquifers
        :rtype: int

        """
        return self._model.getProjectSize(ObjectType.AQUIFER.value)

    def __contains__(self, aquiferid):
        """
        Checks if Aquifer ID exists.

        :return: ID Exists
        :rtype: bool
        """
        return self._model.ObjectIDexist(ObjectType.AQUIFER.value, aquiferid)
    
    def __getitem__(self, aquiferid):
        if self.__contains__(aquiferid):
            return Aquifer(self._model, aquiferid)
        else:
            raise PYSWMMException("Aquifer ID Does not Exist")

    def __iter__(self):
        return self
    

class Aquifer(object):
    """
    Aquifer Methods.

    :param object model: Open Model Instance
    :param str aquiferid: Aquifer ID


    """
         
    def __init__(self, model, aquiferid):
        if not model.fileLoaded:
            raise PYSWMMException("SWMM Model Not Open")
        if aquiferid not in model.getObjectIDList(ObjectType.AQUIFER.value):
            raise PYSWMMException("ID Not valid")
        self._model = model
        self.aquiferid = aquiferid