# Sistema de Controle de Estoque

Projeto acadêmico demonstrativo para a disciplina Laboratório de Programação da UNISA.

## Requisitos
Python 3.9 ou superior. Não utiliza bibliotecas externas.

## Execução
No terminal, dentro da pasta do projeto:

```bash
python estoque.py
```

O arquivo `dados_estoque.json` é criado automaticamente na primeira alteração. Faça backup desse arquivo para preservar os registros.

## Testes
```bash
python -m unittest -v test_estoque.py
```

## Funcionalidades
Cadastro, listagem, entradas, saídas com bloqueio de saldo negativo, alerta de reposição, histórico e alteração de estoque mínimo.

## Limitações
Aplicação local em terminal, sem autenticação, multiusuário ou banco de dados transacional. Não use dados sensíveis.

## Entrega
Preencher os dados acadêmicos no relatório, executar e registrar evidências reais, publicar este código em repositório próprio e inserir o link na capa do relatório.
