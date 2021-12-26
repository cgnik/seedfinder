async function matchHtml(j) {
    return '<p>Results</p><table class="result-table"><thead><tr><th>Laces Student</th><th>GED subject</th></tr></thead><tbody>' +
        Object.keys(j).map(k => `<tr><td>${k}</td><td>${j[k]}</td></tr>`).join('') +
        '</tbody></table>';
}

function submitForm(e) {
    e.preventDefault();
    form = e.target;
    formData = new FormData(form);
    inputs = $('#searchForm :input');
    $('#response').html('<p>Searching...</p>');
    inputs.prop('disabled', true);
    fetch(form.attributes['action'].value, {'method': 'post', 'body': formData})
        .then(r => r.json())
        .then(matchHtml)
        .then(r => $('#response').html(r))
        .catch(console.error)
        .finally(() => inputs.prop('disabled', false));
    return false;
}

$(document).ready(() => $('#searchForm').on('submit', submitForm));