
from sys import path
path.append(__file__[:__file__.find("/core/common")])

from core.rextlib.common.hash import get_file_hash


print(get_file_hash("core/config/types_.py"))