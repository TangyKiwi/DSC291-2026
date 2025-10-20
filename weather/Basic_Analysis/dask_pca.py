#!/usr/bin/env python3
"""
Dask PCA Implementation

A standalone implementation of PCA for Dask arrays that handles NaN values.
This module provides efficient PCA computation for large datasets using Dask.
"""

import dask.array as da
import numpy as np


def dask_pca(X, n_components=None):
    """
    Compute PCA for a dask array X (samples x features).
    Returns principal components and explained variances.
    
    Parameters:
        X: dask.array.Array, shape (n_samples, n_features)
        n_components: int or None, number of PCs to compute (default: all)
    Returns:
        components_: principal axes (n_components, n_features)
        explained_variances_: variances explained by each PC (n_components,)
        mean_: mean of X (n_features,)
    """
    # Use nanmean to center, ignoring NaNs
    mean_ = da.nanmean(X, axis=0)
    Xc = X - mean_

    # For covariance, handle NaNs: for each pair of features, compute the mean excluding any rows with NaN in either feature

    # We'll compute the valid-count matrix and the nan-aware cross-products via masked arrays

    # Compute dot product (ignoring NaNs)
    # Use masked_arrays to compute sums where both values are finite
    def nan_cov(a):
        # a: (n_samples, n_features)
        valid = da.isfinite(a)
        counts = da.matmul(valid.T, valid)
        
        # Handle case where counts might be 0 or 1
        counts = da.where(counts <= 1, 2, counts)
        
        # Use nan_to_num to replace NaN with 0 for covariance computation
        a_clean = da.nan_to_num(a)
        product = da.matmul(a_clean.T, a_clean)
        cov = product / (counts - 1)
        
        # Ensure covariance matrix is symmetric and positive semi-definite
        cov = (cov + cov.T) / 2
        
        return cov

    cov = nan_cov(Xc)
    # Convert to numpy for eigendecomposition
    cov = cov.compute()

    # Add small regularization for numerical stability
    cov = cov + np.eye(cov.shape[0]) * 1e-10

    # Eigen decomposition
    try:
        eigvals, eigvecs = np.linalg.eigh(cov)
    except np.linalg.LinAlgError:
        # If eigh fails, try with SVD
        try:
            U, s, Vt = np.linalg.svd(cov, full_matrices=False)
            eigvals = s ** 2
            eigvecs = U
        except np.linalg.LinAlgError:
            # Final fallback: use sklearn PCA
            from sklearn.decomposition import PCA
            X_clean = da.nan_to_num(X).compute()
            pca = PCA(n_components=n_components)
            pca.fit(X_clean)
            eigvecs = pca.components_.T
            eigvals = pca.explained_variance_
            mean_ = pca.mean_
            return eigvecs, eigvals, mean_
    
    # Sort eigenvalues & eigenvectors in descending order
    idx = eigvals.argsort()[::-1]
    eigvals = eigvals[idx]
    eigvecs = eigvecs[:, idx]

    if n_components is not None:
        eigvals = eigvals[:n_components]
        eigvecs = eigvecs[:, :n_components]

    # eigvecs: columns are principal axes
    return eigvecs.T, eigvals, mean_.compute()


def dask_pca_transform(X, components_, mean_):
    """
    Transform data using computed PCA components.
    
    Parameters:
        X: dask.array.Array, shape (n_samples, n_features)
        components_: principal axes (n_components, n_features)
        mean_: mean of X (n_features,)
    Returns:
        X_transformed: transformed data (n_samples, n_components)
    """
    # Center the data
    Xc = X - mean_
    
    # Transform using principal components
    X_transformed = da.matmul(Xc, components_.T)
    
    return X_transformed


def dask_pca_inverse_transform(X_transformed, components_, mean_):
    """
    Inverse transform PCA data back to original space.
    
    Parameters:
        X_transformed: transformed data (n_samples, n_components)
        components_: principal axes (n_components, n_features)
        mean_: mean of X (n_features,)
    Returns:
        X_reconstructed: reconstructed data (n_samples, n_features)
    """
    # Transform back to original space
    X_reconstructed = da.matmul(X_transformed, components_) + mean_
    
    return X_reconstructed


def dask_pca_explained_variance_ratio(explained_variances_):
    """
    Calculate explained variance ratio for each principal component.
    
    Parameters:
        explained_variances_: variances explained by each PC
    Returns:
        explained_variance_ratio_: ratio of explained variance for each PC
    """
    total_variance = da.sum(explained_variances_)
    explained_variance_ratio_ = explained_variances_ / total_variance
    
    return explained_variance_ratio_


# Example usage
if __name__ == "__main__":
    # Create sample data
    import dask.array as da
    
    # Generate random data with some NaN values
    np.random.seed(42)
    n_samples, n_features = 1000, 50
    X = da.random.random((n_samples, n_features))
    
    # Add some NaN values
    nan_mask = da.random.random((n_samples, n_features)) < 0.1
    X = da.where(nan_mask, np.nan, X)
    
    print(f"Sample data shape: {X.shape}")
    print(f"Number of NaN values: {da.isnan(X).sum().compute()}")
    
    # Perform PCA
    components_, explained_variances_, mean_ = dask_pca(X, n_components=3)
    
    print(f"Components shape: {components_.shape}")
    print(f"Explained variances: {explained_variances_}")
    
    # Calculate explained variance ratio
    explained_variance_ratio_ = dask_pca_explained_variance_ratio(explained_variances_)
    print(f"Explained variance ratio: {explained_variance_ratio_.compute()}")
    
    # Transform data
    X_transformed = dask_pca_transform(X, components_, mean_)
    print(f"Transformed data shape: {X_transformed.shape}")
    
    # Inverse transform
    X_reconstructed = dask_pca_inverse_transform(X_transformed, components_, mean_)
    print(f"Reconstructed data shape: {X_reconstructed.shape}")
