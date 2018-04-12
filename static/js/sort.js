/* stores the ordered state of columns */
var asc1=1;
var asc2=1;
var asc3=1;
var asc4=1;
var asc5=1;
var asc6=1;
var asc7=1;
var asc8=1;
        
function sort_table(tbody, col, asc) {
            var rows = tbody.rows,
                rlen = rows.length;
            
            var swapped;
            do {
                swapped = false;
                for (var i=0; i < rlen-1; i++) {
                    if (asc==1){
                            if (rows[i].cells[col].textContent > rows[i+1].cells[col].textContent) { //ascending order
                                tbody.insertBefore(rows[i+1], rows[i]);
                                swapped = true;
                            }
                    }if (asc==-1){
                            if (rows[i].cells[col].textContent < rows[i+1].cells[col].textContent) { //descending order
                                tbody.insertBefore(rows[i+1], rows[i]);
                                swapped = true;
                            }
                    }
                }
            } while (swapped);
}