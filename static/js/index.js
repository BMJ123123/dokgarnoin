const delete_note = (note_id) => {
    let send = { note_id };
    let option = confirm('삭제하시겠습니까?');
    if (!option) return;

    fetch(`/notes/delete`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(send)
    })
        .then((res) => {
            return res.json();
        })
        .then((data) => {
            if (data.ok) {
                alert('Note deleted successfully');
                location.reload();
            }
            else {
                throw new Error(data.error_code);
            }
        }).catch((e) => {
            alert('Note cannot be deleted: ' + e.toString());
        });
};