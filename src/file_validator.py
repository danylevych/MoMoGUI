from abc import ABC, abstractmethod
import pandas as pd
from momo.system_models.system_models import SystemModel


class FileValidator(ABC):
    @abstractmethod
    def validate(self, file_path):
        pass

    @abstractmethod
    def get_systems_data(self, file_path):
        pass



class ExcelFileValidator(FileValidator):
    OPTIONAL_SHEETS = ['Prototype', 'Results']

    def validate(self, file_path):
        try:
            self._validate_file_path(file_path)
            self._validate_file_extension(file_path)
            self._validate_sheets_name(file_path)
        except Exception as e:
            raise e

    def _validate_file_path(self, file_path):
        if not file_path:
            raise ValueError("No file path provided.")

    def _validate_file_extension(self, file_path):
        if not file_path.endswith(('.xlsx', '.xls')):
            raise ValueError("Invalid file extension. Please provide an Excel file.")

    def _validate_sheets_name(self, file_path):
        if not pd.ExcelFile(file_path).sheet_names:
            raise ValueError("No sheets found in the Excel file.")

    def get_systems_data(self, file_path):
        return self._read_systems_data(file_path)

    def _read_systems_data(self, file_path):
        excel_file = pd.ExcelFile(file_path)
        systems_data = {}

        systems_data['Systems'] = []
        systems_data['Prototype'] = None
        systems_data['Results'] = None

        for sheet_name in excel_file.sheet_names:
            sheet_data = excel_file.parse(sheet_name, index_col=0)
            if sheet_name not in self.OPTIONAL_SHEETS:
                systems_data['Systems'].append(self.buid_system(sheet_name, sheet_data))
            else:
                systems_data[sheet_name] = self.buid_system(sheet_name, sheet_data)

        return systems_data

    def buid_system(self, name, systems_data):
        system = SystemModel(name)
        system.data = systems_data
        return system
