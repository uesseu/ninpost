import csv
import json
import os
import sys

class SpreadSheet:
    def __init__(self, path):
        with open(path, newline="", encoding="utf-8") as f:
            data = list(csv.reader(f))
        self.label = data[0]
        self.data = data[1:]

    def as_dict(self):
        results = []
        for data in self.data:
            result = {}
            for num, label in enumerate(self.label):
                if label in result.keys():
                    if isinstance(result[label], list):
                        result[label].append(data[num])
                    else:
                        result[label] = [result[label], data[num]]
                else:
                    result[label] = data[num]
            results.append(result)
        return results
