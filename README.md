# __Projeto Automação de Produtos__

Este projeto foi desenvolvido para automatizar um processo repetitivo e manual realizado na empresa onde trabalho. O objetivo principal é dar celeridade a uma etapa crítica do pipeline de dados, que anteriormente era feita manualmente no Excel, arquivo por arquivo, consumindo muito tempo.

O programa utiliza arquivos CSV extraídos do sistema ou ERP da empresa, além de um arquivo modelo chamado `modelo_de_busca.csv`, que contém os produtos que desejamos encontrar. A automação reúne todos os arquivos extraídos em um único arquivo, realiza a busca pelos produtos desejados e aplica uma série de transformações nos dados (pipeline ou ETL). No final, o programa gera automaticamente os arquivos processados, eliminando a necessidade de realizar essas tarefas manualmente no Excel.

## __Funcionalidades__
- Reunir todos os arquivos extraídos do sistema em um único arquivo.
- Buscar produtos específicos com base no arquivo `modelo_de_busca.csv`.
- Aplicar transformações nos dados, como exclusão de colunas, reorganização e filtros.
- Modificar e classificar os dados de acordo com regras específicas.
- Gerar arquivos processados automaticamente, com nomes personalizados baseados na data e hora.

---

## __Etapas do Processo__

### __1° Passo__: Leitura dos Arquivos
- Reunir todos os arquivos CSV extraídos do sistema em um único arquivo para facilitar o processamento.

### __2° Passo__: Busca por Produtos Específicos
- Utilizar o arquivo `modelo_de_busca.csv` para listar os produtos que desejamos buscar nos dados.

### __3° Passo__: Exclusão de Colunas Indesejadas
- Remover as seguintes colunas:
  - `FL_ABRANGENCIA`
  - `CD_REDE_ANS`
  - `NM_COMERCIAL`
  - `PRESTADOR`
  - `NM_LOCAL_ATENDIMENTO`
  - `SITUACAO_PRODUTO`
- Reorganizar as colunas:
  - Mover `NM_PRESTADOR` e `NM_FANTASIA` para a direita da coluna `CIDADE`.

### __4° Passo__: Modificação da Coluna `SERVICO`
- Substituir os códigos da coluna `SERVICO` por valores mais descritivos:
  - **Consulta**: `0`
  - **Exame**: `19-36`, `201-202`, `401-412`
  - **Terapias**: `25`, `60-63`, `500`
- Excluir todos os outros códigos que não se enquadram nas categorias acima.

### __5° Passo__: Filtros nas Colunas `TIPO_PESSOA` e `TIPO_PRESTADOR_SERVICO`
- Filtrar valores específicos:
  - `TIPO_PESSOA`: Excluir valores iguais a `1` (Corpo Clínico).
  - `TIPO_PRESTADOR_SERVICO`: Excluir linhas com valores iguais a `CORPO CLÍNILO`.

### __6° Passo__: Classificação dos Dados
- Classificar os dados pelas seguintes colunas:
  1. `UF`
  2. `CIDADE`
  3. `NM_LIVRO`
  4. `ESPECIALIDADE`

### __7° Passo__: Salvamento dos Arquivos
- Gerar arquivos processados automaticamente com nomes personalizados, incluindo:
  - Nome da rede
  - Produto
  - Data e hora do processamento

---
### __Benefícios da Automação__

- ✅ Redução significativa do tempo de processamento.
- ✅ Eliminação de tarefas manuais repetitivas.
- ✅ Maior precisão na análise dos dados.
- ✅ Facilidade na geração e organização dos relatórios.

---

## __Como Executar o Programa__

1. Certifique-se de ter o Python instalado em sua máquina.
3. Se preferir pode usar venv ou máquina virtual que está no projeto.
   - A medida em que digita, se você usar o tab no vscode ele completa pra você.
   - Estamos partindo do sistema operacional windows.
   - ```bash
      .\venv\Scripts\activate
   - Para desativar a máquina virtual.
   - ```bash
      deactivate
2. Instale as dependências listadas no arquivo `requirements.txt`:
   ```bash
   pip install -r requirements.txt