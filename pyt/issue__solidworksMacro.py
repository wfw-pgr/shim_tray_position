import os, sys
import numpy as np

# ========================================================= #
# ===  issue__solidworksMacro.py                        === #
# ========================================================= #

def issue__solidworksMacro():

    radius   = 0.05
    macroCmd = "Set skSegment = Part.SketchManager.CreateCircle( "\
        "{0[0]:.5}, {0[1]:.5}, {0[2]:.5}, {0[3]:.5}, {0[4]:.5}, {0[5]:.5} )\n"
    
    # ------------------------------------------------- #
    # --- [1] load shim tray points                 --- #
    # ------------------------------------------------- #
    import nkUtilities.load__pointFile as lpf
    inpFile = "dat/circle_tray_points.dat"
    centers = lpf.load__pointFile( inpFile=inpFile, returnType="point" )
    npt     = centers.shape[0]
    radii   = np.repeat( radius, npt )
    zeros   = np.zeros( (npt,2) )
    shifted = np.concatenate( [ radii[:,None], zeros ], axis=1 )
    dragged = centers + shifted

    circles = np.concatenate( [centers,dragged], axis=1 )
    
    # ------------------------------------------------- #
    # --- [2] issue macro command                   --- #
    # ------------------------------------------------- #
    stack = []
    for ik, circ in enumerate( circles ):
        cmd   = macroCmd.format( circ )
        stack.append( cmd )
    commands = "".join( stack )

    # ------------------------------------------------- #
    # --- [3] save in a file                        --- #
    # ------------------------------------------------- #
    with open( "dat/solidworks_macro.swp_part", "w" ) as f:
        f.write( commands )
    

# ========================================================= #
# ===   Execution of Pragram                            === #
# ========================================================= #

if ( __name__=="__main__" ):
    issue__solidworksMacro()
