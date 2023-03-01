"RT Lib - Get Config Class Hash"

from sys import path
path.append(__file__[:__file__.find("/core/rtlib")])

from core.rextlib.common.hash import get_file_hash


print(get_file_hash("config.template.toml"))