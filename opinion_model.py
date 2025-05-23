

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
#import matplotlib.pyplot as plt
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

try:
    import networkx
except:
    print("Warning: networkx cannot be imported.  Unable to draw graph model!")
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
            dataWP, wpStart, wpEnd = getData(filename, "&prob")
            dataP, pStart, pEnd = getData(filename, "&p")
            dataLambda, lStart, lEnd = getData(filename, "&lambda")
            dataC, cStart, cEnd = getData(filename, "&groupC")


            print(dataIS)
            print(dataWP)
            print(dataP)
            print(dataLambda)
            print(dataC)

            NumAgents=len(dataIS)-1

            matrixIS=readFloatArray(dataIS, NumAgents, 1)
            if matrixIS.shape[0]!=NumAgents:
                print('\nError with matrixIS\n')

            if len(dataLambda)>1:
                matrixL=readFloatArray(dataLambda, NumAgents, 1)
                if matrixL.shape[0]!=NumAgents:
                    print('\nError with matrixL\n')
            else:
                matrixL=np.ones((NumAgents, 1))

            if len(dataWP)>1:
                matrixWP=readFloatArray(dataWP, NumAgents, NumAgents)
                # %%%% Input parameter check
                if np.shape(matrixWP)!= (NumAgents, NumAgents):
                    print('\nError on input parameter\n')

            if len(dataP)>1 and len(dataC)>1 and len(dataP)==len(dataC):

                matrixP=readFloatArray(dataP, NumAgents, 1)
                if matrixP.shape[0]!=NumAgents:
                    print('\nError with matrixP\n')

                CArray=readFloatArray(dataC, NumAgents, NumAgents)
                if CArray.shape!=(NumAgents, NumAgents):
                    print('\nError with CArray\n')

                print("matrixP:\n", np.shape(matrixP), "\n", matrixP, "\n")
                print("CArray:\n", np.shape(CArray), "\n", CArray, "\n")

                PFactor = np.zeros((NumAgents, NumAgents))
                print("CArray:\n", np.shape(CArray), "\n", CArray, "\n")
                for idai in range(NumAgents):
                    #if ai.inComp == 0:
                    #    continue
                    if np.sum(np.fabs(CArray[idai,:]))>0:
                        CArray[idai,:] = np.sign(CArray[idai,:])*np.fabs(CArray[idai,:])/np.sum(np.fabs(CArray[idai,:]))
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

            print("matrixWP:\n", np.shape(matrixWP), "\n", matrixWP, "\n")
            print("matrixIS:\n", np.shape(matrixIS), "\n", matrixIS, "\n")
            print("matrixL:\n", np.shape(matrixL), "\n", matrixL, "\n")
            
        except:

            agents, agent2exit, agentgroup = readSocialArrayCSV(filename, debug=True, marginTitle=1)
            NumAgents=len(agents)-1
            print("Number of Agent:", NumAgents)
            
            matrixIS = np.zeros((NumAgents, 1))
            matrixP = np.zeros((NumAgents, 1))
            matrixL = np.ones((NumAgents, 1))

            for idai in range(NumAgents):
                matrixIS[idai,0]= agents[idai+1][6]
                matrixP[idai,0] = agents[idai+1][7]
                #matrixL[idai,0] = agents[idai+1][13]

            #print(agents)
            print("matrixIS:\n", matrixIS, "\n")
            print("matrixL:\n", matrixL, "\n")
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
            #print("PFactor:\n", np.shape(PFactor), "\n", PFactor, "\n")
            for idai in range(NumAgents):
                #if ai.inComp == 0:
                #    continue
                if np.sum(np.fabs(CArray[idai,:]))>0:
                    CArray[idai,:] = np.sign(CArray[idai,:])*np.fabs(CArray[idai,:])/np.sum(np.fabs(CArray[idai,:]))
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
        f.write("---------------------------------------------------------------------\n")
        f.write("-------------------Opinion Dynamic Process-------------------\n")
        f.write("---------------------------------------------------------------------\n")
        f.write("Date&Time:"+time.strftime('%Y-%m-%d_%H_%M_%S')+"\n")
        f.write("matrixWP\n"+str(matrixWP)+"\n")
        f.write("matrixIS\n"+str(matrixIS)+"\n")
        f.write("matrixL\n"+str(matrixL)+"\n")
        f.write("Number of Agents:"+str(NumAgents))
        try:
            f.write("matrixP\n"+str(matrixP)+"\n")
            f.write("matrixC\n"+str(CArray)+"\n")
        except:
            f.write("No matrixP or CArray defined! \n")

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

        #numOfAgent = len(matrixIS)
        print("Number of Agent:", NumAgents)
        print("Initial State of Agents:")
        print(OPIN[:,0])
        print(matrixIS)

        #MovComp = np.zeros((NumAgents, Num_P))
        #MovCompDir = np.zeros((NumAgents, Num_P))
        #MovCompInter = np.zeros((NumAgents, Num_P))

        matrixComp = np.zeros((NumAgents, NumAgents))
        for i in range(0, NumAgents):
            for j in range(0, NumAgents):
                matrixComp[i,j] = matrixWP[i,j]*matrixL[i,0]

        #eigval, eigvec  = np.linalg.eig(matrixWP)
        eigval, eigvec  = np.linalg.eig(matrixComp)
        for i in range(len(eigval)):
            print('eigen_value:', eigval[i])
            print("eigen_vector:", eigvec[:,i])
            
        print("----------------------------")
        print("eigen_values:", eigval)
        print("----------------------------")

        f.write("----------------------------------\n")
        f.write("eigen_values:"+str(eigval)+"\n")
        f.write("-----------------------------------\n")

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
                OPIN[i,t+1]=sum*matrixL[i,0]+(1-matrixL[i,0])*OPIN[i,0]

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
            plt.plot(OPIN[i,:], linewidth=2.0, label=str(i))
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
