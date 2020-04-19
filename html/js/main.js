function allowCardMove(ev) {
  // Don't count if the card being moved is the card we have
  let mycard = ev.currentTarget.getElementsByClassName("card")[0];
  if (!mycard.classList.contains("dragStart")) {
    ev.preventDefault();
    ev.dataTransfer.dropEffect = "move";
  }
}

function dragEnter(ev) {
  // Don't count if the card being moved is the card we have
  let mycard = ev.currentTarget.getElementsByClassName("card")[0];
  if (!mycard.classList.contains("dragStart")) {
    ev.currentTarget.classList.add("dragTarget");
  }
}

function dragLeave(ev) {
  ev.currentTarget.classList.remove("dragTarget");
}


function dragCard(ev) {
  // The start of a card drag.
  // We need to record the id of the thing being dragged in the drag event's
  // dataTransfer - otherwise when we get to the drop event we won't know
  // which card to move.
  ev.dataTransfer.setData("text", ev.target.id);
  ev.target.classList.add("dragStart");
  ev.effectAllowed = "copyMove";
  document.body.classList.add("dragActive");
}

function dragStop(ev) {
  ev.target.classList.remove("dragStart");
  document.body.classList.remove("dragActive");
}

function dropCard(ev) {
  document.body.classList.remove("dragActive");
  ev.currentTarget.classList.remove("dragTarget");
  let oldcard = ev.currentTarget.getElementsByClassName("card")[0];
  ev.preventDefault();
  let data = ev.dataTransfer.getData("text");
  let newcard = document.getElementById(data);
  // swap the cards
  newcard.parentElement.appendChild(oldcard);
  ev.currentTarget.appendChild(newcard);
  // reset card font size
  newcard.classList.remove("dragStart");
  oldcard.classList.remove("dragStart");
  newcard.style.fontSize = Math.max(6, newcard.clientHeight / 13) + 'px';
  oldcard.style.fontSize = Math.max(6, oldcard.clientHeight / 13) + 'px';
}

window.addEventListener('DOMContentLoaded', () => {
  // Add event handlers for cards and cardDests
  // Find the elements we want by class name
  const cards = document.getElementsByClassName("card");
  for(var i=0; i < cards.length; i++) {
    let element = cards[i];
    element.addEventListener("dragstart", dragCard);
    element.addEventListener("dragend", dragStop);
    element.addEventListener("dblclick", (ev) => {
      ev.currentTarget.classList.toggle("cardfront");
      ev.currentTarget.classList.toggle("cardback");
    });
  }
  const cardDests = document.getElementsByClassName("cardDest");
  for(var i=0; i < cardDests.length; i++) {
    let element = cardDests[i];
    element.addEventListener("dragover", allowCardMove);
    element.addEventListener("drop", dropCard);
    element.addEventListener("dragenter", dragEnter);
    element.addEventListener("dragleave", dragLeave);
  }
});

// Compute the cards' font sizes.
// Unfortunately, we can't do this in CSS because CSS can't
// access an element's width/height when setting font-size.
// We can't do this above because during DOMContentLoaded
// layout hasn't happened yet, so .clientHeight is 0
window.addEventListener('load', () => {
  // Get the elements by class name
  const cards = document.getElementsByClassName("card");
  for(var i=0; i < cards.length; i++) {
    let card = cards[i];
    card.style.fontSize = Math.max(6, card.clientHeight / 13) + 'px';
  }
});
