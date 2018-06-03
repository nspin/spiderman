window.addEventListener('load', function(){
    console.log('injection start');
    var req = new XMLHttpRequest();
    req.addEventListener('load', function(){
        console.log(this.responseText);
        window.location = 'https://cia.gov/next';
    })
    req.open('POST', 'https://cia.gov/enqueue');
    req.send(JSON.stringify([
        'https://stackoverflow.com/questions/39519246/make-xmlhttprequest-post-using-json',
        'https://github.com/pallets/werkzeug/blob/master/examples/shortly/shortly.py',
        'https://stackoverflow.com/questions/39519246/make-xmlhttprequest-post-using-json',
        'https://github.com/pallets/werkzeug/blob/master/examples/shortly/shortly.py',
        'https://stackoverflow.com/questions/39519246/make-xmlhttprequest-post-using-json',
        'https://github.com/pallets/werkzeug/blob/master/examples/shortly/shortly.py',
        'https://stackoverflow.com/questions/39519246/make-xmlhttprequest-post-using-json',
        'https://github.com/pallets/werkzeug/blob/master/examples/shortly/shortly.py',
        'https://stackoverflow.com/questions/39519246/make-xmlhttprequest-post-using-json',
        'https://github.com/pallets/werkzeug/blob/master/examples/shortly/shortly.py',
        'https://stackoverflow.com/questions/39519246/make-xmlhttprequest-post-using-json',
        'https://github.com/pallets/werkzeug/blob/master/examples/shortly/shortly.py'
    ]));
});
