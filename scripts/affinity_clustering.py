from sklearn.cluster import AffinityPropagation
from sklearn import preprocessing
import matplotlib.pyplot as plt
import pandas as pd
from car_accident_traitement import df

def affinity_clustering(df, severities_df):

    # Standardize your features
    X_scaled = preprocessing.scale(df)  # Standardize your features
    new_df = df.drop(['Accident_Severity'], axis='columns')

    # Apply Affinity Propagation
    af = AffinityPropagation().fit(X_scaled)
    cluster_centers_indices = af.cluster_centers_indices_
    labels = af.labels_

    # Map clusters to severities
    cluster_severities = severities_df.iloc[cluster_centers_indices]

    # Print the cluster labels and corresponding severities
    #for cluster_label, severity in zip(cluster_centers_indices, cluster_severities):
    #    print(f"Cluster {cluster_label} corresponds to Severity {severity}")

    # Assuming 'X' is your feature matrix, and 'severities' is your target variable
    # (as used in the previous example)

    # Scatter plot of the first two features
    plt.scatter(X_scaled[:, 0], X_scaled[:, 1], c=labels, cmap='viridis', s=50, alpha=0.5)

    # Highlight cluster centers
    plt.scatter(X_scaled[cluster_centers_indices, 0], X_scaled[cluster_centers_indices, 1],
                c='red', marker='x', s=200, label='Cluster Centers')

    # Add labels and legend
    plt.title('Affinity Propagation Clustering with Severities')
    plt.xlabel('Feature 1 (Standardized)')
    plt.ylabel('Feature 2 (Standardized)')
    plt.legend()

    # Show the plot
    plt.show()

df = df.truncate(after=100)

severities_df = df['Accident_Severity']

affinity_clustering(df, severities_df)
