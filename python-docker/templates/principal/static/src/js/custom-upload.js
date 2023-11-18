document.querySelector('form').addEventListener('submit', (e) => {
    e.preventDefault();
    const form = e.currentTarget;
    const data = new FormData(form);
    const queryString = new URLSearchParams(data).toString();
    form.action = "/editar-registro/registro/" + queryString;
});