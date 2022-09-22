import numpy as np
import os, sys
import gmsh
import nkGmshRoutines.geometrize__fromTable as gft

# ========================================================= #
# ===  make__geometry                                   === #
# ========================================================= #

def make__geometry( dimtags={} ):

    r1  = 0.275
    r2  = 0.855
    th1 = 0.0
    th2 = 45.0
    
    import nkGmshRoutines.generate__fanShape as fan
    ret = fan.generate__fanShape( r1=r1, r2=r2, th1=th1, th2=th2, defineSurf=True )
    dimtags = { "tray": [ (3,ret["surf"]["fan"] ) ] }

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
    gmsh.option.setNumber( "Mesh.Algorithm"  , 6 )
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
        gmsh.option.setNumber( "Mesh.CharacteristicLengthMin", 0.015 )
        gmsh.option.setNumber( "Mesh.CharacteristicLengthMax", 0.015 )

    # ------------------------------------------------- #
    # --- [4] post process                          --- #
    # ------------------------------------------------- #
    gmsh.model.occ.synchronize()
    gmsh.model.mesh.generate(3)
    gmsh.write( "msh/sector_tray.msh" )
    gmsh.finalize()

