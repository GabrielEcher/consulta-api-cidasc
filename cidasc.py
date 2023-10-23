import requests
import json  
import pandas as pd
from threading import Event




def call_api():
    api = input("Digite o link da API desejada: ")
    
    try:
        requisition = requests.get(api)
        requisition.raise_for_status() 
        jfile = requisition.json()
    
    except requests.exceptions.HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
        Event().wait(40)

    except requests.exceptions.RequestException as err:
        print(f'Error occurred: {err}')
        Event().wait(40)

    except requests.exceptions.JSONDecodeError() as error:
        raise(
            'Erro inesperado ao consultar API'
            'Consulte-a diretamente, verifique se as chaves primárias do arquivo JSON são respectivamente'
            '["UnidadeMedidas"] = https://sigensvc.cidasc.sc.gov.br/UnidadeMedida/Pesquisar'
            '["agrotoxicos"] = https://sigensvc.cidasc.sc.gov.br/Agrotoxico/Pesquisar?nrRegistroMapa='
            '["agrotoxicoMedida"] = https://sigensvc.cidasc.sc.gov.br/AgrotoxicoMedida/Pesquisar'
            'Ou verifique se o link da API foi alterado do padrão.'
            , error)

    for key in jfile:
        csvfile1 = json.dumps(jfile)
        csvfile2 = json.loads(csvfile1)

        print(csvfile2)
    
        df = pd.json_normalize(csvfile2[key])

    
    if key == "UnidadeMedidas":
        df.to_csv('C:/CIDASC/unidade_medidas.csv', encoding='utf-8', index=False)

    elif key == "agrotoxicos":
        df.to_csv('C:/CIDASC/cidasc_agrotoxicos.csv', encoding='utf-8', index=False)
        
    elif key == "agrotoxicoMedida":
        df.to_csv('C:/CIDASC/cidasc_agrotoxico_medida.csv', encoding='utf-8', index=False)


if __name__ == '__main__':
    call_api()