// var myDiv = document.getElementById('sidebar-button-1');

// myDiv.addEventListener('click', function() {
//   alert('test');
// });

function loadDashboard() {
  loadDashboardMenu("immersive-welcome-experience");
  loadInitialValues();

  bindSidebarButton("open-immersive-welcome-experience", "immersive-welcome-experience");
  bindSidebarButton("open-bot-credentials", "bot-credentials");
  bindSidebarButton("open-server-management", "server-management");
  bindSidebarButton("open-moderation-module", "moderation-module");
  bindSidebarButton("open-greetings-module", "greetings-module");
  bindSidebarButton("open-special-channels-module", "special-channels-module");
  bindSidebarButton("open-polls-module", "polls-module");
  bindSidebarButton("open-slash-commands", "slash-commands");
}

function bindSidebarButton(buttonId, pageId) {
  let button = document.getElementById(buttonId);

  button.addEventListener('click', function() {
    loadDashboardMenu(pageId);
  });
}

function loadDashboardMenu(pageId) {
  let menus = document.getElementsByClassName("category");
  
  Array.from(menus).forEach((element) => {
    if(element.id == pageId) {
      element.style.display = "block";
    } else {
      element.style.display = "none";
    }
  });
}

function loadInitialValues() {
  var url = '/settings';
  fetch(url, {
    method: 'GET'
  })
    .then(response => response.json())
    .then(responseData => {
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

function slashCommandsRegister() {
  var url = '/register-slash-commands';
  fetch(url, {
    method: 'GET'
  })
    .then(response => response.text())
    .then(responseData => {
      console.log(responseData)
    })
    .catch(error => {
      console.error('Error:', error);
    });
}