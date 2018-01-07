
function TodoList(container, incompleteItems, completeItems) {
// Object which associated with todo list displayed on screen.
// container is the ul element containing all list items
// incompleteItems and completeItems are list items in container
  this.container = container;
  this.incompleteItems = incompleteItems;
  this.completeItems = completeItems;

  this.displayIncompleteItems = function () {
    for (let i = 0; i < this.completeItems.length; i++) {
      this.completeItems[i].classList.add('hide');
    }

    for (let i = 0; i < this.incompleteItems.length; i++) {
      this.incompleteItems[i].classList.remove('hide');
    }
  }

  this.displayCompleteItems = function () {
    for (let i = 0; i < this.incompleteItems.length; i++) {
      this.incompleteItems[i].classList.add('hide');
    }

    for (let i = 0; i < this.completeItems.length; i++) {
      this.completeItems[i].classList.remove('hide');
    }

  }

  this.displayAll = function () {
    for (let i = 0; i < this.incompleteItems.length; i++) {
      this.incompleteItems[i].classList.remove('hide');
    }
    for (let i = 0; i < this.completeItems.length; i++) {
      this.completeItems[i].classList.remove('hide');
    }
  }
}

var todoListTest = null;

var initializeTodoList = function () {
  // initialize todolist
  let todoListContainer = document.getElementById('todoList');
  if (!todoListContainer) {
    // ensure todolist is actually there. Stop initialization if it isn't.
    return;
  }
  let incompleteItems = document.querySelectorAll('.incomplete');
  let completeItems = document.querySelectorAll('.completed');

  var todoList = new TodoList(todoListContainer, incompleteItems, completeItems);

  // initialize controls
  let displayAllButton = document.getElementById('displayAllItems');
  let displayCompleteItemsButton = document.getElementById('displayCompleteItems');
  let displayIncompleteItemsButton = document.getElementById('displayIncompleteItems');

  displayAllButton.addEventListener('click', function () {todoList.displayAll();});
  displayCompleteItemsButton.addEventListener('click', function () {todoList.displayCompleteItems();});
  displayIncompleteItemsButton.addEventListener('click', function () {todoList.displayIncompleteItems();});

  return todoList;


}

document.addEventListener('DOMContentLoaded', initializeTodoList());
