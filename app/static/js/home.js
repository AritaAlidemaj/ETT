var uploadDznButton = document.querySelector("#upload-dzn");
var uploadDznButtonInput = document.querySelector("#upload-dzn input");
var uploadDznButtonLoading = document.querySelector("#upload-loading");
var dataTable = document.querySelector("#data");
var dataTableBody = document.querySelector("#data tbody");
var pdfButton = document.querySelector('#pdfBtn')

uploadDznButtonInput.onchange = () => {

    hideTable();
    hideButton();
    const formData = new FormData();
    formData.append("dznFile", uploadDznButtonInput.files[0])

    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/upload', true);
    xhr.onload = function () {
        showTable();
        showButton();
        populateTable(JSON.parse(this.response));

        uploadDznButtonLoading.style.display = "none";
        uploadDznButton.style.display = "inline-block";
    };
    xhr.send(formData);

    uploadDznButtonLoading.style.display = "inline-block";
    uploadDznButtonInput.value = "";

    uploadDznButton.style.display = "none";
}
hideTable = () => {
    dataTable.classList.add("d-none");
    dataTableBody.innerHTML = "";
}
hideButton = () => {
    pdfButton.classList.add("d-none");
}
showTable = () => {
    dataTable.classList.remove("d-none");
}
showButton = () => {
    pdfButton.classList.remove("d-none");
}
populateTable = (data) => {
    dataTableBody.innerHTML = '';
    var rows = data.data;
    for (var i = 0; i < rows.length; i++) {
        var row = rows[i];

        var tableRow = dataTableBody.insertRow(i);
        var exam = tableRow.insertCell(0);
        var teachers = tableRow.insertCell(1);
        var period = tableRow.insertCell(2);
        var room = tableRow.insertCell(3);

        exam.innerHTML = row.Exam;
        teachers.innerHTML = row.Teachers.map((e) => " " + e.Name);
        period.innerHTML = row.Periods;
        room.innerHTML = row.Room;
    }
    console.log(data)
    return true;
}

function generatePDF() {
    var doc = new jsPDF();
    doc.autoTable({
        html: '#data'
    })
    doc.save('ETT.pdf');
}


