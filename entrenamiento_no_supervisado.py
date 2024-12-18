# -*- coding: utf-8 -*-
"""Entrenamiento  no supervisado.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1rfCKEAarHEsBwoMEr307zKQdb0ZvVS07
"""

from sklearn.preprocessing import MinMaxScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import adjusted_rand_score
# Cargar el dataset
def load_data(filepath):
    df = pd.read_csv(filepath)
    return df

# Preprocesamiento de los datos
def preprocess_data(df):
    # Remover la columna 'target' (sin usar etiquetas de clase)
    X = df.drop(columns='target')
    return X

# Aplicar Min-Max Scaling
def apply_minmax_scaling(X):
    scaler = MinMaxScaler()
    X_scaled = scaler.fit_transform(X)
    return X_scaled

# Aplicar PCA para reducción de dimensionalidad
def apply_pca(X, n_components):
    pca = PCA(n_components=n_components)
    X_pca = pca.fit_transform(X)
    return X_pca, pca

# Aplicar K-Means para clustering
def apply_kmeans(X, n_clusters):
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    labels = kmeans.fit_predict(X)
    return labels, kmeans

# Visualización de clusters en 2D
def plot_clusters(X, labels):
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x=X[:, 0], y=X[:, 1], hue=labels, palette='Set1')
    plt.title('Clusters encontrados por K-Means')
    plt.xlabel('Componente Principal 1')
    plt.ylabel('Componente Principal 2')
    plt.legend(title='Cluster')
    plt.show()

# Función principal
def main():
    # Cargar los datos
    df = load_data('heart.csv')

    # Preprocesamiento
    X = preprocess_data(df)

    # Aplicar Min-Max Scaling
    X_scaled = apply_minmax_scaling(X)

    # Aplicar PCA para reducir a 2 componentes para visualización
    X_pca, pca = apply_pca(X_scaled, n_components=2)

    # Aplicar K-Means con 2 clusters (enfermo vs. sano es una hipótesis)
    labels, kmeans = apply_kmeans(X_pca, n_clusters=2)

    # Visualizar los clusters
    plot_clusters(X_pca, labels)

    # Mostrar información relevante
    print("Centroides de los clusters:\n", kmeans.cluster_centers_)
    print("Inercia del modelo (menor es mejor):", kmeans.inertia_)



if __name__ == "__main__":
    main()