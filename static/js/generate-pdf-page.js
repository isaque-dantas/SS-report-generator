const btnGeneratePDF = document.querySelector('button#generate-pdf-page')

const options = {
    margin: 0,
    filename: 'presentes.pdf',
    html2canvas: {scale: 2},
    jsPDF:
        {
            orientation: 'l',
            unit: 'px',
            image: {type: 'png', quality: 0.9},
            format: [1024, 768],
            putOnlyUsedFonts: true,
            floatPrecision: 16
        }
}

btnGeneratePDF.addEventListener('click', () => {
        const content = document.querySelector('#content')
        html2pdf().set(options).from(content).save()
    }
)
