window.onload = init;

function init() {

    state_selection = document.getElementById("state_choice");
    removeOptions(state_selection);

    /**
    Control country and state drop down options that are selectable
    */ 

    country_selection = document.getElementById("country_choice");

    country_selection.addEventListener('change', function() {

        // remove any entries in the state selection dropdown box
        removeOptions(state_selection);

        country_name = this.options[this.selectedIndex].text;
        console.log(country_name)

        fetch(`/maps/${country_name}`)
        .then(response => response.json())
        .then(object => {
            console.log(object);
            state_names = object;
            
            length = state_names[0].length;
            for (i = 0; i < length; i++) {
                new_option = document.createElement('option');
                new_option.value = state_names[1][i];
                new_option.innerHTML = state_names[0][i];
                state_selection.append(new_option)
            }

        })
    }, false);

}

function removeOptions(selectElement) {
    var i, L = selectElement.options.length - 1;
    for(i = L; i >= 0; i--) {
       selectElement.remove(i);
    }
}
