function deleteRecord(recordId) {
    fetch('/delete-record', {
        method: 'POST',
        body: JSON.stringify({ recordId: recordId }),
    }).then((_res) => {
        window.location.href = '/home';
    });
}