import os

#default dir
BASE_DIR = os.getcwd()
DATA_DIR = os.path.join(BASE_DIR, 'data')

#origin data
ORIGIN_DIR = os.path.join(DATA_DIR, 'origin')
ORIGIN_PATH = os.path.join(ORIGIN_DIR, '*')

#name identification dictionary
NAME_DIR = os.path.join(DATA_DIR, 'name_dict')
NAME_PATH = os.path.join(NAME_DIR, '*')

#html dir
HTML_DIR = os.path.join(DATA_DIR, 'html')

#txt anchor dir
TXT_ANCHOR_DIR = os.path.join(DATA_DIR, 'txt')
TXT_ANCHOR_PATH = os.path.join(TXT_ANCHOR_DIR, 'txt.csv')

#path pattern dir
PATH_PATTERN_DIR = os.path.join(DATA_DIR, 'path')
PATH_PATTERN_PATH = os.path.join(PATH_PATTERN_DIR, 'path.csv')

#a tag length limit
A_TAG_LENGTH_LIMIT = 300