# Level Planarity Test by Harrigan & Healy

[This](./HarriganHealy.ipynb) is an [ogdf-python](https://github.com/ogdf/ogdf-python) implementation of the quadratic-time Level Planarity test and embedder by Harrigan and Healy.

> Harrigan, M., Healy, P. (2008). Practical Level Planarity Testing and Layout with Embedding Constraints. In: Hong, SH., Nishizeki, T., Quan, W. (eds) Graph Drawing. GD 2007. Lecture Notes in Computer Science, vol 4875. Springer, Berlin, Heidelberg. https://doi.org/10.1007/978-3-540-77537-9_9

Unfortunately, the embedding algorithm fails to produce a planar layout for the instance that is loaded as default.
You can open an interactive online version of this notebook by clicking [here](https://mybinder.org/v2/gh/N-Coder/HarriganHealy/HEAD?labpath=HarriganHealy.ipynb) or by running the following on your own computer (please use the WSL on Windows):

```bash
pip install ogdf-python[quickstart]
jupyter lab
```
