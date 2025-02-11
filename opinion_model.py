

########################################################################
#-----------------------------------------------------------------------
# Copyright (C) 2022, All rights reserved
#
# Peng Wang
# Email: wp2204@gmail.com
#-----------------------------------------------------------------------
########################################################################
# -*-coding:utf-8-*-


#%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#%%% Simulation
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%


import numpy as np
import random
import matplotlib.pyplot as plt
import csv
from data_func import *
#from RandomFlow import *
import logging, os, sys

try:
    import matplotlib.pyplot as plt
except:
    print("Warning: matplotlib cannot be imported.  Unable to plot figures!")
    if sys.version_info[0] == 2: 
        raw_input("Please check!")
    else:
        input("please check!")

logging.basicConfig(filename='log_examp.log',level=logging.DEBUG)
logging.debug('This message should go to the log file')
logging.info('So should this')
logging.warning('And this, too')


def simulationOP(filename, T, DEBUG=True):

        # Time Horizon: T

        # Read in csv file
        #fileName

        print('\nBuilding Models\n')

        try: 
            dataIS, isStart, isEnd = getData(filename, "&inti")
            dataP, pStart, pEnd = getData(filename, "&p")
            #dataBLD, bldStart, bldEnd = getData(filename, "&bld")
            dataWP, wpStart, wpEnd = getData(filename, "&prob")

            print(dataIS)
            print(dataWP)
            print(dataP)

            NumAgents=np.size(dataIS)-1

            matrixIS=readFloatArray(dataIS, NumAgents, 1)
            if matrixIS.shape[0]!=NumAgents:
                print('\nError with matrixIS\n')
                    
            matrixWP=readFloatArray(dataWP, NumAgents, NumAgents)
            # %%%% Input parameter check
            if np.shape(matrixWP)!= (NumAgents, NumAgents):
                print('\nError on input parameter\n')

            if dataP:
                matrixP=readFloatArray(dataP, NumAgents, 1)
                if matrixP.shape[0]!=NumAgents:
                    print('\nError with matrixP\n')

            print(matrixWP)
            print(matrixIS)
            if dataP:
                print(matrixP)

        except:

            agents, agent2exit, agentgroup = readSocialArrayCSV(filename, debug=True, marginTitle=1)
            NumAgents=len(agents)-1
            print("Number of Agent:", NumAgents)
            
            matrixIS = np.zeros((NumAgents, 1))
            matrixP = np.zeros((NumAgents, 1))
            
            for idai in range(NumAgents):
                matrixIS[idai,0]= agents[idai+1][6]
                matrixP[idai,0]= agents[idai+1][7]

            #print(agents)
            print("matrixIS:\n", matrixIS, "\n")
            print("matrixP:\n", matrixP, "\n")

            tableFeatures, LowerIndex, UpperIndex = getData(filename, '&groupCABD')
            if len(tableFeatures)>0:
                CFactor_Init, AFactor_Init, BFactor_Init, DFactor_Init = readGroupCABD(tableFeatures, NumAgents, NumAgents)
            else:
                tableFeatures, LowerIndex, UpperIndex = getData(filename, '&groupSABD')
                if len(tableFeatures)>0:
                    CFactor_Init, AFactor_Init, BFactor_Init, DFactor_Init = readGroupCABD(tableFeatures, NumAgents, NumAgents)
                else:
                    tableFeatures, LowerIndex, UpperIndex = getData(filename, '&groupC')
                    if len(tableFeatures)>0:
                        CFactor_Init = readGroupC(tableFeatures, NumAgents, NumAgents)
                    else:
                        CFactor_Init = np.zeros((NumAgents, NumAgents))

            CArray = CFactor_Init
            PFactor = np.zeros((NumAgents, NumAgents))
            print("CArray:\n", np.shape(CArray), "\n", CArray, "\n")
            print("PFactor:\n", np.shape(PFactor), "\n", PFactor, "\n")
            for idai in range(NumAgents):
                #if ai.inComp == 0:
                #    continue
                if np.sum(CFactor_Init[idai,:])>0:
                    CArray[idai,:] = CArray[idai,:]/np.sum(CArray[idai,:])
                    for idaj in range(NumAgents):
                        if idaj == idai:
                            PFactor[idai,idaj] = 1-matrixP[idai,0]*np.sum(CArray[idai,:])
                        else:
                            PFactor[idai,idaj] = CArray[idai,idaj]*matrixP[idai,0]
                else:
                    for idaj in range(NumAgents):
                        if idaj == idai:
                           PFactor[idai,idaj] = 1.0
                        else:
                            PFactor[idai,idaj] = 0.0
            print("PFactor:\n", np.shape(PFactor), "\n", PFactor, "\n")
            matrixWP = PFactor

        f = open("out.txt", "w+")

        f.write("matrixWP\n"+str(matrixWP)+"\n")
        f.write("matrixIS\n"+str(matrixIS)+"\n")
        f.write("Number of Agents:"+str(NumAgents))
        if dataP:
            f.write("matrixP\n"+str(matrixP)+"\n")

        if DEBUG and sys.version_info[0] == 2:
            raw_input('Please check input data here!')
        if DEBUG and sys.version_info[0] == 3:
            input('Please check input data here!')

        OPIN = np.zeros((NumAgents, T))
        #Mov = np.zeros((Num_P, T))
        #MovSource = np.zeros((Num_P, T))

        print(OPIN[:,1])
        print(OPIN[1,:])
        #matrixIS.shape = 1,-1

        OPIN[:,0] = matrixIS.reshape((1,-1))

        numOfAgent = len(matrixIS)
        print("Number of Agent:", numOfAgent)
        print("Initial State of Agents:")
        print(OPIN[:,0])
        print(matrixIS)

        #MovComp = np.zeros((NumAgents, Num_P))
        #MovCompDir = np.zeros((NumAgents, Num_P))
        #MovCompInter = np.zeros((NumAgents, Num_P))

        eigval, eigvec  = np.linalg.eig(matrixWP)
        for i in range(len(eigval)):
            print('eigen_value:', eigval[i])
            print("eigen_vector:", eigvec[:,i])
            
        print("----------------------------")
        print("eigen_values:", eigval)
        print("----------------------------")
        
        if DEBUG and sys.version_info[0] == 2: 
            print >> f, "Initial State: OPIN[:,0]\n", OPIN[:,0], "\n"
        if DEBUG and sys.version_info[0] == 2: 
            raw_input('Please check data in initialization phase here!')
        if DEBUG and sys.version_info[0] == 3: 
            input('Please check data in initialization phase here!')

        print("Computing in iteration starts here!\n")
        f.write("Computing in iteration starts here!\n")

        for t in range(0, T-1):
            
            print("\n&&&&&&&&&&&&&&&&&&&")
            print("Time Step:", t)
            print("&&&&&&&&&&&&&&&&&&&\n")
            
            f.write("\n&&&&&&&&&&&&&&&&&&&&")
            f.write("Time Step:"+str(t))
            f.write("&&&&&&&&&&&&&&&&&&&&&&\n")
            

            for i in range(0, NumAgents):
                sum = 0.0
                for j in range(0, NumAgents):                    
                    #if np.fabs(OPIN[i,t])>1E-2:
                    sum = sum + matrixWP[i,j]*OPIN[j,t]
                OPIN[i,t+1]=sum


            #print "Movement integrated from the above matrix", Mov[:,t]
            print("OPIN[t]:", OPIN[:,t])
            print("OPIN[t+1]:", OPIN[:,t+1])
            #print("number of evacuees", np.sum(OPIN[:,t]))

            # Record opinions of agents in output data files: 
            f.write("OPIN[t]:"+str(OPIN[:,t])+"\n")
            f.write("OPIN[t+1]:"+str(OPIN[:,t+1])+"\n")

        f.close()

        #print('E1:', OPIN[0,:])
        #print('E2:', OPIN[1,:])
        #np.save("E1.npy",OPIN[0,:])
        #np.save("E2.npy",OPIN[1,:])
        np.save("dataResult.npy", OPIN)
        #plt.figure('data')
        for i in range(NumAgents):
            plt.plot(OPIN[i,:], linewidth=2.0, label=str(i+1))
            plt.text(0,OPIN[i,0], str(i), fontsize=18)
            
        (xDim, tDim)=np.shape(OPIN)
        timeline = np.linspace(0, tDim)
        plt.plot(timeline, timeline, linewidth='3.0', linestyle='-.')
        plt.title("Plot of Opinion Model")
        plt.xlabel("t" ) #, fontsize = 15)
        plt.ylabel("tpre") #, fontsize = 15)
        plt.grid()
        plt.legend(loc='best')
        #plt.ylim(0,7)
        plt.show()
        
        temp=filename.split('.')
        fnamePNG = temp[0]+'_opinion_plot.png'
        plt.savefig(fnamePNG)


if __name__ == '__main__':
    #test = np.random.multinomial(10, [0.1, 0.2, 0.7])
    T=11  # Simulation Timo Horizon [0, T]
    simulationOP('tpre2024_triple_2025Jan', T)
    #simulation('tpre_2022Nov.csv', T)
    #simulation('d0_2022Nov.csv', T)
