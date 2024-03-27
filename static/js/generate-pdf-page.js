document.addEventListener('DOMContentLoaded', () => {
        header_content = document.querySelector('#header').textContent

        const options = {
            margin: 0,
            filename: `slide-${header_content.toLowerCase()}.pdf`,
            html2canvas: {scale: 1},
            jsPDF:
                {
                    orientation: 'l',
                    unit: 'px',
                    image: {type: 'png', quality: 0.95},
                    format: [1024, 768],
                    putOnlyUsedFonts: true,
                    floatPrecision: 16
                }
        }

        const content = document.querySelector('#content')
        // html2pdf().set(options).from(content).save()
    }
)
