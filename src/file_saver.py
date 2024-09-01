import pandas as pd

class ExcelSaver:
    def __init__(self, file_path):
        self.file_path = file_path

    def save_tab(self, tab_name, data):
        try:
            with pd.ExcelWriter(self.file_path, mode='a', engine='openpyxl') as writer:
                if tab_name in writer.book.sheetnames:
                    del writer.book[tab_name]
                data.to_excel(writer, sheet_name=tab_name)
        except FileNotFoundError:
            with pd.ExcelWriter(self.file_path, mode='w', engine='openpyxl') as writer:
                data.to_excel(writer, sheet_name=tab_name)
