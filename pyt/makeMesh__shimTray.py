import numpy as np
import os, sys
import gmsh
import nkGmshRoutines.geometrize__fromTable as gft

# ========================================================= #
# ===  make__geometry                                   === #
# ========================================================= #

def make__shimTray( dimtags={} ):

    table   = { "tray": { "geometry_type":"cylinder", \
                          "xc":0.0, "yc":0.0, "zc":0.0, \
                          "dx":0.0, "dy":0.0, "dz":0.010, "r1":1.650*0.5 }, \
    }
    dimtags = gft.geometrize__fromTable( table=table, dimtags=dimtags )
    return( dimtags )


def make__shimHole( dimtags={}, points=None ):

    # for ik,pts in enumerate(points):
    #     print( ik )
    #     table   = { "hole": { "geometry_type":"cylinder", \
    #                           "xc":pts[0], "yc":pts[1], "zc":pts[2], \
    #                           "dx":0.0, "dy":0.0, "dz":0.010, "r1":0.005 }, \
    #                 "tray": { "boolean_type":"cut", \
    #                           "targetKeys":["tray"], "toolKeys":["hole"] }, \
    #     }
    #     dimtags = gft.geometrize__fromTable( table=table, dimtags=dimtags )


    table   = { "hole{0:06}".format(ik+1): { "geometry_type":"cylinder", \
                                             "xc":pts[0], "yc":pts[1], "zc":pts[2], \
                                             "dx":0.0, "dy":0.0, "dz":0.010, "r1":0.005 } \
                for ik,pts in enumerate(points) }
    dimtags = gft.geometrize__fromTable( table=table, dimtags=dimtags )
    keys    = [ "hole{0:06}".format(ik+1) for ik,pts in enumerate(points) ]
    table   = { "tray": { "boolean_type":"cut", \
                          "targetKeys":["tray"], "toolKeys":keys } }
    return( dimtags )


# ========================================================= #
# ===   実行部                                          === #
# ========================================================= #

if ( __name__=="__main__" ):

    import nkUtilities.load__pointFile as lpf
    inpFile = "dat/circle_tray_points.dat"
    points  = lpf.load__pointFile( inpFile=inpFile, returnType="point" )
    # points  = points[0:100,:]
    
    # ------------------------------------------------- #
    # --- [1] initialization of the gmsh            --- #
    # ------------------------------------------------- #
    gmsh.initialize()
    gmsh.option.setNumber( "General.Terminal", 1 )
    gmsh.option.setNumber( "Mesh.Algorithm"  , 5 )
    gmsh.option.setNumber( "Mesh.Algorithm3D", 1 )
    gmsh.option.setNumber( "Mesh.SubdivisionAlgorithm", 0 )
    gmsh.model.add( "model" )
    
    # ------------------------------------------------- #
    # --- [2] Modeling                              --- #
    # ------------------------------------------------- #
    dimtags = {}
    dimtags = make__shimTray( dimtags=dimtags )
    dimtags = make__shimHole( dimtags, points=points )
    
    gmsh.model.occ.synchronize()
    gmsh.model.occ.removeAllDuplicates()
    gmsh.model.occ.synchronize()
    gmsh.write( "msh/model.stp" )

    # ------------------------------------------------- #
    # --- [3] Mesh settings                         --- #
    # ------------------------------------------------- #
    mesh_from_config = False         # from nkGMshRoutines/test/mesh.conf, phys.conf
    if ( mesh_from_config ):
        meshFile = "dat/mesh.conf"
        physFile = "dat/phys.conf"
        import nkGmshRoutines.assign__meshsize as ams
        meshes = ams.assign__meshsize( meshFile=meshFile, physFile=physFile, dimtags=dimtags )
    else:
        gmsh.option.setNumber( "Mesh.CharacteristicLengthMin", 0.05 )
        gmsh.option.setNumber( "Mesh.CharacteristicLengthMax", 0.05 )

    # ------------------------------------------------- #
    # --- [4] post process                          --- #
    # ------------------------------------------------- #
    gmsh.model.occ.synchronize()
    gmsh.model.mesh.generate(3)
    gmsh.write( "msh/model.msh" )
    gmsh.finalize()

