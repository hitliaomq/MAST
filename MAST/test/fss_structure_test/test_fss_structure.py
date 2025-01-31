import os
import time
import unittest
from unittest import SkipTest
import filecmp
from filecmp import dircmp
import MAST
from MAST.ingredients.pmgextend.structure_extensions import StructureExtensions
import shutil
import pymatgen
from pymatgen.io.vasp import Poscar
import numpy as np
from MAST.utility import dirutil

testname ="fss_structure_test"
#oldcontrol = os.getenv("MAST_CONTROL")
#oldscratch = os.getenv("MAST_SCRATCH")
#print "Old directories:"
#print oldcontrol
#print oldscratch
testdir = os.path.join(dirutil.get_mast_install_path(),'test',testname)


class TestSE(unittest.TestCase):
    """Test StructureExtensions
    """
    def setUp(self):
        os.chdir(testdir)

    def tearDown(self):
        pass

    def test_scale_structure(self):
        size = '1 1 0,-1 1 0,0 0 1'
        perfect = Poscar.from_file("POSCAR_perfect").structure
        sxtend = StructureExtensions(struc_work1=perfect,scaling_size=size)
        scaled = sxtend.scale_structure()
        compare = Poscar.from_file("POSCAR_scaled").structure
        #self.assertEqual(scaled, Poscar.from_file("POSCAR_scaled").structure)
        self.assertAlmostEqual(scaled.volume, compare.volume, places=3)
        self.assertEqual(scaled.lattice, compare.lattice)
        self.assertEqual(scaled.sites.sort(), compare.sites.sort())
        return
    def test_scale_defect(self):
        size = '1 1 0,-1 1 0,0 0 1'
        perfect = Poscar.from_file("POSCAR_perfect").structure
        sxtend = StructureExtensions(struc_work1=perfect,scaling_size=size)
        scaled = sxtend.scale_structure()
        sxtend2 = StructureExtensions(struc_work1=scaled,scaling_size=size)
        vac1={'symbol':'O', 'type': 'vacancy', 'coordinates':  np.array([0.25, 0.75, 0.25])}
        defected =  sxtend2.scale_defect(vac1,'fractional',0.0001)
        int1={'symbol':'Ni', 'type': 'interstitial', 'coordinates': np.array([0.3, 0.3, 0.3])}
        sxtend3 = StructureExtensions(struc_work1=defected,scaling_size=size)
        defected2 = sxtend3.scale_defect(int1,'fractional',0.0001)
        sub1={'symbol':'Fe', 'type': 'substitution','coordinates':np.array([0.25, 0.25,0.75])}
        sxtend4 = StructureExtensions(struc_work1=defected2,scaling_size=size)
        defected3 = sxtend4.scale_defect(sub1,'fractional',0.0001)
        compare = Poscar.from_file("POSCAR_scaled_defected").structure
        #self.assertEqual(Poscar.from_file("POSCAR_scaled_defected").structure, defected3)
        self.assertAlmostEqual(defected3.volume, compare.volume, places=3)
        self.assertEqual(defected3.lattice, compare.lattice)
        self.assertEqual(defected3.sites.sort(), compare.sites.sort())
        return
