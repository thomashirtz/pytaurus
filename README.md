# pytaurus

Repository that provide a wrapper to use the software [Sentarurus TCAD](www.synopsys.com) with Python. 

# Projects



## PLT Files

This repository contains a very simple class to convert "plt" file to different formats such as dataframe, csv or dictionary. The class can be easily added to your project. This allows to efficiently process files coming from software such as [Sentarurus TCAD](www.synopsys.com). 

A raw plt file is also provided to test the script. The file was downloaded from the [National Tsinghua University website](http://semiconductorlab.iwopop.com/). It is part of the [3D TCAD Simulation for CMOS Nanoeletronic Devices](https://www.springer.com/gp/book/9789811030659) book.

### Basics

Import the library and create an instance
``` 
from pytaurus import PLTFile

filepath = 'file.plt'
plt_file = PLTFile(filepath)
```
Getting the keys
```
keys = plt_file.get_keys()
print(keys)
```

### Conversions

The different conversions:
```
# Dataframe
dataframe = plt_file.to_dataframe()
print(dataframe)

# CSV file
path_csv_file = 'file.csv'
plt_file.to_csv(path_csv_file)

# Dictionary 
dictionary = plt_file.to_dict()
print(dictionary)
```

It is also possible to filter the wanted keys during the conversion
```
keys = ['d_total_current', 'd_inner_voltage']
dictionary = plt_file.to_dict(keys=keys)
print(dictionary)
```

### Keys and Kwargs

By default the keys in the files are in the form "D Total Current", however, to make the name more pythonic, they are converted by default to "d_total_current" (by replacing spaces by underscore and removing uppercase). It is possible to change the keys by modifing the kwargs `separator: str = '_'` and `lowercase: bool = True`

## Requirements
pandas  

## Installation
This library contains only few helper functions. It is therefore possible to integrate it directly in the project. 
Otherwise, the command to install the repository via pip is:
```
pip install git+https://github.com/thomashirtz/pytaurus#egg=pytaurus
```
