import os, sys
import numpy as np

# ========================================================= #
# ===  issue__solidworksMacro.py                        === #
# ========================================================= #

def issue__solidworksMacro():

    radius   = 0.005
    maxLines = 400    # solidworks macro is very poor, cannot handle more than 1023 lines.
    macroCmd = "Set skSegment = Part.SketchManager.CreateCircle( "\
        "{0[0]:.5}, {0[1]:.5}, {0[2]:.5}, {0[3]:.5}, {0[4]:.5}, {0[5]:.5} )\n"\
        "Part.ClearSelection2 True\n"
    
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
    print( shifted.shape, centers.shape )
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

    # ------------------------------------------------- #
    # --- [4] confirmation                          --- #
    # ------------------------------------------------- #
    import nkUtilities.plot1D         as pl1
    import nkUtilities.load__config   as lcf
    import nkUtilities.configSettings as cfs
    x_,y_                    = 0, 1
    pngFile                  = "png/out.png"
    config                   = lcf.load__config()
    config                   = cfs.configSettings( configType="plot.def", config=config )
    config["plt_xAutoRange"] = True
    config["plt_yAutoRange"] = True
    config["plt_xRange"]     = [ -1.2, +1.2 ]
    config["plt_yRange"]     = [ -1.2, +1.2 ]
    fig     = pl1.plot1D( config=config, pngFile=pngFile )
    fig.add__plot( xAxis=circles[:,0], yAxis=circles[:,1], linestyle="none", \
                   marker=".", markersize=0.8, color="magenta" )
    fig.add__plot( xAxis=circles[:,3], yAxis=circles[:,4], linestyle="none", \
                   marker=".", markersize=0.8, color="cyan" )
    fig.add__legend()
    fig.set__axis()
    fig.save__figure()


    

# ========================================================= #
# ===   Execution of Pragram                            === #
# ========================================================= #

if ( __name__=="__main__" ):
    issue__solidworksMacro()
