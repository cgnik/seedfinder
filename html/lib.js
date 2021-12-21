function submitForm(e) {
    e.preventDefault();
    form = e.target
    p = new URLSearchParams()
    for (const i of new FormData(form)) {
        p.append(i[0], i[1])
    }
    $('#response').html('<p>Searching...</p>');
    fetch(form.action, {'method': 'post', body: p})
        .then(r => r.json())
        .then(r => $('#response').html(r))
        .catch(console.error)
    return false;
}

$(document).ready(() => {
    $('#searchForm').on('submit', submitForm);
});