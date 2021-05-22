document.addEventListener('DOMContentLoaded', function() {

    const close_button = document.querySelector(".navbar-close");

    /* function called when you click of the button */
    close_button.addEventListener('click', function() {
        
        /* this if else to change the text in the button */
        if(close_button.innerHTML === "🞬"){
            close_button.innerHTML = "☰";
        }else{
            close_button.innerHTML = "🞬";
        }
      
      /* this function toggle the visibility of our "li" elements */
      document.querySelectorAll(".navbar-list-items").forEach(list_items => {
          if (list_items.classList.contains("animate-show")){
            list_items.classList.remove("animate-show");
            list_items.classList.add("animate-hide");

            list_items.addEventListener('animationend', () => {
                list_items.classList.remove("animate-hide");
              });
          } else {
            list_items.classList.add("animate-show");
            list_items.classList.remove("animate-hide");
          }
      });
    });
});