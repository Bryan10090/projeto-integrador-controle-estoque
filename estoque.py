"""Sistema de estoque em terminal, com persistência em JSON (biblioteca padrão)."""
import json
from datetime import datetime
from pathlib import Path

ARQUIVO = Path(__file__).with_name('dados_estoque.json')


def carregar():
    if not ARQUIVO.exists():
        return {'produtos': {}, 'movimentacoes': []}
    try:
        dados = json.loads(ARQUIVO.read_text(encoding='utf-8'))
        if not isinstance(dados.get('produtos'), dict) or not isinstance(dados.get('movimentacoes'), list):
            raise ValueError('Estrutura de dados inválida')
        return dados
    except (OSError, ValueError, json.JSONDecodeError) as erro:
        raise RuntimeError(f'Não foi possível ler o arquivo de dados: {erro}') from erro


def salvar(dados):
    temporario = ARQUIVO.with_suffix('.tmp')
    temporario.write_text(json.dumps(dados, ensure_ascii=False, indent=2), encoding='utf-8')
    temporario.replace(ARQUIVO)


def cadastrar(dados, codigo, nome, quantidade, minimo):
    codigo, nome = codigo.strip(), nome.strip()
    if not codigo or not nome or codigo in dados['produtos'] or min(quantidade, minimo) < 0:
        raise ValueError('Código/nome inválido, código duplicado ou valor negativo.')
    dados['produtos'][codigo] = {'nome': nome, 'quantidade': quantidade, 'minimo': minimo}


def movimentar(dados, codigo, tipo, quantidade):
    if codigo not in dados['produtos']:
        raise ValueError('Produto não encontrado.')
    if tipo not in ('entrada', 'saida') or quantidade <= 0:
        raise ValueError('Movimentação inválida.')
    produto = dados['produtos'][codigo]
    if tipo == 'saida' and quantidade > produto['quantidade']:
        raise ValueError('Estoque insuficiente.')
    produto['quantidade'] += quantidade if tipo == 'entrada' else -quantidade
    dados['movimentacoes'].append({'data': datetime.now().isoformat(timespec='seconds'), 'codigo': codigo, 'tipo': tipo, 'quantidade': quantidade})


def inteiro(mensagem):
    try:
        valor = int(input(mensagem))
        if valor < 0:
            raise ValueError
        return valor
    except ValueError:
        print('Digite um número inteiro não negativo.')
        return None


def listar(dados, apenas_baixos=False):
    encontrados = 0
    for codigo, produto in sorted(dados['produtos'].items()):
        if apenas_baixos and produto['quantidade'] > produto['minimo']:
            continue
        situacao = 'REPOR' if produto['quantidade'] <= produto['minimo'] else 'OK'
        print(f"{codigo} | {produto['nome']} | Quantidade: {produto['quantidade']} | Mínimo: {produto['minimo']} | {situacao}")
        encontrados += 1
    if not encontrados:
        print('Nenhum produto encontrado.')


def executar():
    try:
        dados = carregar()
    except RuntimeError as erro:
        print(erro)
        return
    while True:
        print('\n=== CONTROLE DE ESTOQUE ===')
        print('1 Cadastrar | 2 Listar | 3 Entrada | 4 Saída | 5 Estoque baixo | 6 Histórico | 7 Alterar mínimo | 0 Sair')
        opcao = input('Opção: ').strip()
        try:
            if opcao == '0':
                print('Encerrado.'); break
            elif opcao == '1':
                codigo = input('Código: ')
                nome = input('Nome: ')
                quantidade = inteiro('Quantidade inicial: ')
                minimo = inteiro('Estoque mínimo: ')
                if quantidade is None or minimo is None: continue
                cadastrar(dados, codigo, nome, quantidade, minimo)
                salvar(dados); print('Produto cadastrado.')
            elif opcao == '2':
                listar(dados)
            elif opcao in ('3', '4'):
                codigo = input('Código: ').strip()
                quantidade = inteiro('Quantidade: ')
                if quantidade is None: continue
                movimentar(dados, codigo, 'entrada' if opcao == '3' else 'saida', quantidade)
                salvar(dados); print('Movimentação registrada.')
            elif opcao == '5':
                listar(dados, apenas_baixos=True)
            elif opcao == '6':
                for item in dados['movimentacoes']:
                    print(f"{item['data']} | {item['codigo']} | {item['tipo']} | {item['quantidade']}")
                if not dados['movimentacoes']: print('Sem movimentações.')
            elif opcao == '7':
                codigo = input('Código: ').strip()
                if codigo not in dados['produtos']: raise ValueError('Produto não encontrado.')
                minimo = inteiro('Novo mínimo: ')
                if minimo is None: continue
                dados['produtos'][codigo]['minimo'] = minimo
                salvar(dados); print('Mínimo atualizado.')
            else:
                print('Opção inválida.')
        except (ValueError, OSError) as erro:
            print(f'Erro: {erro}')


if __name__ == '__main__':
    executar()
