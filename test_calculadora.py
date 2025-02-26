import unittest
import pandas as pd
from calculadora import add, create_operations_log

class TestCalculadora(unittest.TestCase):
    def test_add_integers(self):
        """Test suma de números enteros"""
        self.assertEqual(add(5, 3), 8)
        self.assertEqual(add(-1, 1), 0)
        self.assertEqual(add(0, 0), 0)
    
    def test_add_floats(self):
        """Test suma de números decimales"""
        self.assertAlmostEqual(add(3.5, 2.5), 6.0)
        self.assertAlmostEqual(add(0.1, 0.2), 0.3, places=1)
    
    def test_create_operations_log(self):
        """Test creación del DataFrame con operaciones"""
        operations = [
            (5, 3, 8),
            (2, 2, 4)
        ]
        df = create_operations_log(operations)
        
        # Verificar que el DataFrame se creó correctamente
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(len(df), 2)
        
        # Verificar las columnas
        expected_columns = ['Number1', 'Number2', 'Result', 'Operation_Date', 
                          'Is_Result_Even', 'Numbers_Sum_Greater_Than_10']
        self.assertListEqual(list(df.columns), expected_columns)
        
        # Verificar cálculos
        self.assertTrue(df['Is_Result_Even'].all())  # Todos los resultados son pares
        self.assertTrue(df.loc[0, 'Numbers_Sum_Greater_Than_10'])  # 5 + 3 > 10 es False
        self.assertFalse(df.loc[1, 'Numbers_Sum_Greater_Than_10'])  # 2 + 2 > 10 es False

if __name__ == '__main__':
    unittest.main() 