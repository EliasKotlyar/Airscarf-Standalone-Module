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
    inputElement.val(value);
  } else if (inputElement.is('span')) {
    inputElement.html(value);
  } else if (inputElement.is('select')) {
    inputElement.val(value).change();
  }
}
