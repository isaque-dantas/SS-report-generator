import os

from flask import Flask, render_template, redirect, url_for, request, flash, send_from_directory
from werkzeug.utils import secure_filename

import json
import pandas as pd

from bs4 import BeautifulSoup
from pyhtml2pdf import converter
from pypdf import PdfMerger
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'batat docde xf 123jhf1jd0-9kjbmckxjok'

df = pd.DataFrame()
presentation_config = json.loads(open('presentation-config.json', 'r', encoding='latin-1').read())


def html_report_to_pandas_df(report_filename):
    with open(report_filename, mode='r', encoding="latin-1") as file:
        text = file.read()
    text = remove_trash(text)

    edited_report_filename = report_filename.replace('.html', '') + '-edited.html'

    with open(edited_report_filename, mode='w', encoding="latin-1") as file:
        file.write(text)

    return parse_html_data(edited_report_filename)


def remove_trash(text):
    text = text[text[6:].find('<table') + 6:]
    text = text.replace('\'', '\"')
    text = text.replace('table >', 'table>').replace('</table><table>', '')
    text = text.replace('<td align=\"center\">', '<td>')
    text = text.replace('<tr style=\"color: red;\">', '<tr>')
    return text


def parse_html_data(html_report_filename):
    data = []

    list_header = []
    soup = BeautifulSoup(open(html_report_filename, encoding='latin-1'), 'html.parser')
    header = soup.find_all("table")[0].find("tr")

    for items in header:
        try:
            list_header.append(items.get_text())
        except Exception:
            continue

    html_data = soup.find_all("table")[0].find_all("tr")[1:]

    for element in html_data:
        sub_data = []
        for sub_element in element:
            try:
                if sub_element.get_text() != ' ':
                    sub_data.append(sub_element.get_text())
            except Exception:
                continue
        data.append(sub_data)

    return pd.DataFrame(data=data, columns=list_header)


def merge_slides():
    filenames = os.listdir('generated-pdfs/')
    pdfs = []
    for i, filename in enumerate(filenames):
        if filename.endswith('.pdf') and 'slide' in filename:
            pdfs.append(filename)

    merger = PdfMerger()

    for pdf in pdfs:
        merger.append('generated-pdfs/' + pdf)

    merger.write(f"generated-pdfs/relatorio-{datetime.now().strftime('%d-%m-%y_%H-%M-%S')}.pdf")
    merger.close()


def exclude_slides():
    filenames = os.listdir('generated-pdfs/')
    for i, filename in enumerate(filenames):
        if filename.endswith('.pdf') and 'slide' in filename:
            os.remove('generated-pdfs/' + filename)


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        report = request.files['report']
        report.save(os.path.join('reports', report.filename))
        report.close()

        global df
        df = html_report_to_pandas_df(os.path.join('reports', report.filename))

        return redirect(url_for('generate_pdfs', current_slide=0))

    reports = []
    filenames = os.listdir('generated-pdfs')
    for filename in filenames:
        if filename.endswith('.pdf') and 'relatorio' in filename:
            reports.append(filename)

    return render_template('index.html', reports=reports)


@app.route('/download/<report>')
def download_report(report):
    return send_from_directory('generated-pdfs', secure_filename(report))


@app.route('/generate_all/<int:current_slide>')
def generate_pdfs(current_slide):
    global presentation_config
    if current_slide >= len(presentation_config):
        flash('Slide gerado com sucesso.')
        merge_slides()
        exclude_slides()
        return redirect(url_for('index'))
    else:
        return redirect(url_for('generate_pdf', slide_id=current_slide))


@app.route('/generate/<int:slide_id>')
def generate_pdf(slide_id):
    converter.convert(
        f'http://127.0.0.1:5000/slide/{slide_id}',
        fr'generated-pdfs/slide-{slide_id}.pdf',
        print_options={'scale': 1}
    )

    return redirect(url_for('generate_pdfs', current_slide=slide_id + 1))


@app.route('/slide/<int:slide_id>')
def slide(slide_id):
    global df
    global presentation_config

    if slide_id >= len(presentation_config):
        return redirect('index')

    current_slide_config = presentation_config[slide_id]

    header = current_slide_config['header']

    rows = []
    for row_config in current_slide_config['body']:
        if "value" in row_config:
            row_data = df.loc[row_config['value']['index'], row_config['value']['column']]
        elif 'max_column' in row_config and 'target' in row_config:
            copied_df = df.copy()
            copied_df = copied_df.drop(copied_df.index[10])
            index_of_max_value_row = copied_df.idxmax()[row_config['max_column']]
            row_data = copied_df.loc[index_of_max_value_row, row_config['target']]

        rows.append({
            'label': row_config['label'],
            'data': row_data
        })

    return render_template('presentation-slide.html', header=header, rows=rows)


if __name__ == '__main__':
    app.run()
