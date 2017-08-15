#!/usr/bin/env python

## \file Compute_Mpolar.py
#  \brief Python script for performing sweep of Mach number.
#  \author H. Kline (based on E. Arad compute_polar script)
#  \version 5.0.0 "Raven"
#
# SU2 Lead Developers: Dr. Francisco Palacios (Francisco.D.Palacios@boeing.com).
#                      Dr. Thomas D. Economon (economon@stanford.edu).
#
# SU2 Developers: Prof. Juan J. Alonso's group at Stanford University.
#                 Prof. Piero Colonna's group at Delft University of Technology.
#                 Prof. Nicolas R. Gauger's group at Kaiserslautern University of Technology.
#                 Prof. Alberto Guardone's group at Polytechnic University of Milan.
#                 Prof. Rafael Palacios' group at Imperial College London.
#
# Copyright (C) 2012-2017 SU2, the open-source CFD code.
#
# SU2 is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# SU2 is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with SU2. If not, see <http://www.gnu.org/licenses/>.

# imports
import numpy as np
import matplotlib.pyplot as plt
from optparse import OptionParser
import os, sys, shutil, copy, os.path
sys.path.append(os.environ['SU2_RUN'])
import SU2

def main():
# Command Line Options
    parser = OptionParser()
    parser.add_option("-f", "--file", dest="filename",
                      help="read config from FILE", metavar="FILE")
    parser.add_option("-n", "--partitions", dest="partitions", default=2,
                      help="number of PARTITIONS", metavar="PARTITIONS")
    parser.add_option("-i", "--iterations", dest="iterations", default=99999,
                      help="number of ITERATIONS", metavar="ITERATIONS")
    
    (options, args)=parser.parse_args()
    options.partitions = int( options.partitions )
    options.iterations = int( options.iterations )
    
    # load config, start state
    config = SU2.io.Config(options.filename)
    state  = SU2.io.State()
    
    # find solution files if they exist
    state.find_files(config)
    
    # prepare config
    config.NUMBER_PART = options.partitions
    config.EXT_ITER    = options.iterations
    
    # Initialize results arrays   
    nMach = 5
    MachList=np.linspace(0.5,0.6,nMach)
    LiftList=[]
    DragList=[]

    # Output file
    outFile='Polar_M' + str(MachList[0]) + '.dat'
    f = open(outFile, 'w')
    f.write('%  Mach, CL, CD,  \n')
        
    # iterate on Mach number
    for MachNumber in MachList:
            
        # local config and state
        konfig = copy.deepcopy(config)
        ztate  = copy.deepcopy(state)
            
        # set config options
        konfig.MACH_NUMBER = MachNumber
        caseName='DIRECT_M_'+str(MachNumber)
        
        # run su2
        drag = SU2.eval.func('DRAG',konfig,ztate)
        lift = SU2.eval.func('LIFT',konfig,ztate)
        
        LiftList.append(lift)
        DragList.append(drag)
        
        output = str(MachNumber)+", "+ str(lift) + ", " + str(drag)+"\n"      
        f.write(output)
        
        # Store result in a subdirectory
        if os.path.isdir(caseName):
           os.system('rm -R '+caseName)
        command='mv DIRECT '+caseName
        os.system(command)
        
    # Close open file    
    f.close()

    # plotting
    #plt.figure()
    #plt.plot( MachList, LiftList )
    #plt.xlabel('Mach')
    #plt.ylabel('Lift Coefficient')
    #plt.show()

   
if __name__ == "__main__":
    main()
