#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  8 07:30:31 2021

@author: jurka
"""


import numpy as np
import pandas as pd
import ase

#from quippy.descriptors import Descriptor
#import quippy.descriptors.Descriptor as Descriptor
from quippy.descriptors import Descriptor

at = ase.Atoms(
        symbols=['O', 'Ga'],
               )
at.set_cell

at.set_scaled_positions

desc = Descriptor(
        "soap cutoff=10 l_max=4 n_max=4 normalize=T atom_sigma=0.5 n_Z=1 Z={14} "
        )

# GAP not installed (under /src)
# fix it
def get_path(tt: str):
    path = '/home/jurka/research-project/'+tt+'/final/'
    return path