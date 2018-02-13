#!/usr/bin/python

## \file square.py
#  \brief Python script for creating a .su2 mesh of a simple square domain.
#  \author Thomas D. Economon
#  \version 1.0.

# Import the option parser and parse input options
from optparse import OptionParser

parser=OptionParser()
parser.add_option("-f", "--file", dest="filename", default="square.su2",
                  help="write mesh to FILE", metavar="FILE")
parser.add_option("-n", "--nNode", dest="nNode", default=3,
                  help="use this NNODE in x direction", metavar="NNODE")
parser.add_option("-m", "--mNode", dest="mNode", default=3,
                  help="use this MNODE in x direction", metavar="MNODE")
(options, args)=parser.parse_args()

# Set the VTK type for the interior elements and the boundary elements
KindElem  = 5 # Triangle
KindBound = 3 # Line

# Store the number of nodes and open the output mesh file
nNode     = int(options.nNode)
mNode     = int(options.mNode)
Mesh_File = open(options.filename,"w")

# Write the dimension of the problem and the number of interior elements
Mesh_File.write( "%\n" )
Mesh_File.write( "% Problem dimension\n" )
Mesh_File.write( "%\n" )
Mesh_File.write( "NDIME= 2\n" )
Mesh_File.write( "%\n" )
Mesh_File.write( "% Inner element connectivity\n" )
Mesh_File.write( "%\n" )
Mesh_File.write( "NELEM= %s\n" % (2*(nNode-1)*(mNode-1)))

# Write the element connectivity
iElem = 0
for jNode in range(mNode-1):
    for iNode in range(nNode-1):
        iPoint = jNode*nNode + iNode
        jPoint = jNode*nNode + iNode + 1
        kPoint = (jNode + 1)*nNode + iNode
        Mesh_File.write( "%s \t %s \t %s \t %s \t %s\n" % (KindElem, iPoint, jPoint, kPoint, iElem) )
        iElem = iElem + 1
        iPoint = jNode*nNode + (iNode + 1)
        jPoint = (jNode + 1)*nNode + (iNode + 1)
        kPoint = (jNode + 1)*nNode + iNode
        Mesh_File.write( "%s \t %s \t %s \t %s \t %s\n" % (KindElem, iPoint, jPoint, kPoint, iElem) )
        iElem = iElem + 1

# Compute the number of nodes and write the node coordinates
nPoint = (nNode)*(mNode)
Mesh_File.write( "%\n" )
Mesh_File.write( "% Node coordinates\n" )
Mesh_File.write( "%\n" )
Mesh_File.write( "NPOIN= %s\n" % ((nNode)*(mNode)) )
iPoint = 0
for jNode in range(mNode):
    for iNode in range(nNode):
        Mesh_File.write( "%15.14f \t %15.14f \t %s\n" % (float(iNode)/float(nNode-1), float(jNode)/float(mNode-1), iPoint) )
        iPoint = iPoint + 1

# Write the header information for the boundary markers
Mesh_File.write( "%\n" )
Mesh_File.write( "% Boundary elements\n" )
Mesh_File.write( "%\n" )
Mesh_File.write( "NMARK= 4\n" )

# Write the boundary information for each marker
Mesh_File.write( "MARKER_TAG= lower\n" )
Mesh_File.write( "MARKER_ELEMS= %s\n" % (nNode-1))
for iNode in range(nNode-1):
    Mesh_File.write( "%s \t %s \t %s\n" % (KindBound, iNode, iNode + 1) )
Mesh_File.write( "MARKER_TAG= right\n" )
Mesh_File.write( "MARKER_ELEMS= %s\n" % (mNode-1))
for jNode in range(mNode-1):
    Mesh_File.write( "%s \t %s \t %s\n" % (KindBound, jNode*nNode + (nNode - 1),  (jNode + 1)*nNode + (nNode - 1) ) )
Mesh_File.write( "MARKER_TAG= upper\n" )
Mesh_File.write( "MARKER_ELEMS= %s\n" % (nNode-1))
for iNode in range(nNode-1):
    Mesh_File.write( "%s \t %s \t %s\n" % (KindBound, (nNode*mNode - 1) - iNode, (nNode*mNode - 1) - (iNode + 1)) )
Mesh_File.write( "MARKER_TAG= left\n" )
Mesh_File.write( "MARKER_ELEMS= %s\n" % (mNode-1))
for jNode in range(mNode-2, -1, -1):
    Mesh_File.write( "%s \t %s \t %s\n" % (KindBound, (jNode + 1)*nNode, jNode*nNode ) )

# Close the mesh file and exit
Mesh_File.close()
