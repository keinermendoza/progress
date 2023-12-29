// SECTION BUTTONS 
document.addEventListener('alpine:init', () => {
    Alpine.store('section', {
        
        activeSection: [
            {name:'home', isActive:null},
            {name:'all', isActive:true},
            {name:'public', isActive:null},
            {name:'private', isActive:null},
        ],

        updateActive(sectionName) {
            this.activeSection =  this.activeSection.map(section => ({...section, isActive: section.name == sectionName}))
        },

        isActive(sectionName) {
            return this.activeSection.find((section) => section.name === sectionName).isActive
        },
        deactivate() {
            this.activeSection = this.activeSection.map(section => ({...section, isActive: false}))
        }
    
}),

// PASSING DATA TO EDIT NOTE FORM
Alpine.store('notes', {
    editProccess(noteId, noteMessage) {
        Array.from(document.getElementsByClassName('form-edit-notes')).forEach(form => {
            
            // update form data
            form.note.value = noteMessage;
            form.noteId.value = noteId;
            
        })}
    })
})

// DELETING NOTE
document.addEventListener("htmx:confirm", function(e) {
    if (Array.from(e.target.classList).includes('delete-note'))  { 
        e.preventDefault()
  
      // Mostrar un cuadro de diálogo personalizado con Swal
      Swal.fire({
        title: "Proceed?",
        text: `I ask you... ${e.detail.question}`
      }).then(function(result) {
        if (result.isConfirmed) {
            const event = new CustomEvent("delete-note");
            e.target.dispatchEvent(event)
            e.detail.issueRequest(true); // this continue the request

        } 
      });
    }
});

// CREATING NOTE
// https://www.reddit.com/r/htmx/comments/10hu6wp/how_to_know_which_event_was_triggered/
htmx.on("htmx:afterRequest", (e) => {
    if (Array.from(e.target.classList).includes("form-notes")) {
        if (e.detail.successful) {
            e.target.note.value = ''
            const event = new CustomEvent("upp-note-counter");
            e.target.dispatchEvent(event)

            Swal.fire({
                icon: "success",
                title: "Note Created",
                showConfirmButton: false,
                timer: 1500
            });

        } else {

            console.log(e)
            console.log(e.target)

            Swal.fire({
                icon: "error",
                title: "Oops...",
                text: e.detail.xhr.responseText,
                showConfirmButton: false,
                timer: 2500
            });

        }
    } 
    // EDITING NOTE
    else if (Array.from(e.target.classList).includes("form-edit-notes")) {
        if (e.detail.successful) {
            e.target.note.value = ''
            const event = new CustomEvent("set-editing-false");
            e.target.dispatchEvent(event)

            Swal.fire({
                icon: "success",
                title: "Note Updated",
                showConfirmButton: false,
                timer: 1500
            });

        } else {

        console.log(e)
        console.log(e.target)

        Swal.fire({
            icon: "error",
            title: "Oops...",
            text: e.detail.xhr.responseText,
            showConfirmButton: false,
            timer: 2500
          });

        }
    } 
});

document.addEventListener("privated_project_added", () => {
    alert("listo")
})