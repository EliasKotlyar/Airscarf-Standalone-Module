// Activate Tabs:
window.activeProfile = null;
$('.activateTab').on('click', function() {
  var mode = $(this).data('id');
  getConfigFromBackend(mode);

  $('.activateTab').removeClass('active');
  $('.tab').removeClass('active');
  $("#"+mode).addClass('active');
  $(".activateTab[data-id='"+mode+"']").addClass('active');
  window.activeProfile = mode
});
$(".activateTab[data-id=\"profiles\"]").trigger('click')

// Activate Current Profile:
$('#current_profile').on('change', function() {
  var profile = $(this).val()
  $('.stage-button').removeClass('active');
  $(".stage-button[data-id='"+profile+"']").addClass('active');
});
$('.stage-button').on('click', function() {
    var profile = $(this).data('id');
    const json = JSON.stringify({"current_profile" : profile});
    var url = '/api/current_profile/setData';

    $.ajax(url, {
        data: json,
        contentType: 'application/json',
        type: 'POST',
    }).done(function() {

    }).fail(function (jqXHR, textStatus){
        alert("There was a problem with saving settings: "+ textStatus)
    });
})
// Current Profile
setInterval(function() {
    var profile = window.activeProfile;
    console.log(profile);
    switch(profile){
        case 'profiles':
            getConfigFromBackend("current_profile");
        break;
        case 'monitor':
            getConfigFromBackend("monitor");
        break;
    }
}, 1000);

