//Function to validate a user's password
function validate(){
    //Retrieve the username and password from the form
    var username = document.getElementById("usernameBox").value;
    var password = document.getElementById("passwordBox").value;

    var comments = "Your password is too weak:\n";
    var valid = true;

    //Check that both fields have been filled out. If not, return w/ error message
    if(username === "" || password === "")
    {
        alert("Must enter both a username and password\n");
        return; 
    }

    //Check all of the password requirements
    //Password must be at least 8 characters in length
    if(password.length < 8){
        comments += "Password must be at least 8 characters! \n";
        valid = false;
    }
    //Password must have at least one lowercase letter
    if(!password.match(/[a-z]/)){
        comments += "Password must contain a lowercase letter! \n";
        valid = false;
    }
    //Password must have at least one uppercase letter
    if(!password.match(/[A-Z]/)){
        comments += "Password must contain an uppercase letter! \n";
        valid = false;
    }
    //Password must contain at least one number
    if(!password.match(/\d/)){
        comments += "Password must contain a numeric digit (0-9)! \n";
        valid = false;
    }
    //Password must contain at least one special character
    if(!password.match(/[^a-zA-Z\d]/)){
        comments += "Password must contain a special character! \n";
        valid = false;
    }

    //If all the criteria are met, successfully log in
    if(valid){
        alert("Login successful!\n");
        //Clear the input boxes
        document.getElementById("usernameBox").value = "";
        document.getElementById("passwordBox").value = "";
    }
    //Return comments if any criterion isn't met
    else{
        alert(comments);
    }

    

}

//Switch between hidden password and displayed password on the login screen
function showPWD(){
    var pwd = document.getElementById("passwordBox");
    if (pwd.type === "password") {
        pwd.type = "text";
    } else {
        pwd.type = "password";
    }
}