# Web Scraper de Dados de Escolas

Este script Python utiliza **Selenium** para navegar e extrair informações de escolas do portal FDE (Fundação para o Desenvolvimento da Educação) de São Paulo e as exporta para um arquivo Excel (`.xlsx`) em tempo real.

---

## Funcionalidades

* Navegação automatizada pelo portal de pesquisa de escolas do FDE, iniciando a partir da página 1.
* Extração de dados detalhados para cada escola, incluindo:
    * Nome da Escola
    * Tipo de Ensino, Município, Diretoria de Ensino, Rede de Ensino
    * Endereço, Bairro, CEP, ZONA, Telefone, E-mail
* Registro do **número da página** do site de onde os dados foram coletados.
* Exportação dos dados coletados para um arquivo Excel (`dados_pagina.xlsx`), que é **atualizado progressivamente** após o processamento de cada página. Isso garante que os dados sejam salvos mesmo que o script seja interrompido, e otimiza o uso de memória.

---

## Pré-requisitos

Antes de executar o script, certifique-se de ter o Python 3 instalado. Você também precisará instalar as seguintes bibliotecas:

* `selenium`: Para automação de navegadores.
* `webdriver_manager`: Para gerenciar automaticamente o driver do Chrome.
* `openpyxl`: Para manipulação de arquivos Excel.
* `pandas`: Usado para gerar o timestamp no nome do arquivo de saída (embora não seja usado para o nome do arquivo final neste script, a biblioteca ainda é importada).

Você pode instalar todas elas usando pip:

```bash
pip install selenium webdriver-manager openpyxl pandas
```

Além disso, o script requer um navegador Chrome instalado em sua máquina, pois ele utiliza o `ChromeDriver` gerenciado pelo `webdriver_manager`.

---

## Como Executar

1.  **Salve o script**: Salve o código Python fornecido em um arquivo, por exemplo, `scraper_escolas.py`.
2.  **Execute o script**: Abra seu terminal ou prompt de comando, navegue até o diretório onde você salvou o arquivo e execute-o:

    ```bash
    python scraper_escolas.py
    ```

O script iniciará um navegador Chrome, navegará até o site do FDE e começará a extrair os dados. Você verá o progresso sendo impresso no console.

Um arquivo Excel chamado `dados_pagina.xlsx` será criado (ou atualizado, se já existir) no mesmo diretório do script. Este arquivo será **salvo e atualizado a cada página processada**, garantindo que os dados sejam persistidos incrementalmente.

---

## Observações

* O script está configurado para iniciar o navegador em modo **anônimo** (`--incognito`) e com o idioma em Português do Brasil (`--lang=pt-BR`).
* Ele utiliza esperas implícitas (`driver.implicitly_wait(10)`) para aguardar o carregamento dos elementos. Pequenas pausas (`sleep()`) foram adicionadas para dar tempo à página de carregar o conteúdo dinamicamente.
* O arquivo de saída Excel é `dados_pagina.xlsx` e é **salvo após o processamento de cada página**. Se o script for executado várias vezes, ele sobrescreverá o arquivo existente com o mesmo nome.
* Qualquer erro durante a extração de dados de uma escola específica ou na navegação entre as páginas será reportado no console. Em caso de erro ao passar de página, o script interromperá a raspagem.
* A extração dos dados das escolas é feita iterando por cada bloco de `article` e buscando elementos `h4` e `p` por índice dentro do contexto global, o que funciona bem para a estrutura atual do site.
