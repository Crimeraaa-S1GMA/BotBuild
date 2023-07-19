var myDiv = document.getElementById('sidebar-button-1');

myDiv.addEventListener('click', function() {
  alert('test');
});

function loadInitialValues() {
  var url = '/settings';
  fetch(url, {
    method: 'GET'
  })
    .then(response => response.json())
    .then(responseData => {
      console.log(responseData);
      document.getElementById("bot-credentials-token").setAttribute("value", responseData.token)
    })
    .catch(error => {
      console.error('Error:', error);
    });
}

function botCredentialsSave() {
  let tokenValue = document.getElementById("bot-credentials-token").value;

  let data = {
    token : tokenValue
  };
  let serializedData = JSON.stringify(data);

  var url = '/bot-credentials/set';
  fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: serializedData
  })
    .then(response => response.text())
    .then(responseData => {
      console.log(responseData);
    })
    .catch(error => {
      console.error('Error:', error);
    });
}