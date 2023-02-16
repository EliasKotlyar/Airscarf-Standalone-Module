setInterval(function() {
  $.getJSON('api/livedata.json', function(data) {

    $('.livedata').each(function(index) {
      var inputElement = $(this);
      var name = inputElement.data('id');
      var value = data[name];
      setElement(inputElement, value);
    });
  });

}, 1000);
