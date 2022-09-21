import os, sys
import numpy as np

# ========================================================= #
# ===  extract__shimpoint.py                            === #
# ========================================================= #

def extract__shimpoint():

    x_, y_, z_ = 0, 1, 2

    
    mshFile = "msh/circle_tray.msh"
    radius  = 1.650*0.5 # unit: [m]
    epsilon = 5.e-4     #  0.5 [mm]
    
    # ------------------------------------------------- #
    # --- [1] load mesh file                        --- #
    # ------------------------------------------------- #
    import nkMeshRoutines.load__meshio as lms
    mesh    = lms.load__meshio( mshFile=mshFile, elementType="vertex", returnType="dict" )
    points  = mesh["points"]
    radii   = np.sqrt( points[:,x_]**2 + points[:,y_]**2 )

    extract = points[ ( np.where( radii <= radius - epsilon ) )[0], : ]

    theta   = np.linspace( 0, 2.0*np.pi, 201 )
    cos,sin = np.cos( theta ), np.sin( theta )
    circle  = radius * np.concatenate( [ cos[:,None], sin[:,None] ], axis=1 )

    # ------------------------------------------------- #
    # --- [2] confirmation display                  --- #
    # ------------------------------------------------- #
    import nkUtilities.plot1D         as pl1
    import nkUtilities.load__config   as lcf
    import nkUtilities.configSettings as cfs
    x_,y_                    = 0, 1
    pngFile                  = "png/circle_tray.png"
    config                   = lcf.load__config()
    config                   = cfs.configSettings( configType="plot.def", config=config )
    config["plt_xAutoRange"] = True
    config["plt_yAutoRange"] = True
    config["plt_xRange"]     = [ -1.2, +1.2 ]
    config["plt_yRange"]     = [ -1.2, +1.2 ]
    fig     = pl1.plot1D( config=config, pngFile=pngFile )
    fig.add__plot( xAxis=extract[:,x_], yAxis=extract[:,y_], \
                   linestyle="none", marker=".", markersize=0.6 )
    fig.add__plot( xAxis=circle[:,x_], yAxis=circle[:,y_], \
                   linestyle="--", linewidth=0.8 )
    fig.add__legend()
    fig.set__axis()
    fig.save__figure()

    # ------------------------------------------------- #
    # --- [3] save in a file                        --- #
    # ------------------------------------------------- #
    import nkUtilities.save__pointFile as spf
    outFile   = "dat/circle_tray_points.dat"
    spf.save__pointFile( outFile=outFile, Data=extract )
    return()


# ========================================================= #
# ===   Execution of Pragram                            === #
# ========================================================= #

if ( __name__=="__main__" ):
    extract__shimpoint()
