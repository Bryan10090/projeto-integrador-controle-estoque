import unittest
from estoque import cadastrar, movimentar

class TesteEstoque(unittest.TestCase):
    def setUp(self):
        self.dados = {'produtos': {}, 'movimentacoes': []}
        cadastrar(self.dados, 'A1', 'Caneta', 10, 3)

    def test_cadastro(self):
        self.assertEqual(self.dados['produtos']['A1']['quantidade'], 10)

    def test_entrada(self):
        movimentar(self.dados, 'A1', 'entrada', 5)
        self.assertEqual(self.dados['produtos']['A1']['quantidade'], 15)

    def test_saida(self):
        movimentar(self.dados, 'A1', 'saida', 4)
        self.assertEqual(self.dados['produtos']['A1']['quantidade'], 6)

    def test_saida_excessiva(self):
        with self.assertRaises(ValueError):
            movimentar(self.dados, 'A1', 'saida', 11)

    def test_codigo_duplicado(self):
        with self.assertRaises(ValueError):
            cadastrar(self.dados, 'A1', 'Lápis', 2, 1)

    def test_quantidade_zero(self):
        with self.assertRaises(ValueError):
            movimentar(self.dados, 'A1', 'entrada', 0)

if __name__ == '__main__':
    unittest.main()
