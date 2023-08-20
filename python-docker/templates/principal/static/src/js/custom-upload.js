document.addEventListener('DOMContentLoaded', function() {
    const fileInput = document.getElementById('fileInput');
    const saveButton = document.getElementById('salveButton');
    const selectedFiles = document.getElementById('selectedFiles')


    saveButton.addEventListener('click', function() {
        // Obter os valores dos campos
        const coordenandaX = document.querySelector('input[name="coordenanda_x"]').value;
        const coordenandaY = document.querySelector('input[name="coordenanda_y"]').value;

        // Fazer algo com os valores (por exemplo, enviar para um servidor)
        console.log('Coordenadas X:', coordenandaX);
        console.log('Coordenadas Y:', coordenandaY);
    });
});