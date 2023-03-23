const flashcards = document.getElementsByClassName("flashcards")[0];
const createBox = document.getElementsByClassName("create-box")[0];
const question = document.getElementById("question");
const answer = document.getElementById("answer");
let contentArray = localStorage.getItem('items') ? JSON.parse(localStorage.getItem('items')) : [];

//To display flashcard on screen
contentArray.forEach(divMaker);
function divMaker(text){
    var div = document.createElement("div");
    var h2_question = document.createElement("h2");
    var h2_answer = document.createElement("h2");

    div.className = 'flashcard';
    div.setAttribute("style","border:1px solid purple; padding:15px;margin:30px;background-image: linear-gradient(rgb(250, 255, 177), rgb(255, 213, 134));box-shadow: 0 2px 4px 0 indianred;")
    h2_question.setAttribute("style", "color:blue; padding:15px;");
    h2_question.innerHTML = text.my_question;

    h2_answer.setAttribute("style","text-align:center; display:none; color:purple;");
    h2_answer.innerHTML = text.my_answer;

    div.appendChild(h2_question);
    div.appendChild(h2_answer);

    div.addEventListener("click", function(){
        if(h2_answer.style.display == "none")
            h2_answer.style.display = "block";
        else
            h2_answer.style.display = "none";
    });
    flashcards.appendChild(div);
}

function AddCard(){
    var flashcard_info = {
        'my_question' : question.value,
        'my_answer' : answer.value
    }//user_dictionary
    contentArray.push(flashcard_info);
    localStorage.setItem('items', JSON.stringify(contentArray));//add to local storage
    divMaker(contentArray[contentArray.length - 1]);// last elem from array
    //clear inputs in the text boxes
    question.value = '';
    answer.value = '';
}

function hideCard(){
    createBox.style.display = "none";
}

function CreateCards(){
    createBox.style.display = "block";
}

function DeleteCards(){
    localStorage.clear();
    flashcards.innerHTML = '';
    contentArray = [];
}