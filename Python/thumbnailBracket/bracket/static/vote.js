let voteForm = document.forms["vote-form"];
var left = document.getElementsByName("left")[0];
var right = document.getElementsByName("right")[0];

function voteClick(e) {
  document.getElementById("vs").innerHTML = '<div class="spinner-border text-primary" role="status"> <span class="sr-only">Loading...</span></div>'
  console.log("event on " + e.target.name);
  e.preventDefault();
  data = new FormData(voteForm);
  if (e.target === left) {
    data.append("win", left.id);
    data.append("lose", right.id);
  } else {
    data.append("lose", left.id);
    data.append("win", right.id);
  }
  //submit the data via XHR
  let request = new XMLHttpRequest();
  request.open("POST", "/vote/");
  request.onload = (e) => {
    if (request.status == 200) {
      console.log("submitted!");
      document.getElementById("vote-container").innerHTML = request.response
      thumbnails = document.getElementsByClassName("thumbnail")
      left = document.getElementsByName("left")[0];
      right = document.getElementsByName("right")[0];
      for(ele of thumbnails){
          ele.addEventListener("click", voteClick);
      }

    } else {
      console.log(
        "Error " +
          request.status +
          " occurred when voting <br />"
      );
    }
  };
  request.send(data);
}

left.addEventListener("click", voteClick);
right.addEventListener("click", voteClick);