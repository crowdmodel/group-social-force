

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

import re
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

try:
    import scipy.stats
except:
    print("Warning: scipy.stat cannot be imported.  Unable to generate random variables!")
    if sys.version_info[0] == 2: 
        raw_input("Please check!")
    else:
        input("please check!")

logging.basicConfig(filename='log_examp.log',level=logging.DEBUG)
logging.debug('This message should go to the log file')
logging.info('So should this')
logging.warning('And this, too')


def simulationOP(filename, T, DEBUG=True, antago_model="WP", model="French-DeGroot", hkmodel=None, randmodel=None, LB=None, UB=None):

        # Time Horizon: T
        # Read in csv file
        #fileName
        
        #anta_model="2017Liu" 
        #anta_model=str()
        #model="random" 
        #model="FJ"

        if findKey(filename, '&lowerbound', '&LowerBound', '&LB'):
            LB = str(findKey(filename, '&lowerbound', '&LowerBound', '&LB'))
            if LB != "None":
                LB = float(LB)
            else:
                LB = None
                    
        if findKey(filename, '&upperbound', '&UpperBound', '&UB'):
            UB = str(findKey(filename, '&upperbound', '&UpperBound', '&UB'))
            if UB != "None":
                UB = float(UB)
            else:
                UB = None
        
        if findKey(filename, '&antago_model', '&Antago_Model', '&Antago_model'):
            antago_model = str(findKey(filename, '&antago_model', '&Antago_Model', '&Antago_model'))
        if findKey(filename, '&model', '&Model', '&MODEL'):
            model = str(findKey(filename, '&model', '&Model', '&MODEL'))
            
        if findKey(filename, '&threshold', '&Threshold', '&THRESHOLD'):
            threshold = str(findKey(filename, '&threshold', '&Threshold', '&THRESHOLD'))
        if findKey(filename, '&hkmodel', '&HKModel', '&HKMODEL'):
            hkmodel = str(findKey(filename,  '&hkmodel', '&HKModel', '&HKMODEL'))

        if findKey(filename, '&random', '&Random', '&RANDOM'):
            randmodel = str(findKey(filename,  '&random', '&Random', '&RANDOM'))

        if findKey(filename, '&random_ini', '&Random_Ini', '&RANDOM_INI'):
            randini = str(findKey(filename,  '&random_ini', '&Random_Ini', '&RANDOM_INI'))
          
        print('\nBuilding Models\n')
        print('antago_model:', antago_model)
        print('model:', model)

        dataIS, isStart, isEnd = getData(filename, "&inti")
        dataP, pStart, pEnd = getData(filename, "&p")
        dataLambda, lStart, lEnd = getData(filename, "&lambda")
        dataEta, lStart, lEnd = getData(filename, "&eta")
        
        # Read the inital value x(0) and fix the number of agents
        if len(dataIS)>1:

            NumAgents=len(dataIS)-1
            matrixIS=readFloatArray(dataIS, NumAgents, 1)
            if matrixIS.shape[0]!=NumAgents:
                print('\nError with matrixIS\n')

            dataC, cStart, cEnd = getData(filename, "&groupC")
            dataWP, wpStart, wpEnd = getData(filename, "&prob")

            print(dataIS)
            print(dataWP)
            print(dataP)
            print(dataLambda)
            print(dataEta)
            print(dataC)

            if len(dataP)>1:
                matrixP=readFloatArray(dataP, NumAgents, 1)
                if matrixP.shape[0]!=NumAgents:
                    print('\nError with matrixP\n')

            if len(dataLambda)>1:
                matrixL=readFloatArray(dataLambda, NumAgents, 1)
                if matrixL.shape[0]!=NumAgents:
                    print('\nError with matrixL for FJ opinion model!\n')
            else:
                if model=="FJ":
                    matrixL=np.ones((NumAgents, 1))
                else:
                    matrixL=np.zeros((NumAgents, 1))

            if len(dataEta)>1:
                matrixE=readFloatArray(dataEta, NumAgents, 1)
                if matrixE.shape[0]!=NumAgents:
                    print('\nError with matrixE for random signal input!\n')
            else:
                if randmodel:
                    matrixE=np.ones((NumAgents, 1))
                else:
                    matrixE=np.zeros((NumAgents, 1))

            if len(dataWP)>1:
                matrixWP=readFloatArray(dataWP, NumAgents, NumAgents)
                # %%%% Input parameter check
                if np.shape(matrixWP)!= (NumAgents, NumAgents):
                    print('\nError on input parameter\n')
            else:
                matrixWP=np.zeros((NumAgents, NumAgents))
                
            if len(dataP)>1 and len(dataC)>1 and len(dataP)==len(dataC): #and hkmodel!="HK0":

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
                                #if re.match("2017Liu", antago_model):
                                if antago_model=="2017Liu": 
                                    PFactor[idai,idaj] = 1-matrixP[idai,0]
                                else:
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
            #print("matrixP:\n", np.shape(matrixP), "\n", matrixP, "\n")
            print("matrixL:\n", np.shape(matrixL), "\n", matrixL, "\n")
            
        else:
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
                        tableFeatures, LowerIndex, UpperIndex = getData(filename, '&groupS')
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
                            #if re.match("2017Liu", antago_model):
                            if antago_model=="2017Liu":    
                                PFactor[idai,idaj] = 1-matrixP[idai,0]
                            else:
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
        #print(OPIN[:,0])
        #print(OPIN[1,:])
        #matrixIS.shape = 1,-1
        if randini=='lognorm' or 'Lognorm':
            OPIN[:,0] =scipy.stats.lognorm.rvs(loc=0, scale=1, size=NumAgents)
        elif randini=='logistic' or 'Logistic':
            OPIN[:,0] =scipy.stats.norm.rvs(loc=0, scale=1, size=NumAgents)
        else:
            OPIN[:,0] = matrixIS.reshape((1,-1))
            
        OPIN_CompConverg=OPIN[:,0]
        t_OPIN_CompConverg=0
        flag_OPIN_CompConverg=False

        #numOfAgent = len(matrixIS)
        print("antago_model= ", antago_model)
        print("model= ", model)
        
        print("Number of Agent:", NumAgents)
        print("Initial State of Agents:")
        print(OPIN[:,0])
        print(matrixIS)
        print(matrixWP)

        #MovComp = np.zeros((NumAgents, Num_P))
        #MovCompDir = np.zeros((NumAgents, Num_P))
        #MovCompInter = np.zeros((NumAgents, Num_P))

        matrixComp = np.zeros((NumAgents, NumAgents))
        for i in range(0, NumAgents):
            for j in range(0, NumAgents):
                if model=='FJ':
                    matrixComp[i,j] = matrixWP[i,j]*matrixL[i,0]
                #if model=='random':
                else:
                    matrixComp[i,j] = matrixWP[i,j]

        print(matrixComp)
        #eigval, eigvec  = np.linalg.eig(matrixWP)
        eigval, eigvec  = np.linalg.eig(matrixComp)
        spectralRadius = abs(np.max(eigval))

        print("---------------------------------------------")
        print("------------Right Side Eigen----------------")
        print("---------------------------------------------")
        print('+++spectral radius:+++', spectralRadius)
        print("----------------------------")
        print("eigen_values:", eigval)
        print("----------------------------")
        for i in range(len(eigval)):
            print('eigen_value:', eigval[i])
            print('modulus of eigen_value:', abs(eigval[i]))
            print("eigen_vector:", eigvec[:,i], np.linalg.norm(eigvec[:,i]))

        f.write("----------------------------------\n")
        f.write("eigen_values:"+str(eigval)+"\n")
        f.write("-----------------------------------\n")

        #eigval, eigvec  = np.linalg.eig(np.transpose(matrixWP))
        eigval, eigvec  = np.linalg.eig(np.transpose(matrixComp))
        eigvec_important = None
        converged_val = None

        print("---------------------------------------------")
        print("------------Left Side Eigen----------------")
        print("---------------------------------------------")
        print("eigen_values_lhs:", eigval)
        print("----------------------------")
        for i in range(len(eigval)):
            print('eigen_value_lhs:', eigval[i])
            print('modulus of eigen_value_lhs:', abs(eigval[i]))
            print("eigen_vector_lhs:", eigvec[:,i], np.linalg.norm(eigvec[:,i]))
            if abs(eigval[i]-1.0)<1e-10:
                eigvec_important=eigvec[:,i]/np.sum(eigvec[:,i])
                converged_val=np.dot(OPIN[:,0], eigvec_important)
                print("===For converged_value:===OPIN[t=0]:", OPIN[:,0])
                print("===For converged_value:===eigenvector:", eigvec_important)
                print("===For converged_value:===", converged_val)
                
        print("----------------------------")          
        print("===converged_value:===", converged_val)
        print("----------------------------")

        f.write("----------------------------------\n")
        f.write("eigen_values_lhs:"+str(eigval)+"\n")
        f.write("-----------------------------------\n")

        f.write("----------------------------------\n")
        f.write("converged_value:"+str(converged_val)+"\n")
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

            if hkmodel=='HK0':
                CArray=np.zeros((NumAgents, NumAgents))
                PFactor=np.zeros((NumAgents, NumAgents))
                for idai in range(0, NumAgents):
                    for idaj in range(0, NumAgents):
                        if idai==idaj:
                            continue
                        elif fabs(OPIN[idai, t]-OPIN[idaj, t])<float(threshold):
                            CArray[idai, idaj]=1
                        else:
                            CArray[idai, idaj]=0
                    if np.sum(np.fabs(CArray[idai,:]))>0:
                        CArray[idai,:] = np.sign(CArray[idai,:])*np.fabs(CArray[idai,:])/np.sum(np.fabs(CArray[idai,:]))
                        for idaj in range(NumAgents):
                            if idaj == idai:
                                #if re.match("2017Liu", antago_model):
                                if antago_model=="2017Liu": 
                                    PFactor[idai,idaj] = 1-matrixP[idai,0]
                                else:
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

            if hkmodel=='HK':
                CKArray=np.zeros((NumAgents, NumAgents))
                KArray=np.zeros((NumAgents, NumAgents))
                # Diagonal elements of KArray and CKArray are all zeros
                for idai in range(0, NumAgents):
                    for idaj in range(0, NumAgents):
                        if idai==idaj:
                            continue
                        elif fabs(OPIN[idai, t]-OPIN[idaj, t])<float(threshold):
                            KArray[idai, idaj]=1
                        else:
                            KArray[idai, idaj]=0
                        CKArray[idai, idaj]=KArray[idai, idaj]*CArray[idai, idaj]
                            
                for idai in range(0, NumAgents):
                    if np.sum(np.fabs(CKArray[idai,:]))>0: # Agent socially connected with others
                        CKArray[idai,:] = CKArray[idai,:]/np.sum(np.fabs(CKArray[idai,:]))
                        for idaj in range(NumAgents):
                            if idaj == idai:
                                #if re.match("2017Liu", antago_model):
                                if antago_model=="2017Liu": 
                                    PFactor[idai,idaj] = 1-matrixP[idai,0]
                                else:
                                    PFactor[idai,idaj] = 1-matrixP[idai,0]*np.sum(CKArray[idai,:])
                            else:
                                PFactor[idai,idaj] = CKArray[idai,idaj]*matrixP[idai,0]
                    else: # Isolated agent
                        for idaj in range(NumAgents):
                            if idaj == idai:
                                PFactor[idai,idaj] = 1.0
                            else:
                                PFactor[idai,idaj] = 0.0
                print("PFactor:\n", np.shape(PFactor), "\n", PFactor, "\n")
                matrixWP = PFactor

            for i in range(0, NumAgents):

                # Compute the baseline French-DeGroot model
                sum = 0.0
                for j in range(0, NumAgents):                    
                    #if np.fabs(OPIN[i,t])>1E-2:
                    sum = sum + matrixWP[i,j]*OPIN[j,t]

                # Compute FJ model: Integrate the initial opinion profiles in the dynamical process
                if model=="FJ":
                    OPIN[i,t+1]=sum*matrixL[i,0]+(1-matrixL[i,0])*OPIN[i,0]
                else:
                    OPIN[i,t+1]=sum

                if randmodel:
                    rand_thoughts = 2*(random.random()-0.5)
                    #np.random.normal(loc=0, scale=1)
                    #scipy.stats.norm.rvs(loc=0, scale=1, size=1)
                    #scipy.stats.uniform.rvs(size=1)-0.5 #random.random()-0.5 #
                    #2*(random.random()-0.5) #scipy.stats.uniform.rvs(size=1)-0.5
                    OPIN[i,t+1]=OPIN[i,t+1]+matrixE[i,0]*rand_thoughts

                #Confine the opinion within the range of [LB, UB]
                if UB is not None and OPIN[i,t+1]>UB:
                    OPIN[i,t+1]=UB
                    flag_OPIN_CompConverg=True

                if LB is not None and OPIN[i,t+1]<LB:
                    OPIN[i,t+1]=LB
                    flag_OPIN_CompConverg=True
            
            if flag_OPIN_CompConverg:
                OPIN_CompConverg = OPIN[:,t+1]
                t_OPIN_CompConverg = t+1
                flag_OPIN_CompConverg=False
                
            print("OPIN[t]:", OPIN[:,t])
            print("OPIN[t+1]:", OPIN[:,t+1])
            #print("number of evacuees", np.sum(OPIN[:,t]))

            # Record opinions of agents in output data files:
            f.write("OPIN[t]:"+str(OPIN[:,t])+"\n")
            f.write("OPIN[t+1]:"+str(OPIN[:,t+1])+"\n")


        converged_val=np.dot(OPIN_CompConverg, eigvec_important)
        print("\n")
        print("spectral radius:", spectralRadius)
        if spectralRadius >1.0:
            print("Not converged because spectral radius is larger than 1.0\n.")
        else:
            print("Final Value Converged:")
            print("+++Original converged value+++:", np.dot(OPIN[:,0], eigvec_important))
            print("===For converged_value:===OPIN_CompConverg:", OPIN_CompConverg)
            print("===For converged_value:===t_OPIN_CompConverg:", t_OPIN_CompConverg)
            print("===For converged_value:===eigenvector:", eigvec_important)
            print("===For converged_value:===", converged_val)
                
        f.close()

        #print('E1:', OPIN[0,:])
        #print('E2:', OPIN[1,:])
        #np.save("E1.npy",OPIN[0,:])
        #np.save("E2.npy",OPIN[1,:])
        np.save("dataResult.npy", OPIN)
        #plt.figure('data')
        for i in range(NumAgents):
            plt.plot(OPIN[i,:], linewidth=2.0, label=str(i+1))
            plt.text(0,OPIN[i,0], str(i+1), fontsize=18)
            
        (xDim, tDim)=np.shape(OPIN)
        timeline = np.linspace(0, tDim)
        plt.plot(timeline, timeline, linewidth='3.0', linestyle='-.')
        plt.title("Plot of Opinion Model")
        plt.xlabel("t" ) #, fontsize = 15)
        plt.ylabel("tpre") #, fontsize = 15)
        plt.grid()
        if antago_model != 'HK':
            plt.legend(loc='upper right')

        temp=filename.split('.')
        fnamePNG = temp[0]+'_opinion_plot.png'
        plt.savefig(fnamePNG)
        #plt.ylim(0,7)
        plt.show()

if __name__ == '__main__':
    #test = np.random.multinomial(10, [0.1, 0.2, 0.7])
    T=11  # Simulation Timo Horizon [0, T]
    simulationOP('tpre2024_triple_2025Jan', T)
    #simulation('tpre_2022Nov.csv', T)
    #simulation('d0_2022Nov.csv', T)
