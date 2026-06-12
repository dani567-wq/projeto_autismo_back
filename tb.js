const btn = document.querySelector('a');

btn.addEventListener('mousemove', event => {
    let rect = event.target.getBoundingClientRect().left
    let client = event.clientX * 3 - rect;
    
    btn.style.setProperty('--x', client + 'deg');

    


});



    
