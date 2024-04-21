# --------------------------------------------------------------------------------
# Documentação:
#               https://docs.python-requests.org/en/latest/
#
# Instalação:
#               pip3 install requests
# --------------------------------------------------------------------------------
 
import requests

# --------------------------------------------------------------------------------
# Converte a lista de cotacoes em um dicionário
def list_2_dict(lista_valores):
    dict_retorno = dict()

    for linha in lista_valores:
        data         = linha['dataHoraCotacao'][0:10]
        valor_compra = linha['cotacaoCompra']
        valor_venda  = linha['cotacaoVenda']
        dict_retorno[data] = { 'cotacaoCompra': valor_compra, 'cotacaoVenda': valor_venda }

    return dict_retorno
# --------------------------------------------------------------------------------

#Pego um período baseado no que o usuário quer
#Ano
ano = input("Digite o ano que você deseja saber a cotação.\nOBS:Escolha um ano que não tenha se passado.\n>")
#mês início
mesIni = input("Digite o mês inicial que você deseja do período.\nOBS:Não escolha um mês maior que o final.\n>")
#mês fim
mesFim = input("Digite o mês que representa o final do período.\nOBS:Não escolha um mês menor que o primeiro.\n>")

#url das consultas
url  = 'https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/'
url += 'CotacaoDolarPeriodo(dataInicial=@dataInicial,dataFinalCotacao=@dataFinalCotacao)?'
#ultima consulta modificada para eu poder fazer a minha pesquisa de acordo com os parâmetros
url += '@dataInicial=%27'+mesIni+'-01-'+ ano +'%27&@dataFinalCotacao=%27'+mesFim+'-31-'+ano+'%27&$format=json'

#pega os dados em json
dados_brutos = requests.get(url).json()
#cria um dicionário
retorno_dados = list_2_dict(dados_brutos['value'])
#meu dicionário a partir do dicionário gerado
dicionario = {}
#vou começar indo do período do mes inicial ao mes final
for x in range(int(mesIni), int(mesFim)+1):
    #pego a string que representa o mês
    if x <= 9:
        mes = '0' + str(x)
    else:
        mes = str(x)
    #crio uma lista com os valores da cotação de cada mês
    valores = []
    #aqui vai servir como a chave, que é o ano/mês
    mesV = '' 
    #vou em dia por dia de cada mês, presumindo que ele tem até 31 dias, começando do dia 1
    for y in range(1,32):
        #modifico o dia para o padrão que eu quero
        if y <= 9:
            dia = '0' + str(y)
        else:
            dia = str(y)
        #monto a data para procurar no dicionário, que no caso vai ser a chave
        data = f"{ano}-{mes}-{dia}"
        #isso aqui é para criar a chave do meu próprio dicionário
        mesV = f"{ano}-{mes}"
        #tente fazer isso se conseguir
        try:
            #pego a data e uso como chave na busca
            dic = retorno_dados[data]
            #pego o valor em decimal e jogo na lista do mês 
            valores.append(float(dic['cotacaoCompra']))
        #se der erro, a data n tem valores e eu não faço nada :P
        except:
            #pra não fazer nada
            nada = 0
    #pego a média dos valores
    media = sum(valores)/len(valores)
    #pego a maior cotação
    maior = max(valores, key=float)
    #boto no meu dicionário
    dicionario[mesV] = {'maiorCotacao': maior, 'mediaCotacao': media}
#mostro ele
print(dicionario)