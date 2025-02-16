import base64
import io
import os

from IPython.display import Javascript
from plotly.offline import get_plotlyjs
Javascript(get_plotlyjs())

PATH_TO_NOTEBOOK = os.environ.get('PATH_TO_NOTEBOOK')
output_dir='/content'
os.system(f'jupyter nbconvert --output-dir={output_dir} --to html "{PATH_TO_NOTEBOOK}"')

notebook_filename = os.path.basename(PATH_TO_NOTEBOOK)  # Get filename from path
html_filename = os.path.splitext(notebook_filename)[0] + '.html'
pdf_filename = os.path.splitext(notebook_filename)[0] + '.pdf'
print(f"HTML filename: {html_filename}")
print(f"PDF filename: {pdf_filename}")

plotly_script = '<script charset="utf-8" src="https://cdn.plot.ly/plotly-2.35.2.min.js"></script>'
from bs4 import BeautifulSoup
with open('/content/'+html_filename, 'r') as f:
    soup = BeautifulSoup(f, 'html.parser')
title_tag = soup.find('title')
title_tag.insert_after(BeautifulSoup(plotly_script, 'html.parser'))

with open('/content/'+html_filename, 'w') as f:
    f.write(str(soup))

os.system('pip install playwright --quiet')
os.system('playwright install chromium')
os.system('pip install nest-asyncio --quiet')

import nest_asyncio
nest_asyncio.apply()

from playwright.async_api import async_playwright

import pathlib

fileUrl = pathlib.Path('/content/' + html_filename).as_uri()

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.emulate_media(media="print")
        await page.wait_for_timeout(100)
        await page.goto(fileUrl, wait_until="networkidle")
        await page.wait_for_timeout(60000)

        pdf_params = {"print_background": True}
        # Floating point precision errors cause the printed
        # PDF from spilling over a new page by a pixel fraction.
        dimensions = await page.evaluate(
            """() => {
            const rect = document.body.getBoundingClientRect();
            return {
            width: Math.ceil(rect.width) + 1,
            height: Math.ceil(rect.height) + 1,
            }
        }"""
        )
        # Convert width and height to strings with units
        pdf_params.update(
            {
                "width": f"{min(dimensions['width'], 200 * 72)}px",  # Add 'px' unit
                "height": f"{min(dimensions['height'], 200 * 72)}px", # Add 'px' unit
                "path":'/content/'+pdf_filename
            }
        )
        await page.pdf(**pdf_params)

        await browser.close()
        #await playwright.stop()

import asyncio
asyncio.get_event_loop().run_until_complete(main())

from google.colab import files

# Trigger the download
files.download(pdf_filename)
