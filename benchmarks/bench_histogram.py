from time import time
import numpy as np
from joblib import Memory
from pygbm.histogram import Histogram

m = Memory(location='/tmp')


@m.cache
def make_data(n_bins=256, n_samples=int(1e8), n_subsample=int(1e6),
              loss_dtype=np.float32, binned_feature_dtype=np.uint8, seed=42):
    rng = np.random.RandomState(seed)

    ordered_gradients = rng.randn(n_subsample).astype(loss_dtype)
    ordered_hessians = rng.randn(n_subsample).astype(loss_dtype)

    binned_feature = rng.randint(0, n_bins - 1, size=n_samples)
    binned_feature = binned_feature.astype(np.uint8)

    sample_indices = rng.choice(np.arange(n_samples, dtype=np.uint32),
                                n_subsample, replace=False)
    return sample_indices, binned_feature, ordered_gradients, ordered_hessians


n_bins = 256
sample_indices, binned_feature, gradients, hessians = make_data(
    n_bins, n_samples=int(1e8), n_subsample=int(1e7))

n_subsamples = sample_indices.shape[0]
n_samples = binned_feature.shape[0]
print(f"Building feature histogram on {n_subsamples} values of {n_samples}")
tic = time()
Histogram(n_bins).build(sample_indices, binned_feature, gradients, hessians)
toc = time()
duration = toc - tic
print(f"Built in {duration:.3f}s")
