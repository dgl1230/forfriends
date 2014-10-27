checkPwd = function () {
    var str = document.getElementById('password').value;
    if (str.length < 6) {
        alert("Please enter a password that is at least 8 characters.");
        return ("too_short");
    }
}