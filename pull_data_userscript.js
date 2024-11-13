// ==UserScript==
// @name         Pull Soldier Data and Documents from iPERMS
// @namespace    
// @version      
// @description  Pull soldier data and documents from the fake iPERMS site
// @grant        
// ==/UserScript==

(function() {
    'use strict';

    function pullSoldierDataAndSave() {
        const soldiers = [];
        
        document.querySelectorAll('.soldier-card').forEach(card => {
            const soldierInfo = {
                name: card.querySelector('h2').innerText,
                rank: card.querySelector('p:nth-of-type(1)').innerText.split(': ')[1],
                unit: card.querySelector('p:nth-of-type(2)').innerText.split(': ')[1],
                serviceNumber: card.querySelector('p:nth-of-type(3)').innerText.split(': ')[1],
                documents: []
            };

            // Loop through each document for the soldier
            card.querySelectorAll('.download-button').forEach(doc => {
                const documentInfo = {
                    type: doc.closest('tr').querySelector('td:nth-of-type(1)').innerText,
                    issuedDate: doc.closest('tr').querySelector('td:nth-of-type(2)').innerText,
                    url: doc.href
                };
                soldierInfo.documents.push(documentInfo);

                // open it in a new tab?
                // window.open(doc.href, '_blank');
            });
            
            soldiers.push(soldierInfo);
        });

		saveAsCSV(soldiers);
        // Log the pulled data on console
        console.log("Pulled Soldier Data:", JSON.stringify(soldiers, null, 2));
    }

	// Function to save data as a CSV file
	function saveAsCSV(data) {
		let csv = "Name,Rank,Unit,Service Number,Document Type,Document Issued Date,Document URL\n";
	
		data.forEach(soldier => {
			soldier.documents.forEach(doc => {
				csv += `"${soldier.name}","${soldier.rank}","${soldier.unit}","${soldier.serviceNumber}","${doc.type}","${doc.issuedDate}","${doc.url}"\n`;
			});
		});
	
		const blob = new Blob([csv], { type: "text/csv" });
		const link = document.createElement("a");
		link.href = URL.createObjectURL(blob);
		link.download = "pulled_soldier_data.csv";
		link.click();
	}
	
	pullSoldierDataAndSave();
})();