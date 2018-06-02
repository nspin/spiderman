console.log("<<<>>>>");
window.addEventListener('load', function(){
    var req = new XMLHttpRequest();
    req.addEventListener('load', function(){
        console.log(this.responseText);
    })
    req.open('GET', 'http://www.example.org/example.txt');
    req.send();
});
