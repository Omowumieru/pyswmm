# ========================================================
# Some documentation and licensing info goes here probably
# ========================================================

# Local imports
from pyswmm.swmm5 import PYSWMMException
from pyswmm.toolkitapi import ObjectType

class Aquifers(object):
    """
    Aquifer Iterator Methods.

    :param object model: Open Model Instance
    """

    def __init__(self, model):
        if not model._model.fileLoaded:
            raise PYSWMMException("SWMM Model Not Open")
        self._model = model._model
        self._cuindex = 0
        self._nAquifers = self._model.getProjectSize(ObjectType.AQUIFER.value)
        
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
    
    def __next__(self):
        if self._cuindex < self._nAquifers:
            aquiferobject = self.__getitem__(self._aquiferid)
            self._cuindex += 1  # Next Iteration
            return aquiferobject
        else:
            raise StopIteration()
        
    @property
    def _aquiferid(self):
        """Aquifer ID."""
        return self._model.getObjectId(ObjectType.AQUIFER.value, self._cuindex)
    

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
        self._aquiferid = aquiferid

    # --- Get Parameters
    # -------------------------------------------------------------------------
    @property
    def aquiferid(self):
        """
        Get Aquifer ID.

        :return: Parameter Value
        :rtype: float

        Examples:

        >>> from pyswmm import Simulation, Aquifers
        >>>
        >>> with Simulation('tests/data/model_weir_setting.inp') as sim:
        ...     aq1 = Aquifers(sim)["Aq1"]
        ...     print(aq1.aquiferid)
        Aq1
        """
        return self._aquiferid