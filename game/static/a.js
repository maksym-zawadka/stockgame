document.addEventListener("DOMContentLoaded", function () {
    const listaElement = document.getElementById("myUL");

    fetch("fullname")
$.ajax({
                                url: '/fullname/',
                                dataType: 'json',
                                success: function (data) {
                                    var datalist = $('#myUL');
                                    datalist.empty();

                                    data.forEach(function (dopasowanie) {
                                        datalist.append('<li>' + dopasowanie + '</li>');
                                    });
                                }
                            });
});


