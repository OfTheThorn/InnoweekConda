# Installation:
## Linux: (requires 64-bit Python 3.5 - 3.8)
```
conda create --name innoweekconda
conda activate innoweekconda
pip install numpy pandas matplotlib plotly django pystan fbprophet
```

## Windows: (requires 64-bit Python + Conda 3.5 - 3.8)
```
conda create --name innoweekconda
conda activate innoweekconda
pip install numpy pandas matplotlib plotly django
conda install libpython m2w64-toolchain -c msys2
pip install pystan fbprophet
```