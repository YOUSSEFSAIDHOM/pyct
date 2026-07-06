
# PyCT 🧬 (v0.1.0)

### About 💭

PyCT is a python wrapper for the ClinicalTrials.org API (v2). Although a python-wrapper already exists for this API, it doesn't feature full pagination support, thus is unable to give you all the studies that match the search-terms. Moreover, PyCT enables you to search with more accuracy by specifying the conditions and the interventions separately

### Basic usage 🪛
Get started with:
```python
from pyct import ClinicalTrials

ct = ClinicalTrials()
```

Checking API info:

```python
print(ct)
```
Fetching studies:

```python

# Specify each field

df = ct.get_studies(
    condition="Dementia",
    intervention="Non-pharmacological",
    status="RECRUITING"
)

# Alternatively you can get one specific study using the NCT number
study = ct.get_study("NCT06210035")

```
and finally you can export with the following options below:

```python
ct.to_csv(df, "alzheimer_trials.csv") # CSV

ct.to_excel(df, "alzheimer_trials.xlsx") # Excel

ct.to_json(df, "alzheimer_trials.json") # JSON
```
It will automatically give a name if you don't specify
### Installation 📦

```
pip install pyct
```
