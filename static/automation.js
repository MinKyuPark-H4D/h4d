function toggleSelection() {
    var selectionType = document.getElementById('selectionType').value;

    // Show/hide the unit or soldier selection based on the choice
    if (selectionType === 'unit') {
        document.getElementById('unitSelectDiv').style.display = 'block';
        document.getElementById('soldierSelectDiv').style.display = 'none';
    } else if (selectionType === 'soldier') {
        document.getElementById('unitSelectDiv').style.display = 'none';
        document.getElementById('soldierSelectDiv').style.display = 'block';
    }
}