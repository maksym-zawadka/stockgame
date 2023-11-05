document.addEventListener("DOMContentLoaded", function () {
    const listaElement = document.getElementById("myUL");

    fetch("fullname")
        .then(response => response.text())
        .then(data => {
            try {
                const jsonArray = JSON.parse(data);
                jsonArray.forEach(item => {
                    const li = document.createElement("li");
                    li.textContent = item;
			li.classList.add("myli");
                    listaElement.appendChild(li);
                });
            } catch (error) {
                console.error("Błąd podczas przetwarzania danych JSON:", error);
            }
        })
        .catch(error => {
            console.error("Błąd podczas wczytywania pliku:", error);
        });
});

function myFunction() {
  // Declare variables
  var input, filter, ul, li, a, i, txtValue;
  input = document.getElementById('myInput');
  filter = input.value.toUpperCase();
  ul = document.getElementById("myUL");
  li = ul.getElementsByTagName('li');

  // Loop through all list items, and hide those who don't match the search query
  for (i = 0; i < li.length; i++) {
    a = li[i];
    txtValue = a.textContent || a.innerText;
    if (txtValue.toUpperCase().indexOf(filter) > -1) {
      li[i].style.display = "";
    } else {
      li[i].style.display = "none";
    }
  }
}