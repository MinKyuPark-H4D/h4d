
$(document).ready(function(){
         
    // Reveal Soldier SSN
// Reveal Soldier SSN
document.getElementById('reveal-ssn').addEventListener('click', function() {
    var ssnSpan = document.getElementById('ssn');
    var icon = this.querySelector('img');  // Get the image inside the button
    
    // Get the actual SSN from the data attribute
    var ssn = this.getAttribute('data-ssn');
    
    // Check if the SSN is currently hidden
    if (ssnSpan.innerText === '****-**-****') {
        // Show the actual SSN
        ssnSpan.innerText = ssn;  // Display the SSN
        icon.src = 'https://cdns.iconmonstr.com/wp-content/releases/preview/2017/240/iconmonstr-eye-9.png';  // Change image to eye-slash (hide SSN)
        icon.alt = 'Hide SSN';  // Change alt text
    } else {
        // Hide the SSN again
        ssnSpan.innerText = '****-**-****';  // Hide the SSN again
        icon.src = 'https://www.kindpng.com/picc/m/327-3273865_password-eye-icon-png-transparent-png.png';  // Change image back to eye (reveal SSN)
        icon.alt = 'Reveal SSN';  // Change alt text
    }
});

// Reveal Spouse SSN
document.getElementById('reveal-spouse-ssn').addEventListener('click', function() {
    var spouseSsnSpan = document.getElementById('spouse-ssn');
    var icon = this.querySelector('img');  // Get the image inside the button
    
    // Get the actual Spouse SSN from the data attribute
    var spouseSsn = this.getAttribute('data-spouse-ssn');
    
    // Check if the Spouse SSN is currently hidden
    if (spouseSsnSpan.innerText === '****-**-****') {
        // Show the actual Spouse SSN
        spouseSsnSpan.innerText = spouseSsn;  // Display the Spouse SSN
        icon.src = 'https://cdns.iconmonstr.com/wp-content/releases/preview/2017/240/iconmonstr-eye-9.png';  // Change image to eye-slash (hide SSN)
        icon.alt = 'Hide Spouse SSN';  // Change alt text
    } else {
        // Hide the Spouse SSN again
        spouseSsnSpan.innerText = '****-**-****';  // Hide the Spouse SSN again
        icon.src = 'https://www.kindpng.com/picc/m/327-3273865_password-eye-icon-png-transparent-png.png';  // Change image back to eye (reveal SSN)
        icon.alt = 'Reveal Spouse SSN';  // Change alt text
    }
});

    

    

})