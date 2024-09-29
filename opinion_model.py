

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

logging.basicConfig(filename='log_examp.log',level=logging.DEBUG)
logging.debug('This message should go to the log file')
logging.info('So should this')
logging.warning('And this, too')


def simulationOP(filename, T, DEBUG=True):

        # Time Horizon: T

        # Read in csv file
        #fileName

        print('\nBuilding Models\n')

        dataIS, isStart, isEnd = getData(filename, "&inti")
        #dataCapa, capaStart, capaEnd = getData(filename, "&capa")
        #dataBLD, bldStart, bldEnd = getData(filename, "&bld")
        dataWP, wpStart, wpEnd = getData(filename, "&prob")

        print(dataIS)
        print(dataWP)

        Num_X=np.size(dataIS)
        Num_R=Num_X-1

        matrixIS=readFloatArray(dataIS, Num_R, 1)
        matrixWP=readFloatArray(dataWP, Num_R, Num_R)


        # %%%% Input parameter check
        if np.shape(matrixWP)!= (Num_R, Num_R):
            print('\nError on input parameter\n')
            
        if matrixIS.shape[0]!=Num_R:
            print('\nError with matrixIS\n')

        print(matrixWP)
        print(matrixIS)

        f = open("out.txt", "w+")

        f.write("matrixWP\n"+str(matrixWP)+"\n")
        f.write("matrixIS\n"+str(matrixIS)+"\n")
        f.write("Number of Agents:"+str(Num_R))
        #f.wrtie("dimension of matrixCapa"+str(np.shape(matrixCapa)))
        #f.wrtie("maximal element in matrixCapa"+str(np.max(matrixCapa)))

        temp=arr1D_2D(dataIS)
        NameLocation =np.transpose(temp)[0,1:]
        #NameLocation=['E1', 'E2', 'H1', 'H2', 'H3', 'O1', 'O2', 'O3', 'L1', 'L2', 'L3']
        #BLD_Index_Room=cellstr(NameLocation);   %Colomn Vector

        #temp=arr1D_2D(dataCapa)
        #NamePassage =temp[0,1:]
        #NamePassage=['H1->E1', 'H3->E2', 'O1->H1', 'O2->H2', 'O3->H3', 'L1->H1', 'L2->H2', 'L3->H3', 'H2->H1', 'H2->H3', 'O2->O1', 'O2->O3', 'L2->L1']
        #BLD_Index_Path=cellstr(NamePassage);   %Colomn Vector

        print(NameLocation)
        #print(NamePassage)
        print("Some Testing Cases:")


        if DEBUG and sys.version_info[0] == 2: 
            raw_input('Please check input data here!')
        if DEBUG and sys.version_info[0] == 3:
            input('Please check input data here!')

        X = np.zeros((Num_R, T))
        #Mov = np.zeros((Num_P, T))
        #MovSource = np.zeros((Num_P, T))

        print(X[:,1])
        print(X[1,:])
        #matrixIS.shape = 1,-1

        X[:,0] = matrixIS.reshape((1,-1))

        numOfPeople = len(matrixIS)
        print("Number of People:", numOfPeople)

        print("Initial State of the Model")
        print(X[:,0])
        print(matrixIS)

        #MovComp = np.zeros((Num_R, Num_P))
        #MovCompDir = np.zeros((Num_R, Num_P))
        #MovCompInter = np.zeros((Num_R, Num_P))


        if DEBUG and sys.version_info[0] == 2: 
            print >> f, "Initial State: X[:,0]\n", X[:,0], "\n"
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
            

            for i in range(0, Num_R):
                sum = 0.0
                for j in range(0, Num_R):                    
                    #if np.fabs(X[i,t])>1E-2:
                    sum = sum + matrixWP[i,j]*X[j,t]
                X[i,t+1]=sum
                

            '''
            # Check the math model: 
            # Is the flow generated correct?  We need to check it
            for i in range(0, Num_R):
                if np.sum(MovComp[i,:])>X[i,t]:
                    print("!!!!!!!!!!!!!!!")
                    print("error found here! About MovComp")
                    print("Flow generated exceeds the source!")
                if np.sum(MovCompInter[i,:])>X[i,t]:
                    print("!!!!!!!!!!!!!!!")
                    print("error found here! About MovCompInter")
                    print("Flow generated exceeds the source!")
                if np.sum(matrixWP[i,:])>1:
                    print("!!!!!!!!!!!!!!!")
                    print("error found here! About matrixWP")
                    print("Flow generated exceeds the source!")
                    print("error location:", i)


            print("Movement Information:")
            print("MovComp: \n", MovComp)
            print("MovCompDir: \n", MovCompDir)
            print("MovCompInter: \n", MovCompInter)
            print("Mov[:,t]: \n", Mov[:,t])
            
            f.write("MovComp: \n"+str(MovComp)+"\n")
            f.write("MovCompDir: \n"+str(MovCompDir)+"\n")
            f.write("MovCompInter: \n"+str(MovCompInter)+"\n")
            f.write("Mov[:,t]: \n"+str(Mov[:,t])+"\n")
            f.write("MovSource[:,t]: \n"+str(MovSource[:,t])+"\n")


            #for j in range(0, Num_P-1):
            #    if Mov[j,t] > matrixCapa[0,j]:
            #	Mov[j,t] = matrixCapa[0,j]
            #	print "print here to show that this line is being run"
            #	print "********************"
            #	print "********************"


            #X = X + BLD*Mov
            X[:,t+1] = X[:,t] + np.dot(matrixBLD, Mov[:,t])

            '''

            #print "Movement integrated from the above matrix", Mov[:,t]
            print("X[t]:", X[:,t])
            print("X[t+1]:", X[:,t+1])
            #print("number of evacuees", np.sum(X[:,t]))

            f.write("X[t]:"+str(X[:,t])+"\n")
            f.write("X[t+1]:"+str(X[:,t+1])+"\n")
            #f.write("number of evacuees"+str(np.sum(X[:,t]))+"\n")

        f.close()

        #print('E1:', X[0,:])
        #print('E2:', X[1,:])
        #np.save("E1.npy",X[0,:])
        #np.save("E2.npy",X[1,:])
        np.save("dataResult.npy", X)
        #plt.figure('data')
        for i in range(Num_R):
            plt.plot(X[i,:])
        plt.show()
        temp=filename.split('.')
        fnamePNG = temp[0]+'_exitprob.png'
        plt.savefig(fnamePNG)


if __name__ == '__main__':
    #test = np.random.multinomial(10, [0.1, 0.2, 0.7])
    T=26  # Simulation Timo Horizon [0, T]
    simulationOP('example2022Nov20.csv', T)
    #simulation('tpre_2022Nov.csv', T)
    #simulation('d0_2022Nov.csv', T)
