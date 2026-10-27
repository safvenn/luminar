# Titanic Survival Lab

A Streamlit app built from the notebook workflow. It trains a K-nearest-neighbors classifier with imputation, scaling, and categorical encoding, then provides an interactive passenger prediction form.

## Run locally

```powershell
python -m pip install -r requirements.txt
streamlit run app.py
```

The app uses seaborn's built-in Titanic dataset by default. Upload a CSV or Excel file with a `Survived` column to use another dataset. Common Titanic column names such as `sex`, `age`, `pclass`, and `fare` are normalized automatically.