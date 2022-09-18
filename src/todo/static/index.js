document.addEventListener('DOMContentLoaded', evt => {
    const todoContainer = document.querySelector("#todo-container")
    fetch('http://127.0.0.1:5000/todo')
        .then((response) => response.json())
        .then((data) => {
           data.data.forEach( item => {
            todo_card = createTodoCard(item)
            todoContainer.appendChild(todoCard)
           })
        });
})

function createTodoCard(item) {
    todoCard = document.createElement("div")
    todoContent = document.createElement("p")
    todoContent.innerHTML = item.text
    deleteButton = createDeleteButton(item.id)
    resolveButton = createResolveButton()
    todoCard.appendChild(todoContent)
    todoCard.id = "todo-" + item.id
    return todoCard
}

function createDeleteButton(todoId) {
    return null
}

function createResolveButton() {
    return null
}

function completeAction(){
    return null
}

function deleteAction(){
    return null
}


addTodoButton = document.querySelector("#add-button")
addTodoButton.addEventListener("click", evt => {
    evt.preventDefault()
    const todoContainer = document.querySelector("#todo-container")
    const todoInput = document.querySelector("#todo-text")
    const todoText = todoInput.value
    fetch("http://127.0.0.1:5000/todo", {
        method: "POST",
        mode: "cors",
        cache: 'no-cache',
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({"text" : todoText})
    })
    .then(response => response.json())
    .then(data => {
        todoInput.value = ""
        todoCard = createTodoCard(data.data)
        todoContainer.appendChild(todoCard)
    })
})
