To run, paste the following code into a new code cell at the bottom of your Colab notebook:
```python
# TODO: change notebook_path to the location of this Colab notebook in your Google Drive
notebook_path = "/content/drive/MyDrive/Colab Notebooks/hw3.ipynb"

!wget -q -O colab_to_pdf.py https://raw.githubusercontent.com/mirapartha/colab_to_pdf/refs/heads/main/colab_to_pdf.py

with open('/content/colab_to_pdf.py', 'r') as f:
    exec(f.read(), globals(), locals())
```
Make sure to change `notebook_path` to reflect the location of your Colab notebook in your Google Drive. This script will both create the PDF and initiate its download from Colab.
