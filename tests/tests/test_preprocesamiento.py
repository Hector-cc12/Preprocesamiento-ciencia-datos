import unittest
import pandas as pd
from src.preprocesamiento import PreprocessingPipeline # Asegúrate que tu clase se llama así y está en src/

# Datos de prueba simples para los tests
TEST_DATA = pd.DataFrame({
    'numeric_col': [1, 2, 3, 4, 5, None],
    'categorical_col': ['A', 'B', 'A', 'C', 'B', 'C'],
    'duplicate_col': [1, 2, 3, 4, 5, 1],
    'target': [10, 20, 30, 40, 50, 60]
})

class TestPreprocessingPipeline(unittest.TestCase):
    """Clase de pruebas unitarias para PreprocessingPipeline."""

    def setUp(self):
        """Prepara el entorno antes de cada test: se ejecuta antes de cada método test_"""
        # Inicializa una nueva instancia del pipeline con una copia de los datos
        self.data = TEST_DATA.copy()
        self.pipeline = PreprocessingPipeline(self.data)

    def test_initialization_successful(self):
        """Verifica que la clase se inicializa correctamente y carga el DataFrame."""
        self.assertIsInstance(self.pipeline.df, pd.DataFrame, "La instancia no contiene un DataFrame de pandas.")
        self.assertEqual(len(self.pipeline.df), 6, "El DataFrame no cargó el número correcto de filas.")

    def test_eliminar_duplicados(self):
        """Verifica que el método de eliminación de duplicados funciona correctamente."""
        # Creamos datos con una fila duplicada
        df_duplicado = pd.concat([self.data, self.data.iloc[0:1]], ignore_index=True)
        pipeline_duplicado = PreprocessingPipeline(df_duplicado)
        
        # Ejecutamos el método
        pipeline_duplicado.eliminar_duplicados()
        
        # Debe reducirse a 6 filas (la original sin duplicados)
        self.assertEqual(len(pipeline_duplicado.df), 6, "No se eliminó la fila duplicada correctamente.")

    # A medida que avanzamos, agregaremos más pruebas unitarias aquí.

if __name__ == '__main__':
    unittest.main()