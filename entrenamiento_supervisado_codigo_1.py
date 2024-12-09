# -*- coding: utf-8 -*-
"""Entrenamiento supervisado codigo 1.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1oSxllCIfTeEalt6vMFagfhLtjOrSLxUv
"""

from sklearn.preprocessing import StandardScaler,MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.feature_selection import VarianceThreshold
from imblearn.over_sampling import SMOTE
import matplotlib.pyplot as plt
import pandas as pd

# Cargar el dataset
def load_data(filepath):
    df = pd.read_csv(filepath)
    return df

# Preprocesamiento de los datos
def preprocess_data(df):
    # Asumimos que 'target' es la columna objetivo
    X = df.drop(columns='target')
    y = df['target']
    # Eliminar características de baja varianza
    vt = VarianceThreshold(threshold=0.01)  # Umbral ajustable
    X_vt = vt.fit_transform(X)
    print(f"Selección de características aplicada: {X_vt.shape[1]} características retenidas.")

    # Normalización (Min-Max Scaling)
    scaler_minmax = MinMaxScaler()
    X_normalized = scaler_minmax.fit_transform(X_vt)
    print(f"Normalización (Min-Max Scaling) aplicada con reslutado:{X_normalized.shape[1]}")

    # Estandarización (Z-score Scaling)
    scaler_standard = StandardScaler()
    X_standardized = scaler_standard.fit_transform(X_normalized)
    print(f"Estandarización (Z-score Scaling) aplicada con reslutado:{X_standardized.shape[1]}")

    print("Datos preprocesados correctamente.\n")
    return X_standardized, y

# Aplicar Min-Max Scaling
def apply_minmax_scaling(X):
    scaler = MinMaxScaler()
    X_scaled = scaler.fit_transform(X)
    return X_scaled

# Dividir los datos en conjunto de entrenamiento y prueba
def split_data(X, y, test_size=0.2):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42)
    print(f"Datos divididos: {len(X_train)} para entrenamiento y {len(X_test)} para prueba.")
    return X_train, X_test, y_train, y_test

# Balanceo de clases con SMOTE
def balance_data(X_train, y_train):
    smote = SMOTE(random_state=42)
    X_train_res, y_train_res = smote.fit_resample(X_train, y_train)
    return X_train_res, y_train_res

# Entrenamiento del modelo con RandomForest
def train_random_forest(X_train, y_train):
    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)
    return model

# Evaluación del modelo
def evaluate_model(model, X_test, y_test):
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    cm = confusion_matrix(y_test, y_pred)
    print(f'Exactitud del modelo: {accuracy:.4f}')
    return accuracy, cm

# Visualización de la matriz de confusión
def plot_confusion_matrix(cm):
    plt.figure(figsize=(6,6))
    plt.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
    plt.title('Matriz de Confusión')
    plt.colorbar()
    tick_marks = range(len(cm))
    plt.xticks(tick_marks, tick_marks)
    plt.yticks(tick_marks, tick_marks)
    plt.ylabel('Etiqueta Real')
    plt.xlabel('Etiqueta Predicha')
    plt.show()

# Función principal
def main():
    # Cargar los datos
    df = load_data('heart.csv')

    # Preprocesamiento
    X, y = preprocess_data(df)

    # Aplicar Min-Max Scaling
    X_scaled = apply_minmax_scaling(X)

    print("💨Splits - Primera ejecución (0.8 - 0.2)\n")

    # División de datos 0.8-0.2
    X_train, X_test, y_train, y_test = split_data(X_scaled, y, test_size=0.2)

    # Balanceo de clases (opcional)
    X_train_res, y_train_res = balance_data(X_train, y_train)

    # Entrenamiento del modelo
    model = train_random_forest(X_train_res, y_train_res)

    # Evaluación
    accuracy, cm = evaluate_model(model, X_test, y_test)

    # Matriz de confusión
    plot_confusion_matrix(cm)

    print("\n💨Splits - Segunda ejecución(0.5 - 0.5)\n")
    # División de datos 0.5-0.5
    X_train, X_test, y_train, y_test = split_data(X_scaled, y, test_size=0.5)

      # Balanceo de clases (opcional)
    X_train_res, y_train_res = balance_data(X_train, y_train)

    # Entrenamiento del modelo
    model = train_random_forest(X_train_res, y_train_res)

    # Evaluación
    accuracy, cm = evaluate_model(model, X_test, y_test)

    # Matriz de confusión
    plot_confusion_matrix(cm)
if __name__ == "__main__":
    main()
