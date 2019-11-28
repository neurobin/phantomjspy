# -*- coding: utf-8 -*-

import sys
from . import Phantom

phantom = Phantom()

if __name__ == '__main__':
    print(phantom.download_page(sys.argv[1], selector=sys.argv[2], timeout=sys.argv[3]))
