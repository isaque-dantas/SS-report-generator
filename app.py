from flask import Flask, render_template, redirect, url_for
from pyhtml2pdf import converter

app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/convert/<int:slide_id>')
def convert_to_pdf(slide_id):
    converter.convert(
        f'http://127.0.0.1:5000/slide/{slide_id}',
        fr'generated-pdfs/slide-{slide_id}.pdf',
        print_options={'scale': 1}
    )

    return redirect(url_for('index'))


@app.route('/slide/<int:slide_id>')
def slide(slide_id):
    return render_template('presentation-slide.html')


if __name__ == '__main__':
    app.run()
