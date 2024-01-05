toggler = document.getElementById('toggle-bar');
if(toggler) {
    toggler.addEventListener('click', function(ev) {
        content = document.getElementById('main-content-container')
        is_collapsed = Boolean(content.getAttribute('sidebar-collapse').toString().toLowerCase() === 'true')
        content.setAttribute('sidebar-collapse', !is_collapsed);
    });
}
