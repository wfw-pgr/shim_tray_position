import numpy as np
import os, sys
import gmsh
import nkGmshRoutines.geometrize__fromTable as gft

# ========================================================= #
# ===  make__geometry                                   === #
# ========================================================= #

def make__geometry( dimtags={} ):

    table   = { "trapezoid": { "geometry_type":"polygon", "axis":None, \
                               "vertex1":[0,0,0], "vertex2":[0.2,0,0], \
                               "vertex3":[0.185,0.15,0], "vertex4":[0.015,0.15,0], } \
    }
    dimtags = gft.geometrize__fromTable( table=table, dimtags=dimtags )
    return( dimtags )


# ========================================================= #
# ===   実行部                                          === #
# ========================================================= #

if ( __name__=="__main__" ):

    # ------------------------------------------------- #
    # --- [1] initialization of the gmsh            --- #
    # ------------------------------------------------- #
    gmsh.initialize()
    gmsh.option.setNumber( "General.Terminal", 1 )
    gmsh.option.setNumber( "Mesh.Algorithm"  , 1 )
    gmsh.option.setNumber( "Mesh.Algorithm3D", 4 )
    gmsh.option.setNumber( "Mesh.SubdivisionAlgorithm", 0 )
    gmsh.model.add( "model" )
    
    # ------------------------------------------------- #
    # --- [2] Modeling                              --- #
    # ------------------------------------------------- #
    dimtags = {}
    dimtags = make__geometry( dimtags=dimtags )
    
    gmsh.model.occ.synchronize()
    gmsh.model.occ.removeAllDuplicates()
    gmsh.model.occ.synchronize()

    # ------------------------------------------------- #
    # --- [3] Mesh settings                         --- #
    # ------------------------------------------------- #
    mesh_from_config = False          # from nkGMshRoutines/test/mesh.conf, phys.conf
    if ( mesh_from_config ):
        meshFile = "dat/mesh.conf"
        physFile = "dat/phys.conf"
        import nkGmshRoutines.assign__meshsize as ams
        meshes = ams.assign__meshsize( meshFile=meshFile, physFile=physFile, dimtags=dimtags )
    else:
        gmsh.option.setNumber( "Mesh.CharacteristicLengthMin", 0.010 )
        gmsh.option.setNumber( "Mesh.CharacteristicLengthMax", 0.010 )

    # ------------------------------------------------- #
    # --- [4] post process                          --- #
    # ------------------------------------------------- #
    gmsh.model.occ.synchronize()
    gmsh.model.mesh.generate(3)
    gmsh.write( "msh/trapezoidal_tray.msh" )
    gmsh.finalize()

