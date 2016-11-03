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
  syncButton.classList.add('trellearn-sync');
  syncButton.innerText = 'Sync Trellearn';
  syncButton.onclick = sync;

  orderButton = document.createElement('button');
  orderButton.classList.add('trellearn-button');
  orderButton.classList.add('trellearn-order');
  orderButton.innerText = 'Trellearn order';
  orderButton.onclick = order;

  document.body.appendChild(orderButton);
  document.body.appendChild(syncButton);

  fetchBoard();
});

function order(e) {
  e.preventDefault();
  e.stopPropagation();
  var matches = window.location.href.match(/\/(.{8})\//);
  Trellearn.cardShortLink = matches[1];
  console.log('The card short Id is:', Trellearn.cardShortLink);
  $.getJSON('https://trello.com/1/cards/'+Trellearn.cardShortLink+'?fields=all', function(card) {
    Trellearn.card = card;
    sendCard();
  });
}

function sendCard(){
  console.log(Trellearn)
  $.ajax({
    type: 'post',
    url: 'http://localhost:8000/labels',
    data: JSON.stringify(_.pick(Trellearn, ['card', 'boardId'])),
    dataType: 'json',
    contentType: "application/json; charset=utf-8",
    traditional: true,
    success: reorderLabels,
  });
}

function reorderLabels(orderedLabels) {
  ul = document.querySelector('.edit-labels-pop-over');
  if(ul) {
    for (i in orderedLabels) {
      span = ul.querySelector('li span[data-idlabel="'+ orderedLabels[i].id +'"]');
      li = span.parentElement;
      orderedLabels[i].li = li;
    }
    while(ul.firstChild){
      ul.removeChild(ul.firstChild);
    }
    for (i in orderedLabels) {
      ul.appendChild(orderedLabels[i].li);
    }
  }
}

function sync(e) {
  e.preventDefault();
  e.stopPropagation();
  $.getJSON('https://trello.com/1/boards/'+Trellearn.boardId+'/cards?fields=all', function(cards) {
    console.log('Sync: ' + cards.length + ' card(s) fetched');
    Trellearn.cards = cards;
    sendCards();
  });
}

function sendCards(){
  $.ajax({
    type: 'post',
    url: 'http://localhost:8000/learn',
    data: JSON.stringify(_.pick(Trellearn, ['cards', 'boardId'])),
    dataType: 'json',
    contentType: "application/json; charset=utf-8",
    traditional: true,
    success: function(response){
      console.log(response);
    },
  });
}

function fetchBoard() {
  $.getJSON('https://trello.com/1/members/me/boards?filter=open&fields=shortLink', function(boards) {
    var board = _.find(boards, ['shortLink', Trellearn.boardShortLink]);
    Trellearn.boardId = board.id;
    console.log('Your board ID is:', Trellearn.boardId);
  });
}
