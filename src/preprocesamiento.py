"""
Módulo de preprocesamiento de datos
Contiene funciones para limpieza, transformación y preparación de datasets
"""

import pandas as pd
import numpy as np
# Se importa LabelEncoder y los Scalers, aunque solo MinMaxScaler y StandardScaler se usan directamente.
from sklearn.preprocessing import StandardScaler, MinMaxScaler, LabelEncoder
from sklearn.impute import SimpleImputer
from typing import Dict, Any, List

class PreprocessingPipeline:
    """
    Pipeline completo para preprocesamiento de datos.
    Los métodos que modifican el DataFrame devuelven 'self' para permitir el encadenamiento de operaciones.
    """
    
    def __init__(self, df: pd.DataFrame):
        """
        Inicializa el pipeline con un DataFrame.
        
        Args:
            df (pd.DataFrame): Dataset a procesar
        """
        self.df = df.copy()
        self.original_df = df.copy()
        self.scaler = None
        self.label_encoders = {}
        print("Pipeline de Preprocesamiento inicializado.")
        
    def info_dataset(self):
        """
        Muestra y devuelve información general del dataset.
        
        Returns:
            dict: Diccionario con información del dataset
        """
        info = {
            'filas': self.df.shape[0],
            'columnas': self.df.shape[1],
            'valores_nulos': self.df.isnull().sum().to_dict(),
            'tipos_datos': self.df.dtypes.to_dict(),
            'duplicados': self.df.duplicated().sum()
        }
        
        # Impresión de información (opcional, pero útil)
        print("\n--- Información del Dataset ---")
        print(f"Filas: {info['filas']}")
        print(f"Columnas: {info['columnas']}")
        print(f"Total de duplicados: {info['duplicados']}")
        print(f"Tipos de datos únicos:\n{self.df.dtypes.value_counts()}")
        print("-----------------------------\n")
        
        return info
    
    def eliminar_duplicados(self):
        """
        Elimina filas duplicadas del dataset.
        
        Returns:
            self: Permite el encadenamiento de métodos.
        """
        duplicados_antes = self.df.duplicated().sum()
        self.df = self.df.drop_duplicates().reset_index(drop=True)
        duplicados_eliminados = duplicados_antes - self.df.duplicated().sum()
        
        print(f"✓ Duplicados eliminados: {duplicados_eliminados}")
        return self # CLAVE: Devuelve self
    
    def manejar_valores_nulos(self, strategy='mean', columns: List[str] = None):
        """
        Maneja valores nulos en el dataset.
        
        Args:
            strategy (str): Estrategia para imputar ('mean', 'median', 'most_frequent', 'drop')
            columns (list): Columnas específicas a procesar. Si es None, procesa todas las que tengan nulos.
            
        Returns:
            self: Permite el encadenamiento de métodos.
        """
        if columns is None:
            # Selecciona solo columnas con al menos un nulo
            columns = self.df.columns[self.df.isnull().any()].tolist()
        
        if strategy == 'drop':
            filas_antes = len(self.df)
            self.df = self.df.dropna(subset=columns)
            filas_despues = len(self.df)
            print(f"✓ Filas con nulos eliminadas: {filas_antes - filas_despues}")
        else:
            numeric_cols = self.df[columns].select_dtypes(include=[np.number]).columns
            
            if len(numeric_cols) > 0:
                imputer = SimpleImputer(strategy=strategy)
                self.df[numeric_cols] = imputer.fit_transform(self.df[numeric_cols])
                print(f"✓ Valores nulos numéricos imputados con estrategia: {strategy}")
        
        return self # CLAVE: Devuelve self
    
    def detectar_outliers(self, columns: List[str] = None, method='iqr', threshold=1.5) -> Dict[str, List[int]]:
        """
        Detecta valores atípicos en columnas numéricas.
        
        Returns:
            dict: Diccionario con índices (locations) de outliers por columna.
        """
        if columns is None:
            columns = self.df.select_dtypes(include=[np.number]).columns.tolist()
        
        outliers = {}
        # Lógica de detección (se mantiene igual)
        for col in columns:
            if method == 'iqr':
                Q1 = self.df[col].quantile(0.25)
                Q3 = self.df[col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - threshold * IQR
                upper_bound = Q3 + threshold * IQR
                outliers_mask = (self.df[col] < lower_bound) | (self.df[col] > upper_bound)
                outliers[col] = self.df[outliers_mask].index.tolist()
            elif method == 'zscore':
                z_scores = np.abs((self.df[col] - self.df[col].mean()) / self.df[col].std())
                outliers_mask = z_scores > threshold
                outliers[col] = self.df[outliers_mask].index.tolist()
        
        print(f"✓ Outliers detectados en {len(outliers)} columnas numéricas.")
        return outliers # NOTA: Este método devuelve el diccionario, no 'self'

    def tratar_outliers(self, columns: List[str] = None, method='iqr', action='remove', threshold=1.5):
        """
        Trata valores atípicos (eliminar o acotar/cap).
        
        Returns:
            self: Permite el encadenamiento de métodos.
        """
        if columns is None:
            columns = self.df.select_dtypes(include=[np.number]).columns.tolist()
        
        for col in columns:
            # Lógica de detección y tratamiento (se mantiene igual)
            if method == 'iqr':
                Q1 = self.df[col].quantile(0.25)
                Q3 = self.df[col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - threshold * IQR
                upper_bound = Q3 + threshold * IQR
                
                if action == 'remove':
                    # Usar la negación de la máscara de outliers
                    self.df = self.df[(self.df[col] >= lower_bound) & (self.df[col] <= upper_bound)]
                elif action == 'cap':
                    self.df[col] = self.df[col].clip(lower=lower_bound, upper=upper_bound)
        
        print(f"✓ Outliers tratados con método {method} y acción {action}.")
        return self # CLAVE: Devuelve self
    
    def normalizar_datos(self, columns: List[str] = None, method='standard'):
        """
        Normaliza o estandariza columnas numéricas.
        
        Returns:
            self: Permite el encadenamiento de métodos.
        """
        if columns is None:
            columns = self.df.select_dtypes(include=[np.number]).columns.tolist()
        
        if method == 'standard':
            self.scaler = StandardScaler()
        elif method == 'minmax':
            self.scaler = MinMaxScaler()
        else:
             print(f"Advertencia: Método {method} no reconocido. Usando Standard por defecto.")
             self.scaler = StandardScaler()
        
        self.df[columns] = self.scaler.fit_transform(self.df[columns])
        print(f"✓ Datos numéricos transformados con método: {method}")
        
        return self # CLAVE: Devuelve self
    
    def codificar_categoricas(self, columns: List[str] = None):
        """
        Codifica variables categóricas usando Label Encoding.
        
        Returns:
            self: Permite el encadenamiento de métodos.
        """
        if columns is None:
            columns = self.df.select_dtypes(include=['object']).columns.tolist()
        
        for col in columns:
            le = LabelEncoder()
            # Se usa astype(str) para manejar nulos como categoría
            self.df[col] = le.fit_transform(self.df[col].astype(str)) 
            self.label_encoders[col] = le
        
        print(f"✓ Variables categóricas codificadas (Label Encoding): {columns}")
        return self # CLAVE: Devuelve self
    
    def crear_dummies(self, columns: List[str]):
        """
        Crea variables dummy (One-Hot Encoding) usando pandas.get_dummies.
        
        Returns:
            self: Permite el encadenamiento de métodos.
        """
        self.df = pd.get_dummies(self.df, columns=columns, drop_first=True)
        print(f"✓ Variables dummy creadas para: {columns}")
        return self # CLAVE: Devuelve self
    
    def pipeline_completo(self, 
                          eliminar_dup=True,
                          manejar_nulos='mean',
                          tratar_outliers_config: Dict[str, Any] = None,
                          normalizar=True,
                          codificar_cat=True):
        """
        Ejecuta el pipeline completo de preprocesamiento.
        """
        print("=" * 50)
        print("INICIANDO PIPELINE DE PREPROCESAMIENTO AUTOMÁTICO")
        print("=" * 50)
        
        if eliminar_dup:
            self.eliminar_duplicados()
        
        if manejar_nulos:
            self.manejar_valores_nulos(strategy=manejar_nulos)
        
        if tratar_outliers_config:
            self.tratar_outliers(**tratar_outliers_config)
        
        if codificar_cat:
            # Primero Label Encoding (para variables ordinales o target)
            cat_cols = self.df.select_dtypes(include=['object']).columns.tolist()
            if cat_cols:
                self.codificar_categoricas(cat_cols)
        
        if normalizar:
            num_cols = self.df.select_dtypes(include=[np.number]).columns.tolist()
            if num_cols:
                self.normalizar_datos(num_cols)
        
        print("=" * 50)
        print("PIPELINE COMPLETADO EXITOSAMENTE")
        self.info_dataset() # Muestra el resultado final
        print("=" * 50)
        
        return self.df
    
    def exportar_datos(self, filename='datos_procesados.csv', path='data/processed/'):
        """
        Exporta el dataset procesado
        """
        full_path = path + filename
        self.df.to_csv(full_path, index=False)
        print(f"✓ Datos exportados a: {full_path}")


# Funciones auxiliares independientes
def cargar_dataset(filepath, **kwargs):
    """
    Carga un dataset desde un archivo (CSV o Excel).
    """
    if filepath.endswith('.csv'):
        return pd.read_csv(filepath, **kwargs)
    elif filepath.endswith(('.xls', '.xlsx')):
        return pd.read_excel(filepath, **kwargs)
    else:
        raise ValueError("Formato de archivo no soportado. Use .csv, .xls o .xlsx")


def resumen_estadistico(df):
    """
    Genera un resumen estadístico del dataset (describe).
    """
    return df.describe(include='all')


if __name__ == "__main__":
    # Ejemplo de uso (Simulación)
    print("Módulo de preprocesamiento de datos cargado correctamente")
    # Para usar este módulo, tendrías que simular un DataFrame:
    # data = {'col1': [1, 2, np.nan, 4], 'col2': ['a', 'b', 'a', 'c']}
    # df_test = pd.DataFrame(data)
    
    # pipeline = PreprocessingPipeline(df_test)
    # pipeline.eliminar_duplicados().manejar_valores_nulos(strategy='median')
    pass