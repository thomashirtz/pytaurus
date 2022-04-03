import csv
import re
from collections import defaultdict
from typing import Dict
from typing import Optional

import pandas as pd


class PLTFile:
    def __init__(self, path):
        self._path = path

    def get_keys(self, **kwargs) -> list:
        data = self._read_file(self._path)
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
        with open(csv_file, 'wb') as outfile:
            writer = csv.writer(outfile, delimiter='\t')
            writer.writerow(keys)
            writer.writerows(zip(*[dictionary[key] for key in keys]))

    def _get_dictionary(self, keys: Optional[list] = None, **kwargs) -> Dict:
        data = self._read_file(self._path)
        dictionary = self._process_data(data, **kwargs)
        if not keys:
            return dictionary
        return {key: dictionary[key] for key in keys}

    @staticmethod
    def _process_data(data: str, snake_case: bool = True) -> Dict[str, list]:
        keys = re.findall(r'"([a-zA-Z0-9 .]+)"', data)
        values = data.split('Data {      ')[1].split('}')[0].split()

        if snake_case:
            def get_snake_case(s):
                return ''.join(['_' + c.lower() if c.isupper() else c for c in s.replace(' ', '')]).lstrip('_')
            keys = [get_snake_case(key) for key in keys]

        d = defaultdict(list)
        for i, value in enumerate(values):
            key = keys[i % len(keys)]
            d[key].append(float(value))
        return dict(d)

    @staticmethod
    def _read_file(path):
        with open(path) as f:
            data = f.read().replace('\n', '')
        return data
