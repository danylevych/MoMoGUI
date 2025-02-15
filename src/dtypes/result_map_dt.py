###########################################################################################
#                    ____                 _ _     __  __                                  #
#                   |  _ \ ___  ___ _   _| | |_  |  \/  | __ _ _ __                       #
#                   | |_) / _ \/ __| | | | | __| | |\/| |/ _` | '_ \                      #
#                   |  _ <  __/\__ \ |_| | | |_  | |  | | (_| | |_) |                     #
#                   |_| \_\___||___/\__,_|_|\__| |_|  |_|\__,_| .__/                      #
#                                                             |_|                         #
###########################################################################################

import pandas as pd

from momo.prototype import Prototype
from .similiraty_dt import SimilarityMenshureType


class ResultsMap:
    """
    ResultsMap is a data type that holds the results of the similarity menshure between systems.
    """
###########################################################################################
#
#                                       CONSTRUCTORS
#
    def __init__(self,
                 data: dict=None,
                 systems_names: list[str]|tuple[str]|set[str]=None,
                 systems: list[str]|tuple[str]|set[str]=None,
                 similarity_menshure: dict[tuple, float]=None,
                 prototype: Prototype=None,
                 similiraty_menshure_type: SimilarityMenshureType|str=None
                ):
        """
        Initialize the ResultsMap object.

        Parameters:
        -----------
        data : dict, optional
            A dictionary containing the data to initialize the object, need to have the
            following keys: 'systems_names', 'similarity_menshure', 'prototype', and
            'similarity_menshure_type'.

        systems_names :list[str]|tuple[str]|set[str], optional
            A list of strings representing the names of the systems.

        similarity_menshure : dict[tuple, float], optional
            A dictionary containing the similarity menshure between the systems.

        prototype : Prototype, optional
            A Prototype object representing the prototype of the systems.

        similiraty_menshure_type : SimilarityMenshureType|str, optional
            A SimilarityMenshureType object representing the type of similarity menshure.
        """
        self._init_empty()

        if data is not None:
            self._init_from_data(data, similiraty_menshure_type)

        elif ((systems_names is not None) and
              (similarity_menshure is not None) and
              (prototype is not None) and
              (similiraty_menshure_type is not None)):
            self._init_from_parts(systems_names,
                                  similarity_menshure,
                                  prototype,
                                  similiraty_menshure_type,
                                  systems
                                  )

    def _init_empty(self):
        """
        Initialize the ResultsMap object with empty data.
        """
        self._systems_names = []
        self._similarity_menshure = {}
        self._systems = []
        self._prototype = Prototype()
        self._similarity_menshure_type = SimilarityMenshureType.Sorensen_Dice

    def _init_from_data(self,
                        data: dict,
                        similiraty_menshure_type: SimilarityMenshureType|str
        ):
        """
        Initialize the ResultsMap object from a dictionary.

        Parameters:
        -----------
        data : dict
            A dictionary containing the data to initialize the object, need to have the
            following keys: 'systems_names', 'similarity_menshure', 'prototype', and
            'similarity_menshure_type'.

        similiraty_menshure_type : SimilarityMenshureType|str
            A SimilarityMenshureType object representing the type of similarity menshure.

        Raises:
        -------
        TypeError
            If data is not a dictionary.

        KeyError
            If data does not have the key 'systems_names', 'similarity_menshure', 'prototype', or
            'similarity_menshure_type'.
        """
        if not isinstance(data, dict):
            raise TypeError("Data should be a dictionary")

        if data.get("systems_names") is None:
            raise KeyError("Data should have a key 'systems_names'")

        if data.get("similarity_menshure") is None:
            raise KeyError("Data should have a key 'similarity_menshure'")

        if data.get("prototype") is None:
            raise KeyError("Data should have a key 'prototype'")

        if similiraty_menshure_type is None and data.get("similarity_menshure_type") is None:
            raise KeyError("Data should have a key 'similarity_menshure_type'")

        if similiraty_menshure_type is None:
            similiraty_menshure_type = data["similarity_menshure_type"]
        else:
            self._similarity_menshure = similiraty_menshure_type

        self.systems_names = data["systems_names"]
        self.similarity_menshure = data["similarity_menshure"]
        self.prototype = Prototype(data["prototype"])

    def _init_from_parts(self,
                         systems_names : list[str]|tuple[str]|set[str],
                         similarity_menshure : dict[tuple, float],
                         prototype : Prototype,
                         similiraty_menshure_type : SimilarityMenshureType|str,
                         systems: list[str]|tuple[str]|set[str]
                         ):
        """
        Initialize the ResultsMap object from its parts.

        Parameters:
        -----------

        systems_names : list[str]|tuple[str]|set[str]
            A list of strings representing the names of the systems.

        similarity_menshure : dict[tuple, float]
            A dictionary containing the similarity menshure between the systems.

        prototype : Prototype
            A Prototype object representing the prototype of the systems.
        """
        self.systems_names = systems_names
        self.similarity_menshure = similarity_menshure
        self.prototype = prototype
        self.similarity_menshure_type = similiraty_menshure_type
        self.systems = systems

#
#                                   END CONSTRUCTORS
#
###########################################################################################

###########################################################################################
#
#                                       PROPERTIES
#
    @property
    def systems(self) -> list[str]:
        """
        Get the systems.
        """
        return self._systems

    @property
    def systems_names(self) -> list:
        """
        Get the names of the systems.
        """
        return self._systems_names

    @property
    def similarity_menshure(self) -> dict[tuple, float]:
        """
        Get the similarity menshure between the systems.
        """
        return self._similarity_menshure

    @property
    def prototype(self) -> Prototype:
        """
        Get the prototype of the systems.
        """
        return self._prototype

    @property
    def similarity_menshure_type(self) -> SimilarityMenshureType:
        """
        Get the type of similarity menshure.
        """
        return self._similarity_menshure_type

    @property
    def data(self) -> dict:
        """
        Get the data of the ResultsMap object.
        """
        return {
            "systems_names": self._systems_names,
            "similarity_menshure": self._similarity_menshure,
            "prototype": self._prototype,
            "similarity_menshure_type": self._similarity_menshure_type
        }

    @property
    def results(self) -> pd.DataFrame:
        """
        Get the results of the similarity menshure between the systems.
        """
        columns = list(self._systems_names) + ["Similarity"]
        data = [(*list(combinations), similarity_result)
                for combinations, similarity_result in self._similarity_menshure.items()]

        return pd.DataFrame(data=data, columns=columns).sort_values(by="Similarity", ascending=False)

#
#                                   END PROPERTIES
#
###########################################################################################

###########################################################################################
#
#                                       SETTERS
#
    @systems.setter
    def systems(self, systems: list[str]|tuple[str]|set[str]):
        """
        Set the systems.

        Parameters:
        -----------
        systems : list|tuple|set
            A list of strings representing the names of the systems.

        Raises:
        -------
        TypeError
            If systems is not a list, tuple, or set.
        """
        if not isinstance(systems, (list, tuple, set)):
            raise TypeError("Systems should be a list, tuple, or set")

        self._systems = systems

    @systems_names.setter
    def systems_names(self, systems_names: list[str]|tuple[str]|set[str]):
        """
        Set the names of the systems.

        Parameters:
        -----------
        systems_names : list|tuple|set
            A list of strings representing the names of the systems.

        Raises:
        -------
        TypeError
            If systems_names is not a list, tuple, or set.
        """
        if not isinstance(systems_names, (list, tuple, set)):
            raise TypeError("Systems names should be a list, tuple, or set")

        self._systems_names = systems_names


    @similarity_menshure.setter
    def similarity_menshure(self, similarity_menshure: dict[tuple, float]):
        """
        Set the similarity menshure between the systems.

        Parameters:
        -----------
        similarity_menshure : dict[tuple, float]
            A dictionary containing the similarity menshure between the systems.

        Raises:
        -------
        TypeError
            If similarity_menshure is not a dictionary.

        TypeError
            If similarity_menshure is not a dictionary with keys as tuples and values as floats.
        """
        if not isinstance(similarity_menshure, dict):
            raise TypeError("Similarity menshure should be a dictionary")

        if (not all(isinstance(key, tuple) and isinstance(value, float)
            for key, value in similarity_menshure.items())
            ):
            raise TypeError("Similarity menshure should be a dict with keys as tuples and values as floats")

        self._similarity_menshure = similarity_menshure


    @prototype.setter
    def prototype(self, prototype: Prototype):
        """
        Set the prototype of the systems.

        Parameters:
        -----------
        prototype : Prototype
            A Prototype object representing the prototype of the systems.

        Risese:
        -------
        TypeError
            If prototype is not a Prototype object.
        """
        if not isinstance(prototype, Prototype):
            raise TypeError("Prototype should be a Prototype object")

        self._prototype = prototype


    @similarity_menshure_type.setter
    def similarity_menshure_type(self, similarity_menshure_type: SimilarityMenshureType|str):
        """
        Set the type of similarity menshure.

        Parameters:
        -----------
        similarity_menshure_type : SimilarityMenshureType|str
            A SimilarityMenshureType object representing the type of similarity menshure.

        Raises:
        -------
        TypeError
            If similarity_menshure_type is not a SimilarityMenshureType object or a string.
        """
        if not isinstance(similarity_menshure_type, (SimilarityMenshureType, str)):
            raise TypeError("Similarity menshure type should be a SimilarityMenshureType object or a string")

        self._similarity_menshure_type = similarity_menshure_type
#
#                                   END SETTERS
#
###########################################################################################
