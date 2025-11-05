import unittest
import pandas as pd
import numpy as np
from src.preprocesamiento import PreprocessingPipeline # Asegúrate que tu clase se llama así y está en src/

# Datos de prueba simples para los tests
TEST_DATA = pd.DataFrame({
    'numeric_col': [1.0, 2.0, 3.0, 4.0, 5.0, np.nan], # Un nulo al final
    'outlier_col': [10, 12, 11, 13, 100, 15], # 100 es un outlier
    'categorical_col': ['A', 'B', 'A', 'C', 'B', 'C'],
    'duplicate_col': [1, 2, 3, 4, 5, 1],
    'target': [10, 20, 30, 40, 50, 60]
})

class TestPreprocessingPipeline(unittest.TestCase):
    """Clase de pruebas unitarias para PreprocessingPipeline.
    
    Aseguramos que cada método de transformación altere el DataFrame (self.df)
    de la manera esperada.
    """

    def setUp(self):
        """Prepara el entorno antes de cada test: se ejecuta antes de cada método test_"""
        # Inicializa una nueva instancia del pipeline con una COPIA de los datos
        self.data = TEST_DATA.copy()
        self.pipeline = PreprocessingPipeline(self.data)

    def test_initialization_successful(self):
        """Verifica que la clase se inicializa correctamente y carga el DataFrame."""
        self.assertIsInstance(self.pipeline.df, pd.DataFrame, "La instancia no contiene un DataFrame de pandas.")
        self.assertEqual(len(self.pipeline.df), 6, "El DataFrame no cargó el número correcto de filas.")

    def test_eliminar_duplicados(self):
        """Verifica que el método de eliminación de duplicados funciona correctamente."""
        # Creamos datos con una fila duplicada para la prueba
        df_duplicado = pd.concat([self.data, self.data.iloc[0:1]], ignore_index=True)
        pipeline_duplicado = PreprocessingPipeline(df_duplicado)
        
        # Ejecutamos el método
        pipeline_duplicado.eliminar_duplicados()
        
        # El resultado esperado es 6 filas (se elimina la fila duplicada)
        self.assertEqual(len(pipeline_duplicado.df), 6, "No se eliminó la fila duplicada correctamente.")
        
    def test_gestionar_nulos_imputar_media(self):
        """Verifica que los nulos se imputen correctamente usando la media."""
        # Columna con nulos: 'numeric_col' = [1.0, 2.0, 3.0, 4.0, 5.0, nan]
        # Media de los 5 valores no nulos: (1+2+3+4+5) / 5 = 3.0
        
        self.pipeline.gestionar_nulos(columnas=['numeric_col'], estrategia='media')
        
        # Verificamos que ya no hay nulos en esa columna
        self.assertFalse(self.pipeline.df['numeric_col'].isnull().any(), "No se imputaron los nulos.")
        
        # Verificamos que el valor imputado sea la media (3.0)
        imputed_value = self.pipeline.df['numeric_col'].iloc[-1]
        self.assertAlmostEqual(imputed_value, 3.0, places=5, msg="El valor imputado no es la media correcta.")

    def test_gestionar_nulos_eliminar_filas(self):
        """Verifica que se eliminen correctamente las filas con nulos."""
        # Hay un nulo en la última fila
        self.pipeline.gestionar_nulos(columnas=['numeric_col'], estrategia='eliminar_filas')
        
        # El resultado esperado es 5 filas (se elimina la última fila con nan)
        self.assertEqual(len(self.pipeline.df), 5, "No se eliminó la fila con nulos correctamente.")

    def test_escalar_variables_minmax(self):
        """Verifica que las variables numéricas se escalen con Min-Max."""
        # Seleccionamos solo la columna numérica (ya imputada previamente si fuera necesario, 
        # pero para el test usaremos datos limpios)
        df_clean = TEST_DATA.dropna().copy()
        pipeline_clean = PreprocessingPipeline(df_clean)
        
        # Escalar
        pipeline_clean.escalar_variables(tipo_escalado='MinMaxScaler', columnas=['numeric_col'])
        
        scaled_col = pipeline_clean.df['numeric_col']
        
        # MinMax debe resultar en min=0 y max=1
        self.assertAlmostEqual(scaled_col.min(), 0.0, places=5, msg="El mínimo no es 0 después de Min-Max.")
        self.assertAlmostEqual(scaled_col.max(), 1.0, places=5, msg="El máximo no es 1 después de Min-Max.")
        self.assertIsInstance(pipeline_clean.scaler, object, "El scaler no se guardó en la instancia.")

    def test_gestionar_outliers_acotar(self):
        """Verifica que los outliers se acoten (capping) usando IQR."""
        # Usamos 'outlier_col': [10, 12, 11, 13, 100, 15]
        # El valor 100 es un outlier que debe ser acotado.
        
        # Para esta columna, los valores "normales" son bajos, 100 será acotado
        self.pipeline.gestionar_outliers(columnas=['outlier_col'], accion='acotar', metodo='IQR')
        
        # El nuevo valor máximo (Q3 + 1.5*IQR) debería ser significativamente menor que 100
        new_max = self.pipeline.df['outlier_col'].max()
        
        # Verificamos que 100 haya sido reducido (acotado)
        self.assertLess(new_max, 100, "El outlier no fue acotado correctamente.")
        self.assertLess(new_max, 25, "El valor máximo acotado sigue siendo demasiado alto.")


if __name__ == '__main__':
    unittest.main()