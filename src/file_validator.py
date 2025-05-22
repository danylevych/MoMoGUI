from abc import ABC, abstractmethod
import pandas as pd
from momo.system_models.system_models import SystemModel
from src.dtypes import ResultsMap


class FileValidator(ABC):
    @abstractmethod
    def validate(self, file_path):
        pass

    @abstractmethod
    def get_systems_data(self, file_path):
        pass


class ExcelFileValidator(FileValidator):
    def validate(self, file_path: str):
        try:
            self._validate_file_path(file_path)
            self._validate_file_extension(file_path)
            self._validate_sheets_name(file_path)
        except Exception as e:
            raise e

    def _validate_file_path(self, file_path: str):
        if not file_path:
            raise ValueError("No file path provided.")

    def _validate_file_extension(self, file_path: str):
        if not file_path.endswith(('.xlsx', '.xls')):
            raise ValueError("Invalid file extension. Please provide an Excel file.")

    def _validate_sheets_name(self, file_path: str):
        if not pd.ExcelFile(file_path).sheet_names:
            raise ValueError("No sheets found in the Excel file.")

    def is_results_file(self, file_path: str) -> bool:
        """Check if the file is a results file by looking for the Metadata sheet"""
        try:
            excel_file = pd.ExcelFile(file_path)
            if "Metadata" in excel_file.sheet_names:
                metadata = pd.read_excel(file_path, sheet_name="Metadata")
                return "file_type" in metadata.columns and "MoMo_Results" in metadata["file_type"].values
            return False
        except:
            return False

    def get_systems_data(self, file_path: str) -> dict:
        return self._read_systems_data(file_path)

    def _read_systems_data(self, file_path) -> list[SystemModel]:
        with pd.ExcelFile(file_path) as excel_file:
            systems_data = []
            for sheet_name in excel_file.sheet_names:
                if sheet_name == "Metadata":
                    continue

                sheet_data = excel_file.parse(sheet_name, index_col=0)
                try:
                    systems_data.append(SystemModel(sheet_name, sheet_data))
                except Exception as e:
                    print(f"Error processing sheet '{sheet_name}': {e}")
                    continue
            return systems_data


def load_systems_data(file_path: str, file_validator_class: FileValidator = ExcelFileValidator, **karg) -> list[SystemModel]:
    file_validator = file_validator_class(**karg)

    try:
        if file_validator.is_results_file(file_path):
            print("File is a results file.")
            results_map = ResultsMap.from_excel(file_path)
            systems = []
            for system_name in results_map.systems_names:
                system = results_map.systems.systems.get(system_name)
                print(f"System name: {system_name}")
                if system is not None:
                    systems.append(system)
            return systems

        # Regular system file
        file_validator.validate(file_path)
        return file_validator.get_systems_data(file_path)
    except Exception as e:
        print(f"Error loading file: {e}")
        return []
