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

function toggleSelection2() {
    var selectionType = document.getElementById('selectionType2').value;

    // Show/hide the unit or soldier selection based on the choice
    if (selectionType === 'unit') {
        document.getElementById('unitSelectDiv2').style.display = 'block';
        document.getElementById('soldierSelectDiv2').style.display = 'none';
    } else if (selectionType === 'soldier') {
        document.getElementById('unitSelectDiv2').style.display = 'none';
        document.getElementById('soldierSelectDiv2').style.display = 'block';
    }
}
$(document).ready(function(){
    //when the page loads, display top 3 data structures
    document.getElementById('scheduleToggle').addEventListener('change', function() {
        var scheduledTimeDiv = document.getElementById('scheduledTimeDiv');
        if (this.checked) {
            scheduledTimeDiv.style.display = 'block'; // Show scheduled time field
        } else {
            scheduledTimeDiv.style.display = 'none'; // Hide scheduled time field
        }
    });                      

    

})
