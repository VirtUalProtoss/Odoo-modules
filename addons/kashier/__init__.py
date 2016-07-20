
from . import models

def test_kkm():
    from .rs232tcp import rs232tcp
    from .shtrihm import beep
    com = rs232tcp('10.19.205.227', 5678)
    res = com.connect()
    print res
    beep(com)
