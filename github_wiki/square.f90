!  \file square.f90
!  \brief Fortran script for creating a .su2 mesh of a simple square domain.
!  \author Thomas D. Economon
!  \version 1.0.

program square

! Local variables and initialization
implicit none
integer :: KindElem, KindBound, iElem
integer :: nNode, mNode, iNode, jNode
integer :: nPoint, iPoint, jPoint, kPoint
character(len=20) :: Mesh_File

! Store the number of nodes and output mesh filename
nNode     = 3
mNode     = 3
Mesh_File = "square.su2"

! Set the VTK type for the interior elements and the boundary elements
KindElem  = 5 ! Triangle
KindBound = 3 ! Line

! Open the formatted mesh file
open(unit=7,file=Mesh_File,form="formatted")

! Write the dimension of the problem and the number of interior elements
write(7,*) "%"
write(7,*) "% Problem dimension"
write(7,*) "%"
write(7,5) 2
5 format('NDIME= ',i1)

write(7,*) "%"
write(7,*) "% Inner element connectivity"
write(7,*) "%"
write(7,10) 2*(nNode-1)*(mNode-1)
10 format('NELEM= ',i1)

! Write the element connectivity
iElem = 0
do jNode = 0,mNode-2
  do iNode = 0,nNode-2
    iPoint = jNode*nNode + iNode
    jPoint = jNode*nNode + iNode + 1
    kPoint = (jNode + 1)*nNode + iNode
    write(7,*) KindElem, iPoint, jPoint, kPoint, iElem
    iElem = iElem + 1
    iPoint = jNode*nNode + (iNode + 1)
    jPoint = (jNode + 1)*nNode + (iNode + 1)
    kPoint = (jNode + 1)*nNode + iNode
    write(7,*) KindElem, iPoint, jPoint, kPoint, iElem
    iElem = iElem + 1
  enddo
enddo

! Compute the number of nodes and write the node coordinates
nPoint = (nNode)*(mNode)
write(7,*) "%"
write(7,*) "% Node coordinates"
write(7,*) "%"
write(7,20) nNode*mNode
20 format('NPOIN= ', i1)

iPoint = 0
do jNode = 0,mNode-1
  do iNode = 0,nNode-1
    write(7,*) real(iNode)/float(nNode-1), real(jNode)/float(mNode-1), iPoint
    iPoint = iPoint + 1
  enddo
enddo

! Write the header information for the boundary markers
write(7,*) "%"
write(7,*) "% Boundary elements"
write(7,*) "%"
write(7,30) 4
30 format('NMARK= ',i1)

! Two formatting statements which will be reused
40 format('MARKER_TAG= ',a)
50 format('MARKER_ELEMS= ', i1)

! Write the boundary information for each marker
write(7,40) "lower"
write(7,50) (nNode-1)
do iNode = 0,nNode-2
  write(7,*) KindBound, iNode, iNode + 1
enddo

write(7,40) "right"
write(7,50) (mNode-1)
do jNode = 0,mNode-2
  write(7,*) KindBound, jNode*nNode+(nNode-1), (jNode+1)*nNode+(nNode-1)
enddo

write(7,40) "upper"
write(7,50) (nNode-1)
do iNode = 0,nNode-2
  write(7,*) KindBound, (nNode*mNode-1)-iNode, (nNode*mNode-1)-(iNode+1)
enddo

write(7,40) "left"
write(7,50) (mNode-1)
do jNode = mNode-2,mNode-3,-1
  write(7,*) KindBound, (jNode+1)*nNode, jNode*nNode
enddo

! Close the mesh file and exit
close(7)

end program square
