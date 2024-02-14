function set_task_clear_form() {
    let tcf = document.getElementById('task-clear-form');
    tcf.addEventListener('submit', function(evt) {
        evt.preventDefault();
        Swal.fire({
            title: "Are you sure?",
            text: "This will delete all completed tasks",
            icon: "question",
            showCancelButton: true,
            confirmButtonText: "Yes",
          }).then((result) => {
            if (result.isConfirmed) {
              tcf.submit();
            }
          });
    })
}


function set_password_revealers() {
    let prls = document.querySelectorAll('.reveal-password-box .reveal-password');
    prls.forEach(function(prl) {
        prl.addEventListener('click', function(evt) {
            let ptn, pwi, ipt, eye;
            ptn = prl.parentElement.parentElement;
            pwi = ptn.firstElementChild;
            eye = prl.firstElementChild;
            ipt = pwi.getAttribute('type');
            pwi.setAttribute('type', (ipt == 'password') ? 'text' : 'password');
            eye.classList.toggle('fa-eye');
            eye.classList.toggle('fa-eye-slash');
        })
    })
}