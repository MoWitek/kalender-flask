function request(url, data, method = "POST") {
    var pipe = new XMLHttpRequest();
    pipe.open(method, url, false);
    pipe.send(JSON.stringify(data));
    return JSON.parse(pipe.responseText)
}