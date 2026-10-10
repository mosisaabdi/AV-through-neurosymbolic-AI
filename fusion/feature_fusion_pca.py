import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

class FeatureFusionPCA:
    """Generic concatenate/scale/PCA helper; use only if it matches your method."""
    def __init__(self, n_components, standardize=True, random_state=42):
        self.scaler = StandardScaler() if standardize else None
        self.pca = PCA(n_components=n_components, random_state=random_state)
        self.fitted = False

    @staticmethod
    def _matrix(features):
        if not features:
            raise ValueError("features must not be empty")
        rows = [np.asarray(x).reshape(-1) for x in features]
        if len({len(row) for row in rows}) != 1:
            raise ValueError("All feature vectors must have the same length")
        return np.stack(rows)

    def fit(self, train_features):
        x = self._matrix(train_features)
        if self.scaler:
            x = self.scaler.fit_transform(x)
        self.pca.fit(x)
        self.fitted = True
        return self

    def transform(self, features):
        if not self.fitted:
            raise RuntimeError("Fit using training features first")
        x = self._matrix(features)
        if self.scaler:
            x = self.scaler.transform(x)
        return self.pca.transform(x)

    def fit_transform(self, train_features):
        self.fit(train_features)
        return self.transform(train_features)
