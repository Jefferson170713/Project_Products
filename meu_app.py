import sys
import warnings
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtWidgets import QProgressBar
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtGui import QIcon
from datetime import datetime
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
        self.path_ico_file = ''
        # 0.2 - título do app
        self.setWindowTitle("App Produtos")

        # 0.3 - Ícone do app
        self.path_ico_file = self.path_ico()
        self.setWindowIcon(QIcon(self.path_ico_file))
        # Dimensões da janela
        self.resize(600, 450)

        # 0.4 - Criação dos widgets
        self.label_file_selects = QLabel("Nenhum arquivo selecionado")
        self.button_selects = QPushButton("Selecionar Arquivos")
        self.button_selects.setFixedSize(120, 30)
        self.text_edit_file = QTextEdit()
        self.text_edit_file.setReadOnly(True)
        self.progress_bar_file = QProgressBar()
        self.progress_bar_file.setValue(0)

        self.label_file_search = QLabel("Nenhum arquivo selecionado")
        self.button_search = QPushButton("Buscar Produto")
        self.button_search.setFixedSize(120, 30)
        self.text_edit_search = QTextEdit()
        self.text_edit_search.setReadOnly(True)

        self.label_process = QLabel("Processamento")
        self.button_process = QPushButton("Processar e Salvar")
        self.button_process.setFixedSize(120, 30)
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
        layout_file_buttons = QHBoxLayout()  # Layout horizontal para centralizar os botões
        layout_file_buttons.addStretch(1)
        layout_file_buttons.addWidget(self.button_selects)
        layout_file_buttons.addStretch(1)
        layout_file.addLayout(layout_file_buttons)
        layout_file.addWidget(self.label_file_selects)
        layout_file.addWidget(self.text_edit_file)
        layout_file.addWidget(self.progress_bar_file)

        # 0.7 - layout_search
        layout_search = QVBoxLayout()
        layout_search_buttons = QHBoxLayout()  # Layout horizontal para centralizar os botões
        layout_search_buttons.addStretch(1)
        layout_search_buttons.addWidget(self.button_search)
        layout_search_buttons.addStretch(1)
        layout_search.addLayout(layout_search_buttons)
        layout_search.addWidget(self.label_file_search)
        layout_search.addWidget(self.text_edit_search)

        # 0.8 - layout_process
        layout_process = QVBoxLayout()
        layout_process_buttons = QHBoxLayout()  # Layout horizontal para centralizar os botões
        layout_process_buttons.addStretch(1)
        layout_process_buttons.addWidget(self.button_process)
        layout_process_buttons.addStretch(1)
        layout_process.addLayout(layout_process_buttons)
        layout_process.addWidget(self.label_process)
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
        folder = self.select_folder_to_save()
        self.search_for_products()
        self.columns_todelete()
        self.rearranging_columns()
        self.modify_column_service()
        self.filter_columns()
        self.sort_columns()
        self.delete_NU_CGC_CPF()
        self.save_file(folder)

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
        pattern = '|'.join(list_bady_clinique)
        if re.search(pattern, row, re.IGNORECASE):
            return 'SIM'
        return 'NÃO'
    
    # 5.0 - função para classificar colunas 6° Passo.
    def sort_columns(self):
        print(f'5.0° sort_columns: Etapa Iniciada, classificando as colunas.')
        sort_list = ['UF', 'CIDADE', 'NM_LIVRO', 'DS_ESPECIALIDADE']
        df_sort_columns = self.df_file.copy()
        df_sort_columns.sort_values(by=sort_list, inplace=True)
        df_sort_columns.reset_index(drop=True, inplace=True)
        self.df_file = df_sort_columns.copy()
        print(f'Etapa de classificação concluída. \n')
        print(self.df_file.head(2), '\n')

    # 5.1 função para exluir cpf e cnpj na tabela 6° Passo.
    def delete_NU_CGC_CPF(self):
        print(f'5.1° delete_NU_CGC_CPF: Etapa Iniciada, deletando NU_CGC_CPF.')
        df_delete_NU_CGC_CPF = self.df_file.copy()
        df_delete_NU_CGC_CPF['NU_CGC_CPF'] = df_delete_NU_CGC_CPF['NU_CGC_CPF'].astype(str)
        df_delete_NU_CGC_CPF['NU_CGC_CPF'] = df_delete_NU_CGC_CPF['NU_CGC_CPF'].str.replace('.0','', regex=False)
        print(f'Etapa de exclusão concluída. \n')
        print(f'Apagando as informações que constam em NU_CGC_CPF onde TIPO_PESSOA é 1.')
        df_delete_NU_CGC_CPF.loc[df_delete_NU_CGC_CPF['TIPO_PESSOA'] == 1, 'NU_CGC_CPF'] = ''
        print(f'Excluindo a coluna CD_PRESTADOR')
        df_delete_NU_CGC_CPF.drop(columns=['CD_PRESTADOR'], inplace=True)
        self.df_file = df_delete_NU_CGC_CPF.copy()
        print(f'Mostrando os valores únicos de NU_CGC_CPF tipo 1: {self.df_file[self.df_file.TIPO_PESSOA == 1]["NU_CGC_CPF"].unique()} \n')
        print(f'Mostrando os valores únicos de NU_CGC_CPF tipo 2: {self.df_file[self.df_file.TIPO_PESSOA == 2]["NU_CGC_CPF"].unique()} \n')
        print(self.df_file.head(2), '\n')

    # 6.0 - função para salvar o arquivo 7° Passo.
    def select_folder_to_save(self):
        options = QFileDialog.Options()
        folder = QFileDialog.getExistingDirectory(self, "Selecionar Pasta para Salvar", options=options)
        return folder
    
    # 6.1 - função para salvar o arquivo 7° Passo.
    def save_file(self, folder):
        print(f'6.1° save_file: Etapa Iniciada, salvando o arquivo. \n')
        date = datetime.now()
        date = date.strftime('%d_%m_%Y')
        print(f'Mostrando a date {date}')

        total_products = len(self.df_search)
        self.progress_bar_process.setMaximum(total_products)
        self.label_process.setText(f"Processamento de {total_products} produtos")
        
        for i, product in enumerate(self.df_search.values):
            df_product = self.df_file[self.df_file.NU_PRODUTO == product[0]].copy()
            df_product.reset_index(drop=True, inplace=True)
            rede = df_product.REDE_ATENDIMENTO.unique()[0]  # Corrigir o nome da coluna
            file_name = f'REDE {rede}_{product[0]}_{date}.csv'
            file_path = os.path.join(folder, file_name)
            df_product.to_csv(file_path, sep=';', encoding='latin1', index=False)
            print(f'{file_name} - {df_product.shape}')
            self.progress_bar_process.setValue(i + 1)
            self.text_edit_process.append(f'Arquivo salvo: {file_name}')
            self.label_process.setText(f"Processando {i + 1} de {total_products} produtos")
            
            # Forçar a atualização da interface do usuário
            QApplication.processEvents()
        
        print(f'Finalizado!!!')

    # 7.0 - função para pegar a logo da empresa
    def path_ico(self):
        print('7.0° path_ico: Etapa Iniciada, pegando a logo da empresa.')
        path = './ico/'
        path_ico = os.listdir(path)
        path_ico = [ico for ico in path_ico if ico.endswith('.ico')]
        path_ico = os.path.join(path, path_ico[0])
        print(path_ico)
        return path_ico

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())