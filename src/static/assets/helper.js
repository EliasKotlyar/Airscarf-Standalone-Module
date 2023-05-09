function flattenObj(obj, parent, res = {}) {
  for (let key in obj) {
    let propName = parent ? parent + '-' + key : key;
    if (typeof obj[key] == 'object') {
      flattenObj(obj[key], propName, res);
    } else {
      res[propName] = obj[key];
    }
  }
  return res;
}

let unflattenObject = (data) => {
  let result = {};
  for (let i in data) {
    let keys = i.split('-');
    keys.reduce((acc, value, index) => {
      return (
          acc[value] ||
          (acc[value] = isNaN(Number(keys[index + 1]))
              ? keys.length - 1 === index
                  ? data[i]
                  : {}
              : [])
      );
    }, result);
  }
  return result;
};

function setElement(inputElement, value) {
  if (inputElement.is('input')) {
    inputElement.val(value).trigger('change');
  } else if (inputElement.is('span')) {
    inputElement.html(value);
  } else if (inputElement.is('select')) {
    inputElement.val(value).change();
  }
}

function getConfigFromBackend(configName) {
  var url = '/api/' + configName + '/data.json';
  $.getJSON(url, function(data) {
    $.each(data, function(itemName, value) {
      var inputElement = $('#' + itemName);
      setElement(inputElement, value);
    });
  });

}


$('.saveButton').on('click', function(){
  var configName = $(this).data('id');
  var elements = {};
  searchQuery = "#"+configName+" .changeable-value";
  $(searchQuery).each(function(index) {
    var inputElement = $(this);
    var name = inputElement.attr('id');
    elements[name] = inputElement.val();
  });
  const json = JSON.stringify(elements);
  var url = '/api/' + configName + '/setData';

  $.ajax(url, {
    data: json,
    contentType: 'application/json',
    type: 'POST',
  }).done(function() {
        alert("Settings saved!")
  }).fail(function (jqXHR, textStatus){
        alert("There was a problem with saving settings: "+ textStatus)
  });
});