from matplotlib.pyplot import scatter,title,xlabel,ylabel,close,gcf
from numpy import loadtxt,remainder,concatenate,genfromtxt,mean,std
from astropy.timeseries import LombScargle
from shutil import rmtree
from os import mkdir,listdir
from os.path import isdir,splitext

def phase_fold(t,y,period):
    
#Essa Função Transforma a Fotometria no Espaço de Fase
    
    phases=remainder(t,period)/period
    return concatenate((phases,phases+1)),concatenate((y,y))


def fase():

#Lendo o DATABASE
        
        aux=tuple(listdir('.\DATABASE'))
        relato=genfromtxt('.\RESULTS\\results.txt',dtype=str,delimiter=' ')
        star=[[x[0] for x in relato],[x[1] for x in relato]]
        del(relato)
        
        for i in range(len(star[0])):
            print('(2-3) Calculando Espaço de Fase da estrela ',star[0][i])

#Carregando os Arquivos:
            
            data=loadtxt('.\DATABASE\%s'%(star[0][i]),delimiter=' ')
            periodos=float(star[1][i])
            t=tuple(data[:,0][1:])
            y=tuple(data[:,1][1:])          
            del(data)
            

#Imprimindo os Dados:

            a1,a2=phase_fold(t,y,periodos)
            del(y)
            a1=tuple(a1.tolist()),tuple(a2.tolist())           
            del(a2)
            arquivo=open('./RESULTS/Fase-Data/%s.txt'%splitext(star[0][i])[0],'a')
            for i in range(len(a1[0])):
                    arquivo.write("%f %f\n"%(a1[0][i],a1[1][i]))
            arquivo.close()
            del(arquivo,a1,periodos)

#Feedback de Operação
            
        del(aux)    
        print('\nCalculos de Fase concluidos',end='')
        print(".",end='')
        print('.',end='')
        print('.     ',end='')
        print('Iniciando Impressão')
        return
