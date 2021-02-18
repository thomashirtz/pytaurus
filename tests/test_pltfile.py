from pytaurus import PLTFile


file = '../data/file.plt'
keys = ['d_total_current', 'd_inner_voltage']

print(PLTFile(file).to_dataframe())
print(PLTFile(file).get_keys(snake_case=False))
print(PLTFile(file).get_keys(snake_case=True))
print(PLTFile(file).to_dict(keys))
