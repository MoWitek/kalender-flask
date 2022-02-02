function login(username = undefined, password = undefined) {
    user = username || document.getElementById("login_username").value
    pass = password || document.getElementById("login_password").value

    if (pass && user) {
        print(user, pass)
        r = request("/login", { username: user, password: pass })
        document.getElementById("login_username").value = ""
        document.getElementById("login_password").value = ""
    } else {
        alert("Please Provide User and Password")
        r = {succes: false}
    }

    if (!r.error) {
        // loged in
    } else {
        // not logged in 
    } 

    userinfo_swicher(user)
    update_modal()
    return r.succes


}

function register(username = undefined, password = undefined, email = undefined, name = undefined) {
    ue = document.getElementById("register_username")
    pe = document.getElementById("register_password")
    ee = document.getElementById("register_email")
    ne = document.getElementById("register_name")
    pe_ = document.getElementById("register_password2")

    r = {
        username: ue.value,
        password: pe.value,
        email: ee.value,
        name: ne.value,
    }

    if (username != undefined && password != undefined && email != undefined && name != undefined) {
        r = {
            username: username,
            password: password,
            email: email,
            name: name
        }
    }




    if (pe.value != pe_.value) {
        alert("Passwords Don't match!")
    } else {
        if (r.username == "" && r.password == "" && r.email == "" && r.name == "") {
            alert("Please input full Credentials.")
        } else {
            ue.value = ""
            pe.value = ""
            ee.value = ""
            ne.value = ""
            pe_.value = ""

            return request("/register", r).succes
        }
        return false
    }
}

function logout() {
    request("logout", {})
    update_modal()
}

function userinfo_swicher(username=undefined){
    if (username === undefined) {
        txt1 = "You are currently not loged in."
        txt2 = "You need to be logged in to performe that Action."
    } else {
        txt1 = `You are loged in as: ${username}`
        txt2 = "&nbsp"
    } 

    document.getElementById("userlog-info").text = txt1
    document.getElementById("modal-header-text").innerHTML = txt2
}
