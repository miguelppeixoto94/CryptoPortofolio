#Imports para a primeira parte
import urllib.request, json
#Imports para a segunda parte
import gspread
from oauth2client.service_account import ServiceAccountCredentials
#Imports para a terceira parte
from datetime import date

#Constantes
API_KEY = "cac53ba09ab8b03db6e63b399b9a465cf40a47c83cbd8d63ddf5e4d522c24c41"
URL = "https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms=USD,EUR"
#//API KEY in URL - just append ? or &api_key={your_api_key} the the end of your request url
#//API KEY in HEADER - add the following header to your request: authorization: Apikey {your_api_key}.

#Funcoes auxiliares
def countHistoricoWorksheetRecords():
  valuesFirstColumn = sheet.col_values(1)
  return len(valuesFirstColumn) + 1

#Primeira parte: vai buscar o valor atual das criptomoedas e guarda
#Inicializacao do dicionario que vai ter os valores das criptomoedas diarios
actualPrice = {
               "BTC":0,
               "ETH":0,
               "XRP":0,
               "BAT":0,
               "ZEC":0
}

listCryptos = list(actualPrice.keys())  #lista das criptomoedas que tenho

#contents = urllib.request.urlopen("https://jsonplaceholder.typicode.com/todos/1").read()

#vai percorrer a lista de criptomoedas e vai buscar o valor respetivo
for key in listCryptos:
    url = "https://min-api.cryptocompare.com/data/price?fsym="+key+"&tsyms=USD,EUR&api_key="+API_KEY
    request = urllib.request.urlopen(url).read()
    contentsDic = json.loads(request)
    actualPrice[key] = contentsDic["EUR"]

#Segunda parte (creditos ao Blog Twilio e a Anton Burnashev): abre o ficheiro onde vai ser guardada a informacao obtida antes
# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

sheet = client.open("Cripto").worksheet("Historico")


#Terceira parte: escreve o valor das criptomoedas no ficheiro
#worksheet.update_acell('B1', value) Or worksheet.update_cell(linha, coluna, value)
#Adiciona os dados na segunda linha, criando uma nova e nao sobrepondo valores
newRowData = [date.today().strftime("%d/%m/%Y"),actualPrice["BTC"],actualPrice["ETH"],actualPrice["XRP"],actualPrice["BAT"],actualPrice["ZEC"]]
indexNewRow = 2
sheet.insert_row(newRowData, indexNewRow)
#Adiciona os dados no final do separador
'''
numLine = countHistoricoWorksheetRecords()
#Escreve a data
sheet.update_cell(numLine, 1, date.today().strftime("%d/%m/%Y"))
#Valor da BTC
sheet.update_cell(numLine, 2, actualPrice["BTC"])
#Valor da ETH
sheet.update_cell(numLine, 3, actualPrice["ETH"])
#Valor da XRP
sheet.update_cell(numLine, 4, actualPrice["XRP"])
#Valor da BAT
sheet.update_cell(numLine, 5, actualPrice["BAT"])
#Valor da ZEC
sheet.update_cell(numLine, 6, actualPrice["ZEC"])
'''
#Feito por Miguel Peixoto
