$.getJSON('api/wifi.json', function(data) {
  $.each(data, function(itemName, value) {
    var inputElement = $('#' + itemName);
    setElement(inputElement, value);
  });
});


$('#save_wifi').on('click', function(){
  var elements = {};
  $('.wifi_data').each(function(index) {
    var inputElement = $(this);
    var name = inputElement.data('id');
    elements[name] = inputElement.val();
  });
  const json = JSON.stringify(elements);
  $.ajax('api/setWifi', {
    data: json,
    contentType: 'application/json',
    type: 'POST',
  }).done(function() {
        alert("Settings saved!")
  }).fail(function (jqXHR, textStatus){
        alert("There was a problem with saving settings: "+ textStatus)
  });
});
