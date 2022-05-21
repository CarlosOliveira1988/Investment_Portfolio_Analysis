[![](https://img.shields.io/static/v1?label=python&message=3.9&color=blue&logo=python)](https://docs.python.org/3/whatsnew/3.9.html)
[![](https://img.shields.io/static/v1?label=linter&message=pylint&color=green&logo=pylint)](https://github.com/PyCQA/pylint)
[![](https://img.shields.io/static/v1?label=security&message=bandit&color=yellow&logo=bandit)](https://github.com/PyCQA/bandit)
[![](https://img.shields.io/static/v1?label=testing&message=pytest&color=green&logo=pytest)](https://docs.pytest.org/en/latest/)

# **Análise de Portfólio**

Este repositório é útil para realizar alguns tipos de análise de carteira, como:
- Comparações de posições abertas/fechadas com CDI/IPCA
- Dividend-yield de Renda Variável ajustado pelo preço médio de compra
- Taxas de Renda Fixa e Tesouro direto ajustadas por CDI/SELIC/IPCA acumalados nos últimos 12 meses
- Cálculos de retorno baseados em históricos mensais de CDI/SELIC/IPCA/FGTS/Poupança
- Etc

Uma das grandes vantagens de usar essa plataforma é que você pode ter carteiras em diferentes corretoras e visualizar todas as informações em único canal, sem necessidade de digitar inúmeras senhas.

Outra grande vantagem é você ter total controle sobre seus investimentos, ao longo de toda a sua história no mundo dos investimentos, a fim de conhecer os seus reais lucros/prejuízos, aportes, custos, etc.

O projeto foi construído para rodar em plataformas Windows, mas em breve poderá também funcionar em ambientes Linux.


# **Instalação**

1. Abrir a pasta do projeto no VSCode
1. Rodar o comando 'pip install -r requirements.txt'


# **Como usar**
## **Abrindo o template de dados**
O arquivo principal do projeto é o "main.py". Ao rodá-lo pela primeira vez, a tela a seguir será exibida:

![image](https://user-images.githubusercontent.com/70613924/169663075-d2b07fbe-6e97-475e-a9d5-f269873d5d65.png)

Na pasta "portfolio_lib" há disponível o arquivo "PORTFOLIO_TEMPLATE_PERFORMANCE.xlsx". Abra esse arquivo pelo menu "Arquivo -> Abrir Extrato". Na aba "Extrato" podemos visualizar todo o histórico de operações cadastradas no arquivo Excel.

![image](https://user-images.githubusercontent.com/70613924/169663208-84436554-aa33-4bbd-ace1-0520ea7687c1.png)


## **Explorando as abas de "Renda Variável", "Renda Fixa" e "Tesouro Direto"**

Nas abas "Renda Variável", "Renda Fixa" e "Tesouro Direto", estarão disponíveis informações como "Preço de Compra", "Cotação", "Dividend-Yield", etc.

As informações de tempo real das abas "Renda Variável" e "Tesouro Direto" são coletadas do site Status Invest e também da API YFinance.

Entretanto, as informações da aba "Renda Fixa" são apenas estimativas baseadas nas tabelas de CDI/SELIC/IPCA disponíveis na pasta "indexer_lib/data".

### **Renda Variável: Ações, FII, BDR, ETF**
![image](https://user-images.githubusercontent.com/70613924/169663264-e85ee3c8-e358-4390-96fb-16c5123a78f7.png)

### **Renda Fixa: PREFIXADO, CDI, IPCA**
![image](https://user-images.githubusercontent.com/70613924/169663457-1cf382d2-ba40-451e-96aa-2a5e2e07bda2.png)

### **Tesouro Direto: PREFIXADO, SELIC, IPCA**
![image](https://user-images.githubusercontent.com/70613924/169663465-6add51b3-3819-49ba-8001-8206a7103841.png)


## **Explorando as ferramentas**

### **Balanceamento de Carteira**
No menu "Ferramentas -> Balanceamento de Carteira", há disponível uma ferramenta para ajudar no balanceamento de carteira.

Basicamente, você irá definir metas de patrimônio para cada tipo de investimento e a ferramenta irá lhe sugerir movimentações com base em seu patrimônio e distribuição atuais.
![image](https://user-images.githubusercontent.com/70613924/169664005-4328f4e0-7502-4a52-a9e5-220a313e6d91.png)

### **Indicadores Econômicos**
No menu "Ferramentas -> Indicadores Econômicos", há disponível uma ferramenta de cálculo baseada nos índices CDI, IPCA, entre outros.

Essa ferramenta é bastante útil para realizar cálculos de custo de oportunidade ou ainda para definir "preço de venda" de bens duráveis, como lotes ou apartamentos, tendo em vista a perda do poder de compra pela inflação (IPCA).
![image](https://user-images.githubusercontent.com/70613924/169663702-6b8a8f52-657f-4c2f-8be4-5f62a89b8bef.png)


## **Preenchimento do arquivo de histórico Excel "Extrato"**
Na pasta "portfolio_lib" há disponível o arquivo "PORTFOLIO_TEMPLATE_EMPTY.xlsx". A partir dele você poderá iniciar os seus lançamentos, seguindo algumas poucas regras nas seguintes colunas obrigatórias:
- "Ticker": identificador principal do investimento
- "Mercado": classifica o tipo do ativo: "Ações", "FII", "BDR", "ETF", "Opções" ("Renda Variável"), "Renda Fixa" e "Tesouro Direto".
- "Operação": classifica o tipo de operação: "Compra", "Venda", "Transferência", "Resgate", "Provento", "Cobrança".
- "Notas": lembretes de objetivos ou motivações que o fizeram comprar ou vender um dado ativo
- Data, Quantidade, preços, taxas, proventos: colunas para controle de fluxo de caixa dos ativos

Para Renda Fixa e Tesouro Direto, temos algumas colunas adicionais:
- "Indexador": classifica os investimentos de Renda Fixa e Tesouro Direto: "PREFIXADO", "CDI", "SELIC", "IPCA".
- "Rentabilidade Contratada": a taxa contratada
- "Vencimento": data de vencimento do contrato
