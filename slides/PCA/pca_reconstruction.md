# Principal Component Analysis and Reconstruction

**Title**: Principal Component Analysis and Reconstruction  
**Author**: Prepared for dask-CSE255

---

## Slide 1: Title Page

---

## Slide 2: Intuition

- High-dimensional data often lie near a low-dimensional subspace.
- PCA finds orthogonal directions that maximize variance.
- Reconstruction uses a subset of these components to approximate the original data.

---

## Slide 3: Notation

- Data matrix: **X** ∈ ℝ^(n × d) centered (zero mean per feature).
- Covariance matrix: **Σ** = (1/(n-1)) **X**^T **X**.
- Eigen-decomposition: **Σ** = **U** **Λ** **U**^T, with **U** = [**u**₁, ..., **u**_d] orthonormal.

---

## Slide 4: Variance Maximization

**u**₁ = arg max_{||**u**|| = 1} **u**^T **Σ** **u**

**u**_k = arg max_{||**u**|| = 1, **u** ⟂ {**u**₁, ..., **u**_{k-1}}} **u**^T **Σ** **u**

- Each eigenvector captures decreasing variance λ₁ ≥ λ₂ ≥ ... ≥ λ_d.
- Project data: **Z** = **X** **U**.

---

## Slide 5: Projection Diagram

[Diagram showing projection of point x onto principal axis u₁]

- x projects onto principal axis u₁ yielding coordinate z₁ = x^T u₁.
- Residual **r** captures information lost in projection.

---

## Slide 6: k-Dimensional Subspace

- Keep top k eigenvectors: **U**_k = [**u**₁, ..., **u**_k].
- Low-dimensional representation: **Z**_k = **X** **U**_k.
- Reconstruction: **X̂** = **Z**_k **U**_k^T.

**x̂**_i = Σ_{j=1}^k z_{ij} **u**_j

---

## Slide 7: Reconstruction Error

E_k = ||**X** - **X̂**||_F^2 = Σ_{j=k+1}^d λ_j

- Error equals sum of discarded eigenvalues.
- Explained variance ratio (EVR):

EVR(k) = (Σ_{j=1}^k λ_j) / (Σ_{j=1}^d λ_j)

- Choose k to balance compression and fidelity.

---

## Slide 8: Summary

- PCA rotates data into variance-ranked axes.
- Reconstruction uses leading components to approximate original data.
- Evaluate trade-off via explained variance and residual error.

