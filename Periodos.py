from numpy import linspace
from fase import*
from printa import*

def redefinir():
        '''Essa função é responsável por limpar os resultados anteriores
        e reler os dados de entrada'''

        #Importando as funções necessárias
        from os import mkdir,listdir
        from shutil import rmtree
        from os.path import isdir
        
        if isdir('./RESULTS/'):
            rmtree('./RESULTS/')
            
        mkdir('./RESULTS/')
        mkdir('./RESULTS/fase')
        mkdir('./RESULTS/Fase-Data')
        mkdir('./RESULTS/Fase/dispersas')

        return tuple(listdir('.\DATABASE'))

def imprimir(nome,periodos,log_periodo,mag):
        '''Essa função é responsável por imprimir os resultados
        em um arquivo  txt'''
        
        arquivo=open('./RESULTS/results.txt','a')
        arquivo.write('%s %f %f %f\n'%(nome,periodos,log_periodo,mag))
        arquivo.close()

def ajuste(X,Y):
        '''Essa função faz o ajuste linear e calcula
        a relação PL'''

        #Importando as funções necessárias
        from matplotlib.pyplot import scatter,title,xlabel,ylabel,close,gcf,plot,show
        from scipy.optimize import curve_fit
        from numpy import sqrt,diag
        
        function = (lambda u,a,b: u*a + b)
        popt,cov=curve_fit(function,X,Y)
        error = sqrt(diag(cov))
        
        t=linspace(min(X),max(X))
        y_reg = function(t, popt[0],popt[1])

        scatter(X,Y,c='k')
        plot(t,y_reg,"-r")
        title('m = (%.5f +- %.5f) * log(P) + (%.5f +- %.5f)'%(popt[0],error[0],popt[1],error[1]))
        xlabel('log(Periodo)')
        ylabel('Magnitude Aparente')
        (gcf()).savefig('./RESULTS/PL.png', format='png')
        close()
        
def main():
        '''Essa é a função principal do programa'''

        #Importando as funções necessárias
        from matplotlib.pyplot import clf
        from numpy import log10,mean,loadtxt
        from astropy.timeseries import LombScargle
        from os.path import splitext        
        
        #Lendo o DATABASE
        per_mag=[],[]     
        DATABASE= redefinir()

        #Iniciando o algoritmo para cada estrela no DATABASE
        for i in DATABASE:
            clf()
            print('(1-3)Processando a estrela ',i)
            texto=splitext(i)

            #Carregando os Arquivos:        
            data=loadtxt('.\DATABASE\%s'%(texto[0]+texto[1]),delimiter=' ')
            t=tuple(data[:,0])
            y=tuple(data[:,1])
            del(data)
            
            #Calculando os Periodos:            
            aux_1=LombScargle(t, y).autopower() #Uso do Periodograma LombScargle
            a,b = list(((1/aux_1[0]).copy()).flatten()) ,list(((aux_1[1]).copy()).flatten())
            del(aux_1)
            periodos=a[b.index(max(b))] #Definindo o periodo mais provável a partir do Periodograma
            del(a,b)

            mag=mean(y)            
            log_p=log10(periodos)
            
            #Imprimindo o Relatório
            imprimir(texto[0]+texto[1],periodos,log_p,mag)

            #Guardando os resultados em variaveis           
            per_mag[0].append(log_p)
            per_mag[1].append(mag)
            del(mag)
            clf()

            del(t,y,periodos,texto)

            
        del(DATABASE,i)        
        ajuste(list(per_mag[0]),list(per_mag[1]))        
        return 

main()
fase()
printa()
print("Calculos Concluidos... Programa encerrado")
