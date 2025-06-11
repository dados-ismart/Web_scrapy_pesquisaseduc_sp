from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from time import sleep
from openpyxl import Workbook 
import pandas as pd 

def iniciar_driver():
    chrome_options = Options()
    arguments = ['--lang=pt-BR', '--window-size=1300,1000', '--incognito']
    for argument in arguments:
        chrome_options.add_argument(argument)

    chrome_options.add_experimental_option('prefs', {
        'download.prompt_for_download': False,
        'profile.default_content_setting_values.notifications': 2,
        'profile.default_content_setting_values.automatic_downloads': 1,

    })
    driver = webdriver.Chrome(service=ChromeService(
        ChromeDriverManager().install()), options=chrome_options)

    return driver


driver = iniciar_driver()
driver.implicitly_wait(10)
driver.get('https://pesquisaseduc.fde.sp.gov.br/localize_diretoria_jurisdicao?idJurisdicao=100&idDiretoria=10205&pageNumber=1')

# --- Configuração do Arquivo Excel (OpenPyXL) ---
wb = Workbook()
headers = ['Nome da Escola',
            'Tipo de ensino',
            'Município',
            'Diretoria de Ensino',
            'Rede de Ensino',
            'Endereço',
            'Bairro',
            'CEP',
            'ZONA',
            'Telefone',
            'E-mail',
            'Pagina_do_site']
sheet = wb['Sheet']
sheet.append(headers)
wb.save('dados_pagina.xlsx')

# --- Começar Scrapy---
page_number = 1
while True:
    print(f"--- Raspando página {page_number} ---")
    try:
        a = driver.find_elements(By.XPATH, '//a')
        driver.execute_script("window.scrollTo(0, 700);")
        blocos = driver.find_elements(By.XPATH, '//article[@class="col-md-12 custom-col-md-12"]')
    except Exception as e:
        print(f"Erro ao ler pagina inicial: {e}")
    for i in range(1, len(blocos)+1):
        try:
            nome_escola = driver.find_element(By.XPATH, f'//article[@class="col-md-12 custom-col-md-12"][{i}]/h4').text
            tipo_ensino = driver.find_element(By.XPATH, f'//article[@class="col-md-12 custom-col-md-12"][{i}]/p[1]').text
            infos_escola = driver.find_element(By.XPATH, f'//article[@class="col-md-12 custom-col-md-12"][{i}]/p[2]').text
            
            #TRATAMENTO NOME_ESCOLA
            nome_escola = nome_escola[15:].strip()
            print(f'{i}:\n Escola: {nome_escola}')

            #TRATAMENTO TIPO DE ENSINO
            partes = tipo_ensino.split(' | ')

            dados = {}
            for parte in partes:
                if ':' in parte:
                    chave, valor = parte.split(':', 1)
                    dados[chave.strip()] = valor.strip()

            print(f"\n\nTipo de ensino: {dados.get('Tipo de ensino')}")
            print(f"Município: {dados.get('Município')}")
            print(f"Diretoria de Ensino: {dados.get('Diretoria de Ensino')}")
            print(f"Rede de Ensino: {dados.get('Rede de Ensino')}")

            #TRATAMENTO INFORMACOES DA ESCOLA
            linhas = infos_escola.strip().split('\n')

            dados_contato = {}
            for linha in linhas:
                if ':' in linha:
                    chave, valor = linha.split(':', 1)
                    dados_contato[chave.strip()] = valor.strip()

            print(f"\nEndereço: {dados_contato.get('Endereço')}")
            print(f"Bairro: {dados_contato.get('Bairro')}")
            print(f"CEP: {dados_contato.get('CEP')}")
            print(f"ZONA: {dados_contato.get('ZONA')}")
            print(f"Telefone: {dados_contato.get('Telefone')}")
            print(f"E-mail: {dados_contato.get('E-mail')}")

            lista_sheets = [nome_escola, 
                        dados.get('Tipo de ensino'),
                        dados.get('Município'),
                        dados.get('Diretoria de Ensino'),
                        dados.get('Rede de Ensino'),
                        dados_contato.get('Endereço'),
                        dados_contato.get('Bairro'),
                        dados_contato.get('CEP'),
                        dados_contato.get('ZONA'),
                        dados_contato.get('Telefone'),
                        dados_contato.get('E-mail'),
                        page_number
                        ]
            sheet.append(lista_sheets)

        except Exception as e:
            print(f"Erro ao encontrar ou processar o elemento de informações: {e}")
    wb.save('dados_pagina.xlsx')
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        botao_proxima_pagina = driver.find_elements(By.XPATH, '//a[@class="page-link" and @rel="next"]')
        botao_proxima_pagina[1].click()
        page_number+=1
    except Exception as e:
        print(f"Erro ao passar de página: {e}")
        break

