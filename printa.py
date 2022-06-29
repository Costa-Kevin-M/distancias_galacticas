from matplotlib.pyplot import scatter,title,xlabel,ylabel,close,gcf,imshow
from matplotlib import use
from numpy import loadtxt,remainder,concatenate,genfromtxt,mean,std,sum,array
from astropy.timeseries import LombScargle
from shutil import rmtree,move
from os import mkdir,listdir
from os.path import isdir,splitext
import cv2
from PIL import Image


def printa():

        relatorio=genfromtxt('.\RESULTS\\results.txt',dtype=str,delimiter=' ')
        for i in range(len(relatorio)):

            nome=splitext(relatorio[i][0])
            data=genfromtxt('.\RESULTS\\Fase-Data\\%s.txt'%nome[0],delimiter=' ')
            
            print('(3-3) Imprimindo a Fase da estrela: ',nome[0])

            x=list([k[0] for k in data])
            y=list([k[1] for k in data])
        
            magnitude=float(relatorio[i][2])            
            scatter(x,y,c='k')
            title('Periodo: %f / Magnitude: %f'%(float(relatorio[i][1]),magnitude))
            xlabel('Fase')
            ylabel('Magnitude')
            (gcf()).savefig('./RESULTS/Fase/%s-Fase.png'%nome[0], format='png')
            close('all')
            use('PS')

            img= cv2.imread('./RESULTS/Fase/%s-Fase.png'%nome[0])
            
            white=sum(img == 255)
            black=sum(img == 0)
            dispersao=black/white



            corte=Image.open('./RESULTS/Fase/%s-Fase.png'%nome[0])
            corte=corte.crop((77, 225, corte.size[0]-60,corte.size[1]-225))
            corte=array(corte)

            white=sum(corte == 255)
            black=sum(corte == 0)            
            corte=black/white
            

            min_disp=0.05
            max_disp=0.15            

            min_cort=0.02
            max_cort=0.12
          
            if dispersao>max_disp or dispersao<min_disp:
                    move('./DATABASE/%s'%relatorio[i][0],'./DISPERSAO/%s'%relatorio[i][0])
                    move('./RESULTS/Fase/%s-Fase.png'%nome[0],'./RESULTS/Fase/dispersas/%s-Fase.png'%nome[0])
            else:
                    if corte>max_cort or corte<min_cort:
                            move('./DATABASE/%s'%relatorio[i][0],'./DISPERSAO/%s'%relatorio[i][0])
                            move('./RESULTS/Fase/%s-Fase.png'%nome[0],'./RESULTS/Fase/dispersas/%s-Fase.png'%nome[0])
                            
            arquivo=open('.\RESULTS\dispersao.txt','a')
            arquivo.write('%s dispersão: %f corte: %f\n'%(nome[0],dispersao,corte))
            arquivo.close()
            
            del(data,nome,magnitude)
            
            
        return

