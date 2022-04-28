const fs = require('fs');

fs.writeFile("tmp.txt", "Hey there!", function(err) {
    if(err) {
        return console.log(err);
    }
}); 
