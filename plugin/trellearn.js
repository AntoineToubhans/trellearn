var Trellearn = {}

$(document)
.ready(function() {
  console.log('Hello! I am Trellearn')
  var matches = window.location.href.match(/\/(.{8})\//);
  if (matches && matches.length > 1){
    Trellearn.boardShortLink = matches[1];
    console.log('Your board short link is:', Trellearn.boardShortLink);
  }

  syncButton = document.createElement('button');
  syncButton.classList.add('trellearn-button');
  syncButton.innerText = 'Sync Trellearn';
  syncButton.onclick = sync;

  document.body.appendChild(syncButton);

  fetchBoard()
});

function sync() {
  console.log('lol');
  $.ajax({
    type: 'post',
    url: 'http://localhost:8000/learn',
    data:  JSON.stringify({
      board: [{ coucou: 'lol' }],
    }),
    dataType: 'json',
    contentType: "application/json; charset=utf-8",
    traditional: true,
    success: function(response){
      console.log(response);
    },
  });
}

function fetchBoard() {
  // tokens=all&sessions=all&credentials=all&logins=true
  $.getJSON('https://trello.com/1/members/me/boards?filter=open&fields=shortLink', function(boards) {
    var board = _.find(boards, ['shortLink', Trellearn.boardShortLink]);
    Trellearn.boardId = board.id;
    console.log('Your board id is:', Trellearn.boardId);
  });
}
