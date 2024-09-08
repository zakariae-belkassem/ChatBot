window.onload = function (){
    //get user lang
    const userLanguage = navigator.language
    Lang(userLanguage)

};


function Lang(lang) {
    const dataLang = {
        "ar": [
            "تسجيل الدخول", "أدخل اسم المستخدم",
            "أدخل كلمة المرور", "تسجيل الدخول", "ليس لديك حساب؟",
            "اشترك", "الاشتراك", "أدخل اسم المستخدم", "قم بإنشاء كلمة مرور",
            "قم بتأكيد كلمة المرور", "الاشتراك", "هل لديك حساب؟", "تسجيل الدخول"
        ],
        "fr": [
             "Connexion", "Entrez votre nom d'utilisateur",
            "Entrez votre mot de passe", "Connexion", "Vous n'avez pas de compte ?",
            "S'inscrire", "S'inscrire", "Entrez votre nom d'utilisateur",
            "Créez un mot de passe", "Confirmez votre mot de passe", "S'inscrire",
            "Vous avez déjà un compte ?", "Connexion"
        ],
        "en": [
            "Login", "Enter your username",
            "Enter your password", "Login", "Don't have an account?",
            "Signup", "Signup", "Enter your username", "Create a password",
            "Confirm your password", "Signup", "Already have an account?", "Login"
        ]
    };
    if (lang === "ar") {
        document.getElementById("username").setAttribute("lang","ar")
        document.getElementById("username").setAttribute("dir","rtl")
        document.getElementById("password").setAttribute("lang","ar")
        document.getElementById("password").setAttribute("dir","rtl")

    }
    else if (lang === "fr" || lang === "en") {

        document.getElementById("username").setAttribute("lang","ar")
        document.getElementById("username").setAttribute("dir","ltr")
        document.getElementById("username").setAttribute("lang","fr")
        document.getElementById("username").setAttribute("dir","ltr")
    }

    let l = lang.substring(0,2).toLowerCase()
    document.getElementById("loginLbl").innerHTML = dataLang[l][0];
    document.getElementById("username").placeholder = dataLang[l][1];
    document.getElementById("password").placeholder = dataLang[l][2];
    document.getElementById("logBtn").value = dataLang[l][3];
    document.getElementById("registerLbl").innerHTML = dataLang[l][6];
    document.getElementById("usernameR").placeholder = dataLang[l][7];
    document.getElementById("passwordR").placeholder = dataLang[l][8];
    document.getElementById("confPswd").placeholder = dataLang[l][9];
    document.getElementById("signupR").value = dataLang[l][10];
    document.getElementById("ss").innerHTML = dataLang[l][11];

    document.getElementById("wxz").innerHTML = '<span class="signup" >'+ dataLang[l][4]  +
        '         <label for="check">'+ dataLang[l][5] +'</label>\n' +
        '        </span>'

    document.getElementById("ss").innerHTML = '<span class="signup"  >'+ dataLang[l][11] +
        '         <label for="check" >'+  dataLang[l][12] +'</label>\n' +
        '        </span>' ;

}




