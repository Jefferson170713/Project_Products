import sys
import warnings
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QFileDialog, QTextEdit, QProgressBar
from PyQt5.QtGui import QIcon
import pandas as pd
import os
import re

# Suprimir avisos de depreciação
warnings.filterwarnings("ignore", category=DeprecationWarning)

class MainWindow(QMainWindow):
    # 0.0 - função construtora principal
    def __init__(self):
        # 0.1 - função construtora da classe pai
        super().__init__()
        self.df_file = pd.DataFrame()
        self.df_search = pd.DataFrame()
        # 0.2 - título do app
        self.setWindowTitle("App Produtos")

        # 0.3 - Ícone do app
        self.setWindowIcon(QIcon('./ico/logo_Hapvida.ico'))
        # Dimensões da janela
        self.resize(600, 400)

        # 0.4 - Criação dos widgets
        self.label_file_selects = QLabel("Nenhum arquivo selecionado")
        self.button_selects = QPushButton("Selecionar Arquivos")
        self.text_edit_file = QTextEdit()
        self.text_edit_file.setReadOnly(True)
        self.progress_bar_file = QProgressBar()
        self.progress_bar_file.setValue(0)

        self.label_file_search = QLabel("Nenhum arquivo selecionado")
        self.button_search = QPushButton("Buscar Produto")
        self.text_edit_search = QTextEdit()
        self.text_edit_search.setReadOnly(True)

        self.button_process = QPushButton("Processar e Salvar")
        self.text_edit_process = QTextEdit()
        self.text_edit_process.setReadOnly(True)
        self.progress_bar_process = QProgressBar()
        self.progress_bar_process.setValue(0)

        # 0.5 - Conectar o botão a uma função
        self.button_selects.clicked.connect(self.select_files)
        self.button_search.clicked.connect(self.search_product)
        self.button_process.clicked.connect(self.process_and_save)

        # 0.6 - layout_file
        layout_file = QVBoxLayout()
        layout_file.addWidget(self.button_selects)
        layout_file.addWidget(self.label_file_selects)
        layout_file.addWidget(self.text_edit_file)
        layout_file.addWidget(self.progress_bar_file)

        # 0.7 - layout_search
        layout_search = QVBoxLayout()
        layout_search.addWidget(self.button_search)
        layout_search.addWidget(self.label_file_search)
        layout_search.addWidget(self.text_edit_search)

        # 0.8 - layout_process
        layout_process = QVBoxLayout()
        layout_process.addWidget(self.button_process)
        layout_process.addWidget(self.text_edit_process)
        layout_process.addWidget(self.progress_bar_process)

        # 0.9 - Layout principal
        main_layout = QVBoxLayout()
        main_layout.addLayout(layout_search)
        main_layout.addLayout(layout_file)
        main_layout.addLayout(layout_process)

        # 0.10 - Container central
        container = QWidget()
        container.setLayout(main_layout)

        self.setCentralWidget(container)
    
    # 1.1 - função para selecionar arquivos 1° Passo.
    def select_files(self):
        options = QFileDialog.Options()
        files, _ = QFileDialog.getOpenFileNames(self, "Selecionar Arquivos CSV", "", "CSV Files (*.csv);;All Files (*)", options=options)
        if files:
            self.label_file_selects.setText(f"{len(files)} arquivos selecionados")
            file_names = [os.path.basename(file) for file in files]
            self.text_edit_file.setText("\n".join(file_names))
            self.read_files(files)
    
    # 1.2 - função para ler arquivos 1° Passo.
    def read_files(self, files): 
        total_files = len(files)
        self.progress_bar_file.setMaximum(total_files)
        for num, file in enumerate(files):
            temp_df = pd.read_csv(file, sep=';', encoding='latin1', header=4)
            self.df_file = pd.concat([self.df_file, temp_df], ignore_index=True)
            self.df_file.drop_duplicates(inplace=True)
            self.progress_bar_file.setValue(num + 1)
        self.df_file.NU_PRODUTO = self.df_file.NU_PRODUTO.astype(str)
        print(f'1.2° read_files: Etapa Iniciada, lendo os arquivos.') 
        print(f'Quantidade de linhas e Colunas: {self.df_file.shape} \n') 
        print(self.df_file.head(2), '\n')  

    # 1.3 - função para buscar produto 1° Passo.
    def search_product(self):
        options = QFileDialog.Options()
        files, _ = QFileDialog.getOpenFileNames(self, "Selecionar Arquivos CSV", "", "CSV Files (*.csv);;All Files (*)", options=options)
        if files:
            self.read_search_files(files)
            num_products = self.df_search['NU_PRODUTO'].nunique()
            self.label_file_search.setText(f"{num_products} produtos encontrados")
            self.text_edit_search.setText("\n".join(self.df_search['NU_PRODUTO'].astype(str).tolist()))

    # 1.4 - função para ler arquivos de busca 1° Passo.
    def read_search_files(self, files):
        for file in files:
            temp_df = pd.read_csv(file, sep=';', encoding='latin1')
            self.df_search = pd.concat([self.df_search, temp_df], ignore_index=True)

        self.df_search.NU_PRODUTO = self.df_search.NU_PRODUTO.astype(str)
        self.df_search.drop_duplicates(inplace=True)
        print(f'1.4° read_search_files: Etapa Iniciada, lendo os arquivos de busca.') 
        print(f'Quantidade de linhas e Colunas: {self.df_search.shape} \n')
        print(self.df_search.head(2), '\n')  

    # 2.0 - função para processar e salvar (vazia por enquanto)
    def process_and_save(self):
        print(f'2.0° process_and_save: Etapa Iniciada, processando e salvando os arquivos.')
        self.search_for_products()
        self.columns_todelete()
        self.rearranging_columns()
        self.modify_column_service()
        #self.save_file()

    # 2.1 - função para filtrar produtos 2° Passo.
    def search_for_products(self):
        print(f'2.1° search_for_products: Etapa Iniciada, filtrando os produtos.')
        print(f'Quantidade de linhas e colunas do df_file: {self.df_file.shape}')
        df_filtered = self.df_file[self.df_file.NU_PRODUTO.isin(self.df_search.NU_PRODUTO)].copy()
        df_filtered.reset_index(drop=True, inplace=True)
        print(f'Quantidade de linhas e colunas do df_filtered: {df_filtered.shape}') 
        self.df_file = df_filtered.copy()
        print(f'Quantidade de linhas e colunas do df_file agora filtrado: {self.df_file.shape}\n')
        print(self.df_file.head(2), '\n')
        

    # 2.2 - função deletar colunas 3° Passo.
    def columns_todelete(self):
        print(f'2.2° columns_todelete: Etapa Iniciada, deletando colunas.')
        colums_to_delete = ['FL_ABRANGENCIA', 'CD_REDE_ANS', 'NM_COMERCIAL', 'PRESTADOR', 'NM_LOCAL_ATENDIMENTO', 'SITUACAO_PRODUTO']
        self.df_file.drop(columns=colums_to_delete, inplace=True)
        print(f'Quantidade de linhas e colunas do df_file agora deletado: {self.df_file.shape}\n')
        print(self.df_file.head(2), '\n')

    # 2.3 - função para reorganizar as colunas 3° Passo.
    def rearranging_columns(self):
        print(f'2.3° rearranging_columns: Etapa Iniciada, reorganizando as colunas.')

        rearranging_columns = ['CONTRATACAO', 'NU_PRODUTO', 'NM_PRODUTO', 'REDE_ATENDIMENTO',
            'DS_REDE_ATENDIMENTO', 'UF', 'CIDADE', 'NM_PRESTADOR', 'NM_FANTASIA','TIPO_ESTABELECIMENTO',
            'SERVICO', 'DS_ESPECIALIDADE', 'CD_PRESTADOR','NU_CGC_CPF', 'NU_CNES_CRM',
            'ENDERECO','COMPLEMENTO', 'NM_BAIRRO', 'CD_CEP', 'DS_FONE', 'SITE', 'NM_LIVRO',
            'TIPO_PESSOA', 'IBGE', 'TIPO_PRESTADOR_SERVICO']
        
        df_rearranging_columns = self.df_file[rearranging_columns].copy()
        self.df_file = df_rearranging_columns.copy()
        print(f'Quantidade de linhas e colunas do df_file agora reorganizado: {self.df_file.shape}\n')
        print(self.df_file.head(2), '\n')
        
    # 3.0 - função para modificar a coluna serviço 4° Passo.
    def modify_column_service(self):
        print(f'3.0° modify_column_service: Etapa Iniciada, modificando a coluna serviço.')
        dict_map ={
            'CONSULTA': [0],
            'EXAME': [19, 20, 21, 22, 23, 24, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 201, 202, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412],
            'TERAPIAS': [25, 60, 61, 62, 63, 500],
        }

        df_modified = self.df_file.copy()

        df_modified.SERVICO = df_modified.SERVICO.apply(lambda line: self.map_services(line, dict_map))

        df_services = df_modified[df_modified.SERVICO != 'OUTROS'].copy()
        df_services.reset_index(drop=True, inplace=True)

        self.df_file = df_services.copy()
        print(f'Quantidade de linhas e colunas do df_file agora modificado: {self.df_file.shape}\n')
        print(self.df_file.SERVICO.unique(), '\n')
        print(self.df_file.head(2), '\n')

    # 3.1 função para mapear os serviços 4° Passo.
    def map_services(self, row, dict_map):
       #quando os valores que estão no dicionário forem iguais ao valor da coluna, então retorna a chave
        for key, value in dict_map.items():
            if row in value:
                return key
        return 'OUTROS'

    # 4.0 - função para filtrar as colunas TIPO_PESSOA eTIPO_PRESTADOR_SERVICO 5° Passo.
    def filter_columns(self):
        print(f'4.0° filter_columns: Etapa Iniciada, filtrando as colunas TIPO_PESSOA e TIPO_PRESTADOR_SERVICO.')
        list_bady_clinique = [
        'CORPO CLINICLO', 'CORPO CLÍNICO', 'CORPO_CLINICO', 'CORPO_CLÍNICO',
        'Corpo Clinico', 'Corpo Clínico', 'Corpo_Clinico', 'Corpo_Clínico',
        'corpo clinico', 'corpo clínico', 'corpo_clinico', 'corpo_clínico',
        ]
        df_filtered = self.df_file.copy()
        df_filtered['STATUS_CLINIQUE'] = df_filtered.apply(lambda row: self.check_bad_clinique(row['NM_PRESTADOR'], list_bady_clinique), axis=1)
        print(df_filtered.STATUS_CLINIQUE.value_counts(), '\n')
        df_filtered_status = df_filtered[df_filtered.STATUS_CLINIQUE == 'NÃO'].copy()
        print(f'Quantidade de linhas e colunas do df_filtered_status agora filtrado: {df_filtered_status.shape}\n')
        print(f'Processo de reorganização das colunas.')

        list_status_clinique = ['CONTRATACAO', 'NU_PRODUTO', 'NM_PRODUTO', 'REDE_ATENDIMENTO',
                    'DS_REDE_ATENDIMENTO', 'UF', 'CIDADE', 'NM_PRESTADOR', 'NM_FANTASIA',
                    'TIPO_ESTABELECIMENTO', 'SERVICO', 'DS_ESPECIALIDADE', 'CD_PRESTADOR',
                    'NU_CGC_CPF', 'NU_CNES_CRM', 'ENDERECO', 'COMPLEMENTO', 'NM_BAIRRO',
                    'CD_CEP', 'DS_FONE', 'SITE', 'NM_LIVRO', 'TIPO_PESSOA', 'IBGE',
                    'TIPO_PRESTADOR_SERVICO']
        self.df_file = df_filtered_status[list_status_clinique].copy()
        print(f'Quantidade de linhas e colunas do df_file agora filtrado: {self.df_file.shape}\n')
        print(self.df_file.head(2), '\n')
    
    # 4.1 - função para checar nome específico e deletar 5° Passo.
    def check_bad_clinique(self, row, list_bady_clinique):
        for bad_clinique in list_bady_clinique:
            if bad_clinique in row:
                return 'SIM'
        return 'NÃO'
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())