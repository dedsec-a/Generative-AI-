const formInput = document.getElementById("input");
const Tasklist = document.getElementById("task-list");
const taskButton = document.getElementById("add-task");


let tasks = [];
/* logic --> The User will input some data in the in the input feild and when the user does that we have to wait for the event to haapen 
when it happens we have to capute the event and then put it in the next child of the event list item and then we must provide the user the 
functionality that the user can click on task completed and thus will be able to move on to the next  */

taskButton.addEventListener("click",() =>{
    const innerText = formInput.value.trim()

    if (innerText === "") return 

    const newData = {
        id : Date.now(),
        text: innerText,
        completed : false
    }

    tasks.push(newData)
    formInput.value = "";
    console.log(tasks);
})







