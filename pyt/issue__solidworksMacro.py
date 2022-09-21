import os, sys
import numpy as np

# ========================================================= #
# ===  issue__solidworksMacro.py                        === #
# ========================================================= #

def issue__solidworksMacro():

    radius   = 0.05
    maxLines = 800    # solidworks macro is very poor, cannot handle more than 1023 lines.
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
    stack    = []
    commands = []
    count    = 0
    for ik, circ in enumerate( circles ):
        cmd    = macroCmd.format( circ )
        stack.append( cmd )
        count += 1
        if ( count == maxLines ):
            commands.append( "".join( stack ) )
            stack = []
            count = 0
    commands.append( "".join( stack ) )

    # ------------------------------------------------- #
    # --- [3] save in a file                        --- #
    # ------------------------------------------------- #
    outFile = "dat/solidworks_macro_{0:04}.swp_part"
    for ik,cmd in enumerate(commands):
        with open( outFile.format(ik+1), "w" ) as f:
            f.write( cmd )

# ========================================================= #
# ===   Execution of Pragram                            === #
# ========================================================= #

if ( __name__=="__main__" ):
    issue__solidworksMacro()
