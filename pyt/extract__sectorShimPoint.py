import os, sys
import numpy as np

# ========================================================= #
# ===  extract__shimpoint.py                            === #
# ========================================================= #

def extract__shimpoint():

    x_, y_, z_ = 0, 1, 2

    mshFile    = "msh/sector_tray.msh"
    
    # ------------------------------------------------- #
    # --- [1] load mesh file                        --- #
    # ------------------------------------------------- #
    import nkMeshRoutines.load__meshio as lms
    mesh    = lms.load__meshio( mshFile=mshFile, elementType="triangle", returnType="dict" )
    points  = mesh["points"]
    cells   = mesh["cells"]
    cellpt  = points[ cells, : ]
    cog     = np.average( cellpt[ :, :, : ], axis=1 )
    theta   = np.linspace( 0.0, 2.0*np.pi, 101 )
    
    
    # radii   = np.sqrt( points[:,x_]**2 + points[:,y_]**2 )
    # extract = points[ ( np.where( radii <= radius - epsilon ) )[0], : ]
    # theta   = np.linspace( 0, 2.0*np.pi, 201 )
    # cos,sin = np.cos( theta ), np.sin( theta )
    # circle  = radius * np.concatenate( [ cos[:,None], sin[:,None] ], axis=1 )

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
    fig.add__plot( xAxis=cog[:,x_], yAxis=cog[:,y_], \
                   linestyle="none", marker=".", markersize=0.6 )
    fig.add__legend()
    fig.set__axis()
    fig.save__figure()

    # ------------------------------------------------- #
    # --- [3] save in a file                        --- #
    # ------------------------------------------------- #
    import nkUtilities.save__pointFile as spf
    outFile   = "dat/sector_tray_points.dat"
    spf.save__pointFile( outFile=outFile, Data=cog )
    return()


# ========================================================= #
# ===   Execution of Pragram                            === #
# ========================================================= #

if ( __name__=="__main__" ):
    extract__shimpoint()
