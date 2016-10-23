$(document)
.ready(function() {
  console.log('Hello! I am Trellearn')
  var matches = window.location.href.match(/\/(.{8})\//);
  if (matches && matches.length > 1){
    boardId = matches[1];
    console.log('Your board id is: ', boardId);
  }
  fetchUser()
});

function fetchUser() {
  $.getJSON('https://trello.com/1/Members/me?tokens=all&sessions=all&credentials=all&paid_account=true&credits=invitation%2CpromoCode&organizations=all&organization_paid_account=true&logins=true', function(user) {
    console.log(user);
  });
}
