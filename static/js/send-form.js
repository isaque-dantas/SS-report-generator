const form = document.querySelector('form')

form.addEventListener(
    'submit',
    () => {
        const formData = new FormData(form)
        sendFormDataTo(formData, form.action)
    }
)

function appendFileToFormData(form, formData) {
    const fileInput = form.querySelector('input[type="file"]')
    formData.append('image_file', fileInput.files[0])
    return formData
}

async function sendFormDataTo(formData, url) {
    formData = appendFileToFormData(form, formData)
    formData.enctype = 'multipart/form-data'
    formData.method = 'post'

    const response = await fetch(url, {
        method: 'POST',
        headers: {
            "Content-Type": "multipart/form-data",
        },
        body: formData
    })

    if (!response.ok) {
        console.error(response.statusText)
    }
}
