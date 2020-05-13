function loadFile(o) {
    var fr = new FileReader();
    fr.onload = function (e) {
      showDataFile(e, o);
    };
    fr.readAsText(o.files[0]);
  }

  function showDataFile(e, o) {
    
    var getCSVData = e.target.result;
    var rows = getCSVData.split("\n");
    // var col = document.getElementById('demo').rows[0].cells.length
    // var col  = getCSVData.split(",");
    rows.length = (rows.length - 1);
    // col = rows[1].cells.length;
    
    var html = '<table class="container table table-bordered table-striped table-hover"  <b> <thead> <tr> <th>Age</th> <th>BusinessTravel</th> <th>Department</th> <th>DistanceFromHome</th> <th>Education</th> <th>EducationField</th> <th>Gender</th> <th>JobInvolvement</th> <th>JobLevel</th> <th>JobRole</th> <th>JobSatisfaction</th> <th>MonthlyIncome</th> <th>MonthlyRate</th> <th>OverTime</th> <th>PercentSalaryHike</th> <th>PerformanceRating</th> <th>TotalWorkingYears</th> <th>YearsAtCompany</th> <th>YearsInCurrentRole</th> <th>YearsSinceLastPromotion</th> <th>YearsWithCurrManager</th> <th>Attrition</th> </tr> </thead>';
    
    
      rows.forEach((data, index) => {
        html += "<tr>";
        var value = data.split(",");
        var i;

        for (i = 0; i < 22 ; i++) {
          html += "<td>" + value[i] + "</td>";
        }

        html += "</tr>";

      });
      html += '</table>';
      document.getElementById("data").innerHTML = html;
      document.getElementById("data").style.color = "blue";
      document.getElementById("demo").innerHTML = (rows.length);
   
  }