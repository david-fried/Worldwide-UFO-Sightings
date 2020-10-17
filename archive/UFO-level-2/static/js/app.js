tbody = d3.select("tbody");

function createTable(data) {
    data.forEach((obj) => {
        var row = tbody.append("tr");
        Object.values(obj).forEach((value) => {
          var cell = row.append("td");
          cell.text(value);
        });
      });   
}

createTable(data);

var button = d3.select("#filter-btn");

// Select the form
var form = d3.select(".filters");

// Create event handlers 
button.on("click", runEnter);
form.on("submit", runEnter);


// Complete the event handler function for the form
function runEnter() {

    // remove previous data from the list to
    tbody.html("");

    // Prevent the page from refreshing
    d3.event.preventDefault();

    // Get the value property of the input element
    var inputDate = d3.select("#datetime").property("value");

    var inputState= d3.select("#state").property("value").toLowerCase();

    var inputCity= d3.select("#city").property("value").toLowerCase();

    var inputCountry= d3.select("#country").property("value").toLowerCase();

    var inputShape= d3.select("#shape").property("value").toLowerCase();

    filteredData = data;

    if (inputDate !== "") {
      var filteredData = filteredData.filter(obj=>obj.datetime === inputDate);
    }

    if (inputState !== "") {
      var filteredData = filteredData.filter(obj=>obj.state === inputState);
    }

    if (inputCity !== "") {
      var filteredData = filteredData.filter(obj=>obj.city === inputCity);
    }
    
    if (inputCountry !== "") {
      var filteredData = filteredData.filter(obj=>obj.country === inputCountry);
    }

    if (inputShape !== "") {
      var filteredData = filteredData.filter(obj=>obj.shape === inputShape);
    }
    
    createTable(filteredData);
}