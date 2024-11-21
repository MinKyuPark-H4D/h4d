function displaySoldiers(soldiers) {
    $("#soldier-items").empty();
    var row; // To group cards into rows of two

    $.each(soldiers.soldiers, function(key, value) {
        // Every two cards, create a new row
        if (key % 2 === 0) {
            row = $("<div class='row'>");  
        }

        var new_col = $("<div class='col-6 mb-4'>"); 
        var new_card = $("<div class='card h-100'>");
        var new_card_body = $("<div class='card-body'>");
        
        var new_title = $("<h5 class='card-title'>").text(value.first_name + " " + value.last_name);
        new_card_body.append(new_title);
        var new_rank = $("<p class='card-text'>").html("<strong>Rank:</strong> " + value.rank);
        var new_unit = $("<p class='card-text'>").html("<strong>Unit:</strong> " + value.UIC); // You can use UIC or another field as unit
        var new_email = $("<p class='card-text'>").html("<strong>Email:</strong> " + value.email);
        var soldier_info_div = $("<div class='soldier-info'>");

        // Append the rank, unit, and email to the div
        soldier_info_div.append(new_rank, new_unit, new_email);
        new_card_body.append(soldier_info_div);
        var link = $("<a>").attr("href", "/view/soldier/" + value.id).addClass("btn custom-btn").text("View Profile");
        new_card_body.append(link);
        new_card.append(new_card_body);
        new_col.append(new_card);
        row.append(new_col);
        // Every two cards, append the row to the container
        if (key % 2 === 1 || key === soldiers.soldiers.length - 1) {
            $('#soldier-items').append(row);
        }
    });
}




$(document).ready(function(){
    //when the page loads, display top 3 data structures
    displaySoldiers(soldiers)                        

    

})