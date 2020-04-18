function allowCardMove(ev) {
  // if we don't have a card, allow a drop event to happen
  if (ev.currentTarget.getElementsByClassName("card").length == 0) {
    ev.preventDefault();
    ev.dataTransfer.dropEffect = "move";
  }
}

function dragEnter(ev) {
  if (ev.currentTarget.getElementsByClassName("card").length == 0) {
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
  ev.effectAllowed = "copyMove";
}

function dropCard(ev) {
  console.log("Dropped");
  if (ev.currentTarget.getElementsByClassName("card").length == 0) {
    ev.preventDefault();
    let data = ev.dataTransfer.getData("text");
    let card = document.getElementById(data);
    // move the card
    ev.currentTarget.appendChild(card);
    // reset card font size
    card.style.fontSize = Math.max(6, card.clientHeight / 13) + 'px';
  }
  ev.currentTarget.classList.remove("dragTarget");
}

window.addEventListener('DOMContentLoaded', () => {
  // Add event handlers for cards and cardDests
  // Find the elements we want by class name
  const cards = document.getElementsByClassName("card");
  for(var i=0; i < cards.length; i++) {
    let element = cards[i];
    element.addEventListener("dragstart", dragCard);
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
