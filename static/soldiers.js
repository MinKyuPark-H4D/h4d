function displaySoldiers(soldiers) {
    $("#soldier-items").empty();
    var row; // To group cards into rows of two
    console.log(soldiers.length);
    $.each(soldiers, function(key, value) {
        console.log(typeof key);
        
        // Every two cards, create a new row
        if (key % 2 === 1) {
            row = $("<div class='row'>");
        }

        var new_col = $("<div class='col-6 mb-4 align-items-center'>");
        var link = $("<a>").attr("href", "/soldiers/" + value.id).addClass("card-link");

        var new_card = $("<div class='card soldier-card h-100'>");
        var new_card_body = $("<div class='card-body'>");
        
        var new_title = $("<h5 class='card-title'>").text(value.first_name + " " + value.last_name);
        new_card_body.append(new_title);
        var new_rank = $("<p class='card-text'>").html("<strong>Rank:</strong> " + value.rank);
        var new_unit = $("<p class='card-text'>").html("<strong>Unit:</strong> " + value.UIC); // You can use UIC or another field as unit
        var new_email = $("<p class='card-text'>").html("<strong>Email:</strong> " + value.email);
        var soldier_info_div = $("<div class='soldier-info'>");

        soldier_info_div.append(new_rank, new_unit, new_email);
        new_card_body.append(soldier_info_div);

        var viewProfileButton = $("<button>").addClass("btn custom-btn").text("View Profile");
        new_card_body.append(viewProfileButton);
        
        new_card.append(new_card_body);
        link.append(new_card);
        new_col.append(link);
        row.append(new_col);

        // Every two cards, append the row to the container
        if (key % 2 === 0 || parseInt(key) === Object.keys(soldiers).length) {
            $('#soldier-items').append(row);
        }
    });
}




$(document).ready(function(){
    //when the page loads, display top 3 data structures
    displaySoldiers(soldiers)                        

    

})