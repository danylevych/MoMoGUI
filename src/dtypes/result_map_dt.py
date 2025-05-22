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
from momo.model import MultiSystemModel
from momo.system_models.system_models import SystemModel
from .similiraty_dt import SimilarityMenshureType


class ResultsMap:
    """
    ResultsMap is a data type that holds the results of the similarity measure between systems.
    It stores the essential data without UI components and provides methods to access the data
    in different formats.
    """

    def __init__(self,
                data: dict = None,
                systems: MultiSystemModel = None,
                similarity_measures: dict[tuple, float] = None,
                prototype: Prototype = None,
                similarity_measure_type: SimilarityMenshureType|str = None
                ):
        """
        Initialize the ResultsMap object.

        Parameters:
        -----------
        data : dict, optional
            A dictionary containing the data to initialize the object.

        systems : MultiSystemModel, optional
            MultiSystemModel containing all the systems data

        similarity_measures : dict[tuple, float], optional
            A dictionary containing the similarity measure between the systems.

        prototype : Prototype, optional
            A Prototype object representing the prototype of the systems.

        similarity_measure_type : SimilarityMenshureType|str, optional
            Type of similarity measure used.
        """
        self._init_empty()

        if data is not None:
            self._init_from_data(data, similarity_measure_type)
        elif all(x is not None for x in [systems, similarity_measures, prototype, similarity_measure_type]):
            self._init_from_parts(systems, similarity_measures, prototype, similarity_measure_type)

    def _init_empty(self):
        """Initialize with empty data"""
        self._systems = MultiSystemModel()
        self._similarity_measures = {}
        self._prototype = Prototype()
        self._similarity_measure_type = SimilarityMenshureType.Sorensen_Dice

    def _init_from_data(self, data: dict, similarity_measure_type: SimilarityMenshureType|str = None):
        """Initialize from a data dictionary"""
        if not isinstance(data, dict):
            raise TypeError("Data should be a dictionary")

        required_keys = ["systems", "similarity_measures", "prototype"]
        for key in required_keys:
            if data.get(key) is None:
                raise KeyError(f"Data should have a key '{key}'")

        if similarity_measure_type is None and data.get("similarity_measure_type") is None:
            raise KeyError("Data should have a key 'similarity_measure_type'")

        self._systems = data["systems"]
        self._similarity_measures = data["similarity_measures"]
        self._prototype = Prototype(data["prototype"])
        self._similarity_measure_type = similarity_measure_type or data["similarity_measure_type"]

    def _init_from_parts(self,
                        systems: MultiSystemModel,
                        similarity_measures: dict[tuple, float],
                        prototype: Prototype,
                        similarity_measure_type: SimilarityMenshureType|str):
        """Initialize from individual components"""
        self._systems = systems
        self._similarity_measures = similarity_measures
        self._prototype = prototype
        self._similarity_measure_type = similarity_measure_type

    @property
    def systems_names(self) -> list[str]:
        """Get list of system names"""
        return self._systems.get_system_names()

    @property
    def systems(self) -> MultiSystemModel:
        """Get the systems model"""
        return self._systems

    @property
    def similarity_measures(self) -> dict[tuple, float]:
        """Get the similarity measures between systems"""
        return self._similarity_measures

    @property
    def prototype(self) -> Prototype:
        """Get the prototype"""
        return self._prototype

    @property
    def similarity_measure_type(self) -> SimilarityMenshureType:
        """Get the similarity measure type"""
        return self._similarity_measure_type

    @property
    def data(self) -> dict:
        """Get all data as a dictionary"""
        return {
            "systems": self._systems,
            "similarity_measures": self._similarity_measures,
            "prototype": self._prototype,
            "similarity_measure_type": self._similarity_measure_type
        }

    @property
    def results(self) -> pd.DataFrame:
        """Get results as a pandas DataFrame"""
        columns = list(self.systems_names) + ["Similarity"]
        data = [(*list(combinations), similarity_result)
                for combinations, similarity_result in self._similarity_measures.items()]
        return pd.DataFrame(data=data, columns=columns).sort_values(by="Similarity", ascending=False)

    def to_excel(self, file_path: str) -> None:
        """
        Save all data to an Excel file, including system states and results

        Parameters:
        -----------
        file_path : str
            Path to save the Excel file
        """
        with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
            metadata = pd.DataFrame([{
                'file_type': 'MoMo_Results',
                'version': '1.0',
                'date': pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S'),
                'similarity_measure_type': self.similarity_measure_type
            }])
            metadata.to_excel(writer, sheet_name='Metadata', index=False)
            self.results.to_excel(writer, sheet_name="Similarity_Results", index=False)

            # Save prototype in correct format
            prototype_df = pd.DataFrame({
                'Name': ['Sheet1'] + [None] * (len(self.prototype) - 1),
                'Feature': self.prototype.index,
                'State': self.prototype.values
            })
            self.prototype.to_excel(writer, sheet_name="Prototype")

            for system_name in self.systems_names:
                system = self._systems.systems.get(system_name)
                if system is not None:
                    system.data.to_excel(writer, sheet_name=f"System_{system_name}")

    @classmethod
    def from_excel(cls, file_path: str):
        """
        Load results from an Excel file

        Parameters:
        -----------
        file_path : str
            Path to the Excel file containing saved results

        Returns:
        --------
        ResultsMap
            A new ResultsMap object with the loaded data
        """
        def is_valide_file(file_path: str) -> bool:
            """Check if the file is a valid results file"""
            try:
                excel_file = pd.ExcelFile(file_path)
                if "Metadata" in excel_file.sheet_names:
                    metadata = pd.read_excel(file_path, sheet_name="Metadata")
                    return "file_type" in metadata.columns and "MoMo_Results" in metadata["file_type"].values
                return False
            except Exception as e:
                print(f"Error validating file: {e}")
                return False


        def load_prototype_data(file_path: str) -> Prototype:
            """Read prototype data from the Excel file"""
            prototype_df = pd.read_excel(file_path, sheet_name="Prototype", index_col=(0, 1))
            return Prototype(prototype_df.iloc[:, 0].values, index=prototype_df.index)


        def load_systems_data(file_path: str) -> list[SystemModel]:
            """Read systems data from the Excel file"""
            systems_data = []
            with pd.ExcelFile(file_path) as excel_file:
                for sheet_name in excel_file.sheet_names:
                    if sheet_name.startswith("System_"):
                        sheet_data = excel_file.parse(sheet_name, index_col=0)
                        system_name = sheet_name.replace("System_", "")
                        systems_data.append(SystemModel(system_name, sheet_data))

            return systems_data

        def load_similarity_measures(file_path: str) -> dict[tuple, float]:
            """Read similarity measures from the Excel file"""
            results_df = pd.read_excel(file_path, sheet_name="Similarity_Results", header=0)
            similarity_measures = {}

            for _, row in results_df.iterrows():
                combination = tuple(row.iloc[:-1].values)
                similarity = float(row.iloc[-1])
                print(f"Combination: {combination}, Similarity: {similarity}")
                similarity_measures[combination] = similarity

            return similarity_measures

        def load_similarity_measure_type(file_path: str) -> SimilarityMenshureType:
            """Read similarity measure type from the Excel file"""
            metadata_df = pd.read_excel(file_path, sheet_name="Metadata")
            if 'similarity_measure_type' in metadata_df.columns:
                return SimilarityMenshureType(metadata_df['similarity_measure_type'].iloc[0])
            return SimilarityMenshureType.Sorensen_Dice

        try:
            if not is_valide_file(file_path):
                raise ValueError("Invalid results file format")

            systems = MultiSystemModel(load_systems_data(file_path))
            print(f"Loaded systems:\n {systems}")

            similarity_measures = load_similarity_measures(file_path)
            print(f"Loaded similarity measures:\n {similarity_measures}")

            prototype = load_prototype_data(file_path)
            print(f"Loaded prototype:\n {prototype}")

            similarity_measure_type = load_similarity_measure_type(file_path)
            print(f"Loaded similarity measure type from the file: {similarity_measure_type}")

            return cls(
                systems=systems,
                similarity_measures=similarity_measures,
                prototype=prototype,
                similarity_measure_type=similarity_measure_type,
            )
        except Exception as e:
            raise ValueError(f"Failed to load results: {str(e)}")
