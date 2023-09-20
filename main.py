import PySimpleGUI as sg
import hashlib, datetime, os, time

user = []
access = False
theme = 'DarkAmber'
key_num = 5
transactions_list = []
decrypted = {}

def verify_login(next_window, warn=None, current_profile=False):
    # next_window = Próxima página a ser exibida
    # warn = None: Sem alertas
    #       'Login Inválido': Tentativa de login incorreta
    # current_profile = True: Existe um usuário logado
    #                   False: Sem usuários logados

    global access, user
    sg.theme(theme)

    if warn is None:
        # Tela de login padrão
        layout = [
            [sg.Text('Usuário'), sg.Input(key='user_name')],
            [sg.Text('Senha'), sg.Input(key='user_password', password_char='•')],
            [sg.Button('Prosseguir', key='proceed'), sg.Button('Cancelar', key='cancel', button_color=(None, 'red'))]
        ]
    else:
        # Tentou fazer login com credenciais incorretas
        layout = [
            [sg.Text(warn, text_color='red')],
            [sg.Text('Usuário'), sg.Input(key='user_name')],
            [sg.Text('Senha'), sg.Input(key='user_password', password_char='•')],
            [sg.Button('Prosseguir', key='proceed'), sg.Button('Cancelar', key='cancel', button_color=(None, 'red'))]
        ]

    # Publicação de janela com nome 'Verificação' com um dos dois layouts definidos acima
    window = sg.Window('Verificação', layout)

    while True:
        button, values = window.Read()

        if button is None or button == 'cancel':
            window.close()

            if next_window == 'menu':
                # Fechar aplicativo se clicou em cancelar e não houver login
                quit()

            else:
                menu()


        elif button == 'proceed':
            # Tentativa de login
            hashed_password = hashlib.sha256(str(values['user_password']).encode('ascii')).hexdigest()
            # Os logins são armazenados no arquivo i/l.txt com o nome de usuário exposto, mas a senha criptografada em sha265

            if current_profile is False:
                # Se ainda não houver um login estabelecido
                file = open('./i/l.txt', 'r', encoding='utf-8')
                lines = file.readlines()
                file.close()

                for line in lines:
                    # Confere em toda a lista de usuários se existe um nome de usuário e hask correspondentes
                    if f'{values["user_name"]} {hashed_password}\n' == line:
                        access = True
                        user = [values['user_name'], hashed_password]


            else:
                # Se já houver um login em vigor (quer trocar a senha ou criar novo usuário)
                if f'{values["user_name"]} {hashed_password}' == f'{user[0]} {user[1]}':
                    # Confere se os dados fornecidos são iguais ao do login atual
                    access = True


        if access is True:
            access = False
            if next_window == 'menu':
                window.close()
                menu()


            elif next_window == 'new_profile':
                window.close()
                new_profile()


            elif next_window == 'edit_profile':
                window.close()
                edit_profile()


        else:
            window.close()
            # Retorna para o início da função com o valor 'warn' definido
            verify_login(next_window, 'Login Inválido', current_profile)

def menu():
    global theme, user, transactions_list
    sg.theme(theme)

    for file in os.listdir('./i/t')[::-1]:
        # i/t corresponde ao diretório de transações (todos criptografados)
        decrypt_file(file, True)

    layout = [
        [sg.TabGroup(layout=[
            [sg.Tab('Registar Transação', layout=[
                [sg.TabGroup(layout=[
                    [sg.Tab('Troca', layout=[
                        [sg.Frame('Registrar Troca', layout=[
                            [sg.TabGroup(layout=[
                                [sg.Tab('Veículo 1', layout=[
                                    [sg.Text('Marca'), sg.Input(key='E1_brand', tooltip='Marca do veículo 1')],
                                    [sg.Text('Modelo'), sg.Input(key='E1_model', tooltip='Modelo do veículo 1')],
                                    [sg.Text('Ano'), sg.Input(key='E1_year', tooltip='Ano do veículo 1')],
                                    [sg.Text('Cor'), sg.Input(key='E1_color', tooltip='Cor do veículo 1')],
                                    [sg.Text('Completo'), sg.OptionMenu(('Sim', 'Não'), key='E1_complete')],
                                    [sg.Text('Avarias'), sg.Multiline(key='E1_damage',
                                                                      tooltip='Avarias do veículo 1 (Se tiver)')],
                                    [sg.Text('Portas'), sg.Spin(('0', '1', '2', '3', '4', '5', '6'), key='E1_door',
                                                                tooltip='Número de portas do veículo 1 (0 se for uma '
                                                                        'moto por exemplo)',
                                                                size=(2, 1))],
                                    [sg.Text('Gastos'), sg.Multiline(key='E1_outgoing',
                                                                     tooltip='Gastos com o veículo 1')],
                                    [sg.Text('Preço de tabela'), sg.Input(key='E1_tabel',
                                                                          tooltip='Preço de tabela do veículo 1')],
                                    [sg.Text('Preço combinado'), sg.Input(key='E1_price',
                                                                          tooltip='Preço combinado do veículo 1')]
                                ])],
                                [sg.Tab('Veículo 2', layout=[
                                    [sg.Text('Marca'), sg.Input(key='E2_brand', tooltip='Marca do veículo 2')],
                                    [sg.Text('Modelo'), sg.Input(key='E2_model', tooltip='Modelo do veículo 2')],
                                    [sg.Text('Ano'), sg.Input(key='E2_year', tooltip='Ano do veículo 2')],
                                    [sg.Text('Cor'), sg.Input(key='E2_color', tooltip='Cor do veículo 2')],
                                    [sg.Text('Completo'), sg.OptionMenu(('Sim', 'Não'), key='E2_complete')],
                                    [sg.Text('Avarias'), sg.Multiline(key='E2_damage',
                                                                      tooltip='Avarias do veículo 2 (Se tiver)')],
                                    [sg.Text('Portas'), sg.Spin(('0', '1', '2', '3', '4', '5', '6'), key='E2_door',
                                                                tooltip='Número de portas do veículo 2 (0 se for uma '
                                                                        'moto por exemplo)',
                                                                size=(2, 1))],
                                    [sg.Text('Gastos'), sg.Multiline(key='E2_outgoing',
                                                                     tooltip='Gastos com o veículo 2')],
                                    [sg.Text('Preço de tabela'), sg.Input(key='E2_tabel',
                                                                          tooltip='Preço de tabela do veículo 2')],
                                    [sg.Text('Preço combinado'), sg.Input(key='E2_price',
                                                                          tooltip='Preço combinado do veículo 2')]
                                ])],
                                [sg.Tab('Conclusão', key='E_conclusion', layout=[
                                    [sg.Text('Compensação'),
                                     sg.OptionMenu(('Nada', 'Recebi', 'Paguei'),
                                                   key='E_compensation'),
                                     sg.Input(key='E_much_compensation', size=(10, 1))],
                                    [sg.Text('Observações'),
                                     sg.Multiline(key='E_observations', tooltip='Opcional')],
                                    [sg.Button('Registar Troca', key='E_confirm')],
                                    [sg.Text('', text_color='green', size=(30, 2), key='E_notification')]
                                ])]
                            ])]
                        ])]
                    ])],
                    [sg.Tab('Venda', layout=[
                        [sg.Frame('Registrar Venda', layout=[
                            [sg.TabGroup(layout=[
                                [sg.Tab('Veículo', key='S_vehicle', layout=[
                                    [sg.Text('Marca'), sg.Input(key='S_brand', tooltip='Marca do veículo')],
                                    [sg.Text('Modelo'), sg.Input(key='S_model', tooltip='Modelo do veículo')],
                                    [sg.Text('Ano'), sg.Input(key='S_year', tooltip='Ano do veículo')],
                                    [sg.Text('Cor'), sg.Input(key='S_color', tooltip='Cor do veículo')],
                                    [sg.Text('Completo'), sg.OptionMenu(('Sim', 'Não'), key='S_complete')],
                                    [sg.Text('Avarias'), sg.Multiline(key='S_damage',
                                                                      tooltip='Avarias do veículo (Se tiver)')],
                                    [sg.Text('Portas'), sg.Spin(('0', '1', '2', '3', '4', '5', '6'), key='S_door',
                                                                tooltip='Número de portas do veículo(0 se for uma '
                                                                        'moto por exemplo)',
                                                                size=(2, 1))],
                                    [sg.Text('Gastos'), sg.Multiline(key='S_outgoing',
                                                                     tooltip='Gastos com o veículo')],
                                    [sg.Text('Preço de tabela'), sg.Input(key='S_tabel',
                                                                          tooltip='Preço de tabela do veículo')],
                                    [sg.Text('Preço combinado'), sg.Input(key='S_price',
                                                                          tooltip='Preço combinado do veículo')]
                                ])],
                                [sg.Tab('Conclusão', key='S_conclusion', layout=[
                                    [sg.Text('Observações'),
                                     sg.Multiline(key='S_observations', tooltip='Opcional')],
                                    [sg.Button('Registar Troca', key='S_confirm')],
                                    [sg.Text('', text_color='green', size=(30, 2), key='S_notification')]
                                ])]
                            ])]
                        ])]
                    ])],
                    [sg.Tab('Compra', layout=[
                        [sg.Frame('Registar Compra', layout=[
                            [sg.TabGroup(layout=[
                                [sg.Tab('Veículo', key='P_vehicle', layout=[
                                    [sg.Text('Marca'), sg.Input(key='P_brand', tooltip='Marca do veículo')],
                                    [sg.Text('Modelo'), sg.Input(key='P_model', tooltip='Modelo do veículo')],
                                    [sg.Text('Ano'), sg.Input(key='P_year', tooltip='Ano do veículo')],
                                    [sg.Text('Cor'), sg.Input(key='P_color', tooltip='Cor do veículo')],
                                    [sg.Text('Completo'), sg.OptionMenu(('Sim', 'Não'), key='P_complete')],
                                    [sg.Text('Avarias'), sg.Multiline(key='P_damage',
                                                                      tooltip='Avarias do veículo (Se tiver)')],
                                    [sg.Text('Portas'), sg.Spin(('0', '1', '2', '3', '4', '5', '6'), key='P_door',
                                                                tooltip='Número de portas do veículo(0 se for uma '
                                                                        'moto por exemplo)',
                                                                size=(2, 1))],
                                    [sg.Text('Gastos'), sg.Multiline(key='P_outgoing',
                                                                     tooltip='Gastos com o veículo')],
                                    [sg.Text('Preço de tabela'), sg.Input(key='P_tabel',
                                                                          tooltip='Preço de tabela do veículo')],
                                    [sg.Text('Preço combinado'), sg.Input(key='P_price',
                                                                          tooltip='Preço combinado do veículo')]
                                ])],
                                [sg.Tab('Conclusão', key='P_conclusion', layout=[
                                    [sg.Text('Observações'),
                                     sg.Multiline(key='P_observations', tooltip='Opcional')],
                                    [sg.Button('Registar Compra', key='P_confirm')],
                                    [sg.Text('', text_color='green', size=(30, 2), key='P_notification')]
                                ])]
                            ])]
                        ])]
                    ])]
                ])]
            ])],
            [sg.Tab('Transações', layout=[
                [sg.Column(layout=transactions_list, scrollable=True, size=(465, 450), vertical_scroll_only=True)]
            ])],
            [sg.Tab('Configurações', layout=[
                [sg.Text(f'{datetime.date.today().day}/'
                         f'{datetime.date.today().month}/'
                         f'{datetime.date.today().year}',
                         relief=sg.RELIEF_RIDGE,
                         background_color='blue'),
                 sg.Text(user[0])],
                [sg.Button('Mudar Tema', key='change_theme'),
                 sg.Combo(sg.theme_list(),
                          default_value=str(theme),
                          key='new_theme')],
                [sg.Button('Novo Login', key='new_profile')],
                [sg.Button('Editar Perfil', key='edit_profile')],
                [sg.Button('Sair', key='quit')]
            ])]
        ])]
    ]
    
    window = sg.Window('Menu', layout, use_default_focus=False, resizable=True)

    while True:
        button, values = window.Read()

        if button is None:
            quit()

        elif button == 'change_theme':
            theme = values['new_theme']
            transactions_list = []
            window.close()
            menu()


        elif button == 'new_profile':
            transactions_list = []
            window.close()
            verify_login('new_profile', 'Insira o Login atual', True)


        elif button == 'edit_profile':
            transactions_list = []
            window.close()
            verify_login('edit_profile', 'Insira o Login atual', True)


        elif button == 'quit':
            # Zera o login e volta para a página inicial
            user = []
            transactions_list = []
            window.close()
            verify_login('menu')


        elif button == 'S_confirm':
            # Registra a venda
            encrypt({'Detalhes': f'Registro de Venda feito por {user[0]} em {datetime.date.today().day}/'
                                 f'{datetime.date.today().month}/'
                                 f'{datetime.date.today().year}\n\n',
                     'Marca': values['S_brand'],
                     'Modelo': values['S_model'],
                     'Ano': values['S_year'],
                     'Cor': values['S_color'],
                     'Completo': values['S_complete'],
                     'Portas': values['S_door'],
                     'Avarias': values['S_damage'],
                     'Gastos': values['S_outgoing'],
                     'Preço de tabela': values['S_tabel'],
                     'Preço combinado': values['S_price'],
                     'Observações': values['S_observations']}, True)
            window['S_notification'].update('Transação salva com sucesso!')
            window.refresh()
            time.sleep(2)
            transactions_list = []
            window.close()
            menu()
        elif button == 'P_confirm':
            # Registra a compra
            encrypt({'Detalhes': f'Registro de Compra feito por {user[0]} em {datetime.date.today().day}/'
                                 f'{datetime.date.today().month}/'
                                 f'{datetime.date.today().year}\n\n',
                     'Marca': values['P_brand'],
                     'Modelo': values['P_model'],
                     'Ano': values['P_year'],
                     'Cor': values['P_color'],
                     'Completo': values['P_complete'],
                     'Portas': values['P_door'],
                     'Avarias': values['P_damage'],
                     'Gastos': values['P_outgoing'],
                     'Preço de tabela': values['P_tabel'],
                     'Preço combinado': values['P_price'],
                     'Observações': values['P_observations']}, True)
            window['P_notification'].update('Transação salva com sucesso!')
            window.refresh()
            time.sleep(2)
            transactions_list = []
            window.close()
            menu()
        elif button == 'E_confirm':
            # Registra a troca
            encrypt({'Detalhes': f'Registro de Troca feito por {user[0]} em {datetime.date.today().day}/'
                                 f'{datetime.date.today().month}/'
                                 f'{datetime.date.today().year}\n\n',
                     'Marca Veículo 1': values['E1_brand'],
                     'Modelo Veículo 1': values['E1_model'],
                     'Ano Veículo 1': values['E1_year'],
                     'Cor Veículo 1': values['E1_color'],
                     'Completo Veículo 1': values['E1_complete'],
                     'Portas Veículo 1': values['E1_door'],
                     'Avarias Veículo 1': values['E1_damage'],
                     'Gastos Veículo 1': values['E1_outgoing'],
                     'Preço de tabela Veículo 1': values['E1_tabel'],
                     'Preço combinado Veículo 1': f'{values["E1_price"]}\n\n',
                     'Marca Veículo 2': values['E2_brand'],
                     'Modelo Veículo 2': values['E2_model'],
                     'Ano Veículo 2': values['E2_year'],
                     'Cor Veículo 2': values['E2_color'],
                     'Completo Veículo 2': values['E2_complete'],
                     'Portas Veículo 2': values['E2_door'],
                     'Avarias Veículo 2': values['E2_damage'],
                     'Gastos Veículo 2': values['E2_outgoing'],
                     'Preço de tabela Veículo 2': values['E2_tabel'],
                     'Preço combinado Veículo 2': f'{values["E2_price"]}\n\n',
                     'Compensação': f'{values["E_compensation"]} {values["E_much_compensation"]}',
                     'Observações': values['E_observations']}, True)
            window['E_notification'].update('Transação salva com sucesso!')
            window.refresh()
            time.sleep(2)
            transactions_list = []
            window.close()
            menu()

        else:
            show_transaction(button)

def new_profile():
    # Novo login 
    # Os perfis ficam guardados e criptografados em i/l.txt
    global access
    access = True
    sg.theme(theme)
    layout = [
        [sg.Text('Criando novo perfil', text_color='green', key='warn', size=(40, 1))],
        [sg.Text('Nome'), sg.Input(key='user_name')],
        [sg.Text('Senha'), sg.Input(key='user_password')],
        [sg.Text('Ao criar um novo perfil, você terá que fazer login novamente', text_color='red')],
        [sg.Button('Criar', key='create'), sg.Button('Cancelar', key='cancel', button_color=(None, 'red'))]
    ]
    window = sg.Window('Verificação', layout)

    while True:
        access = True
        button, values = window.Read()

        if button is None or button == 'cancel':
            window.close()
            menu()

        elif button == 'create':
            file = open('./i/l.txt', 'r', encoding='utf-8')
            lines = file.readlines()
            file.close()

            for value in values:
                if values[value] == '':
                    # Não permitir guardar informações vazias
                    window['warn'].update('Preencha todos os campos')
                    window.refresh()
                    access = False

                if ' ' in values[value]:
                    window['warn'].update('Não coloque espaços no nome ou na senha', text_color='red')
                    window.refresh()
                    access = False

            for line in lines:
                if values['user_name'] == line.split()[0]:
                    window['warn'].update('Este nome de usuário já existe', text_color='red')
                    window.refresh()
                    access = False

            if access is True:
                try:
                    hashed_password = hashlib.sha256(str(values['user_password']).encode('ascii')).hexdigest()
                    lines.append(f'{values["user_name"]} {hashed_password}\n')
                    file = open('./i/l.txt', 'w', encoding='utf-8')
                    file.writelines(lines)
                    file.close()
                    window.close()
                    verify_login('menu', 'Você criou um novo perfil, faça login novamente para continuar')
                    break

                except UnicodeEncodeError:
                    # Algumas senhas retornam erro durante a criptografação
                    window['warn'].update('A senha digitada não pode ser salva, tente outra senha', text_color='red')
                    window.refresh()

def edit_profile():
    global user, access
    access = True
    layout = [
        [sg.Text('Editar Perfil', key='warn', size=(40, 1), text_color='green')],
        [sg.Text('Nome'), sg.Input(user[0], key='user_name')],
        [sg.Text('Senha'), sg.Input(password_char='•', key='user_password', tooltip='Nem todos os '
                                                                                    'caracteres '
                                                                                    'especiais são '
                                                                                    'aceitos')],
        [sg.Button('Salvar', key='save_profile'),
         sg.Button('Cancelar', key='cancel', button_color=(None, 'red')),
         sg.Button('Excluir Perfil', key='exclude_profile', button_color=(None, 'red'))]
    ]
    window = sg.Window('Editar Perfil', layout)


    while True:
        access = True
        button, values = window.Read()

        if button is None or button == 'cancel':
            window.close()
            menu()

        elif button == 'save_profile':
            file = open('./i/l.txt', 'r', encoding='utf-8')
            lines = file.readlines()
            file.close()
            for line in lines:
                # Verifica se já existe um usuário com aquele nome
                if values['user_name'] != user[0]:
                    if values['user_name'] == line.split()[0]:
                        window['warn'].update('Este nome de usuário já existe!', text_color='red')
                        window.refresh()
                        access = False


            for value in values:
                if values[value] == '':
                    window['warn'].update('Preencha todos os campos!', text_color='red')
                    window.refresh()
                    access = False
                if ' ' in values[value]:
                    window['warn'].update('Não coloque espaços no nome de usuário, ou senha', text_color='red')
                    window.refresh()
                    access = False


            if access is True:
                try:
                    hashed_password = hashlib.sha256(str(values['user_password']).encode('ascii')).hexdigest()
                    lines[lines.index(f'{user[0]} {user[1]}\n')] = f'{values["user_name"]} {hashed_password}\n'
                    file = open('./i/l.txt', 'w', encoding='utf-8')
                    file.writelines(lines)
                    file.close()
                    window['warn'].update('Perfil editado com sucesso!', text_color='green')
                    window.refresh()
                    time.sleep(2)
                    window.close()
                    user = [values['user_name'], hashed_password]
                    menu()
                    break
                except UnicodeEncodeError:
                    window['warn'].update('A senha digitada não pode ser salva, tente outra senha', text_color='red')
                    window.refresh()

        elif button == 'cancel':
            window.close()
            menu()


        elif button == 'exclude_profile':
            layout_2 = [
                [sg.Text(f'Tem certaza que quer excluir {user[0]}', size=(30, 1))],
                [sg.Button('Não', key='no'), sg.Button('Sim', key='yes', button_color=(None, 'red'))]
            ]

            confirm_delete = sg.Window('Confirmação', layout_2)

            button_2 = confirm_delete.Read()

            if button_2[0] == 'yes':
                file = open('./i/l.txt', 'r', encoding='utf-8')
                lines = file.readlines()
                file.close()
                del (lines[lines.index(f'{user[0]} {user[1]}\n')])
                file = open('./i/l.txt', 'w', encoding='utf-8')
                file.writelines(lines)
                file.close()
                confirm_delete.close()
                window.close()
                current_user = user[0]
                user = []
                verify_login('menu', f'{current_user} foi exluído! Faça login novamente')
            else:
                confirm_delete.close()
                edit_profile()

def encrypt(content: dict, save=False):
    # Encriptação por cifra de cesar
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    numbers = '123456789'
    encrypted = {}

    for group in content.items():
        # Encriptar nome
        name = group[0]
        encrypted_name = ''
        for a in name:
            try:
                if a.isnumeric():
                    encrypted_name += numbers[(numbers.index(a) + key_num) % 9]
                elif a.isalpha():
                    if a.isupper():
                        encrypted_name += alphabet[(alphabet.index(a.lower()) + key_num) % 26].upper()
                    else:
                        encrypted_name += alphabet[(alphabet.index(a.lower()) + key_num) % 26].lower()
                else:
                    encrypted_name += a
            except ValueError:
                encrypted_name += a
        # Encriptar conteúdo
        content = group[1]
        encrypted_content = ''
        for a in content:
            try:
                if a.isnumeric():
                    encrypted_content += numbers[(numbers.index(a) + key_num) % 9]
                elif a.isalpha():
                    if a.isupper():
                        encrypted_content += alphabet[(alphabet.index(a.lower()) + key_num) % 26].upper()
                    else:
                        encrypted_content += alphabet[(alphabet.index(a.lower()) + key_num) % 26].lower()
                else:
                    encrypted_content += a
            except ValueError:
                encrypted_content += a
        # Juntar os dois
        encrypted[encrypted_name] = encrypted_content

    if save is True:
        files_names = [0]
        for file in os.listdir('./i/t'):
            files_names.append(int(file.replace('.txt', '')))
        file_name = f'{max(files_names) + 1}.txt'
        file = open(f'./i/t/{file_name}', 'w', encoding='utf-8')
        for line in encrypted.items():
            file.write(f'{line[0]}: {line[1]}\n')
        file.close()

def decrypt_file(file_name, save=False):
    # Descriptografa os arquivos em cifra de cesar
    # file_name = Arquivo a ser descriptografado

    global transactions_list, decrypted
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    numbers = '123456789'
    file = open(f'./i/t/{file_name}', 'r', encoding='utf-8')
    lines = file.readlines()
    file.close()
    decrypted = {}
    for line in lines:
        decrypted[lines.index(line)] = ''
        for a in line:
            if a != '\n':
                try:
                    if a.isnumeric():
                        decrypted[lines.index(line)] += numbers[(numbers.index(a) - key_num) % 9]
                    elif a.isalpha():
                        if a.isupper():
                            decrypted[lines.index(line)] += alphabet[(alphabet.index(a.lower()) - key_num) % 26].upper()
                        else:
                            decrypted[lines.index(line)] += alphabet[(alphabet.index(a.lower()) - key_num) % 26].lower()
                    else:
                        decrypted[lines.index(line)] += a
                except ValueError:
                    decrypted[lines.index(line)] += a


    if save is True:
        # Salvar e atualizar a transação no menu
        if decrypted[0].split()[3] != 'Troca':
            transactions_list.append([sg.Button(f'{decrypted[0].split()[3]} {decrypted[3].replace("Marca: ", "")} {decrypted[4].replace("Modelo: ", "")} {decrypted[5].replace("Ano: ", "")}', size=(55, 2), key=file_name)])
        else:
            transactions_list.append([sg.Button(f'{decrypted[0].split()[3]} {decrypted[4].replace("Modelo Veículo 1: ", "")} {decrypted[18].replace("Modelo Veículo 2: ", "")}', size=(55, 2), key=file_name)])

def show_transaction(file_name):
    # file_name = Transação a ser mostrada na janela
    informations = []
    decrypt_file(file_name)
    for line in decrypted.items():
        informations.append([sg.Text(f'{line[1]}')])

    layout = informations

    window = sg.Window('Transação', layout)
    event = window.Read()

    if event:
        window.close()

verify_login('menu')