$.get('profile.html', function(jsonData) {
  for (i = 1; i <= 3; i++) {
    var data = jsonData;
    const profileStr = 'profile' + i + '-';
    data = data.replaceAll('Profile', 'Profile ' + i);
    data = data.replaceAll('profile', 'profile' + i);
    data = data.replaceAll('rpm_duty', profileStr + 'rpm_duty');
    data = data.replaceAll('rpm_freq', profileStr + 'rpm_freq');
    data = data.replaceAll('heater_duty', profileStr + 'heater_duty');
    data = data.replaceAll('heater_freq', profileStr + 'heater_freq');
    $('#profiles').append(data);
  }
  $.getJSON('api/profiles.json', function(data) {

    data = flattenObj(data);
    //console.log(data);
    $.each(data, function(itemName, value) {
      var inputElement = $('#' + itemName);
      setElement(inputElement, value);
      var rangeElement = $('#' + itemName + '_range');
      setElement(rangeElement, value);
    });
    //console.log(data)
    selectProfile(data['current_profile']);
  });
});

function selectProfile(profileNumber) {
  for (i = 1; i <= 3; i++) {
    $('#profile' + i).removeClass('selected-profile');
  }
  $('#profile' + profileNumber).addClass('selected-profile');
}

$('#current_profile').on('change', function() {
  selectProfile($(this).val());
});
$('.change-profile').on('click', function() {
  $('#current_profile').val($(this).data('id')).change().trigger( "input" );
});

var body = $('body');
body.on('input', '.config_data', function() {

  var elements = {};
  $('.config_data').each(function(index) {
    var inputElement = $(this);
    var name = inputElement.data('id');
    elements[name] = inputElement.val();
  });

  elements = unflattenObject(elements);
  console.log(elements);
  const json = JSON.stringify(elements);

  //console.log(elements);
  $.ajax('api/setProfiles', {
    data: json,
    contentType: 'application/json',
    type: 'POST',
  }).always(function() {

  });
});

body.on('change', '.changeable_range', function() {
  var inputElement = $(this);
  var name = inputElement.data('id');
  $('#' + name).val(inputElement.val()).trigger('input');
});




