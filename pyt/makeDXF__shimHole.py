import numpy as np
import os, sys
import ezdxf
import nkUtilities.load__pointFile as lpf


# ========================================================= #
# ===  makeDXF__shimHole.py                             === #
# ========================================================= #

def makeDXF__shimHole():

    x_, y_, z_ = 0, 1, 2
    diameter   = 0.008
    radius     = diameter * 0.5
    inpFile    = "dat/sector_tray_points.dat"
    outFile    = "msh/shimHole_sketch.dxf"
    
    # ------------------------------------------------- #
    # --- [1] load data                             --- #
    # ------------------------------------------------- #
    Data    = lpf.load__pointFile( inpFile=inpFile, returnType="point" )
    
    # ------------------------------------------------- #
    # --- [2] make shim Hole                        --- #
    # ------------------------------------------------- #
    doc = ezdxf.new("R2010")
    msp = doc.modelspace()
    for ik,pts in enumerate( Data ):
        msp.add_circle( center=pts[0:2], radius=radius )
    doc.saveas( outFile )
    return()


# ========================================================= #
# ===   Execution of Pragram                            === #
# ========================================================= #

if ( __name__=="__main__" ):
    makeDXF__shimHole()

