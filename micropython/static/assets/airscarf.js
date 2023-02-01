$('.changeable_data').change(function() {

  var elements = {};
  $('.changeable_data').each(function(index) {
    var inputElement = $(this);
    var name = inputElement.attr('id');
    var value = inputElement.val();
    elements[name] = value;
  });
  console.log(elements);
  $.ajax('api/setData', {
    data: JSON.stringify(elements),
    contentType: 'application/json',
    type: 'POST',
  }, function() {

  });

});

setInterval(function() {
  $.getJSON('api/data.json', function(data) {
    console.log(data);
    $('.data_from_backend').each(function(index) {

      var inputElement = $(this);
      console.log(inputElement);
      var name = inputElement.data('id');
      var value = data[name];
      if (inputElement.is('input')) {
        inputElement.val(value);
      } else if (inputElement.is('span')) {
        inputElement.html(value);
      } else if (inputElement.is('select')) {
        inputElement.val(value).change();
      }

    });

  });
}, 1000);
