from collections import defaultdict
from typing import Dict, Optional
import pandas as pd
import csv


class PLTFile:
    def __init__(self, path):
        self.path = path

    def get_keys(self, **kwargs) -> list:
        data = self.read_file(self.path)
        dictionary = self._process_data(data, **kwargs)
        return list(dictionary.keys())

    def to_dict(self, keys: Optional[list] = None, **kwargs) -> Dict:
        return self._get_dictionary(keys, **kwargs)

    def to_dataframe(self, keys: Optional[list] = None, **kwargs) -> pd.DataFrame:
        dictionary = self._get_dictionary(keys, **kwargs)
        return pd.DataFrame.from_dict(dictionary, orient='index').transpose()

    def to_csv(self, csv_file, keys: Optional[list] = None, **kwargs):
        dictionary = self._get_dictionary(keys, **kwargs)

        keys = dictionary.keys()
        with open(csv_file, "wb") as outfile:
            writer = csv.writer(outfile, delimiter="\t")
            writer.writerow(keys)
            writer.writerows(zip(*[dictionary[key] for key in keys]))

    def _get_dictionary(self, keys: Optional[list] = None, **kwargs) -> Dict:  # todo add kwarg
        data = self.read_file(self.path)
        dictionary = self._process_data(data, **kwargs)
        if not keys:
            return dictionary
        return {key: dictionary[key] for key in keys}

    @staticmethod
    def _process_data(data: str, separator='_', lowercase=True) -> Dict[str, list]:
        keys = data.replace(' ', '').split('datasets=[')[1].split(']')[0].split('"')[1::2]
        values = data.split('Data {      ')[1].split('}')[0].split()

        def reformat_name(string: str, separator: str, lowercase: bool) -> str:
            name = ''.join([separator + char.lower() if char.isupper() and lowercase else char for char in string])
            return name.lstrip(separator)
        keys = [reformat_name(key, separator, lowercase) for key in keys]

        d = defaultdict(list)
        for i, value in enumerate(values):
            key = keys[i % len(keys)]
            d[key].append(float(value))
        return dict(d)

    @staticmethod
    def read_file(path):
        with open(path, 'r') as f:
            data = f.read().replace('\n', '')
        return data
