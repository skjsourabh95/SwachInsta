var b=document.querySelector('#signup');
var b2=document.querySelector('#signup2');
b.addEventListener('mouseenter',function(evt){
    var allClasses=b.classList;
    allClasses.remove("oneClass");
    allClasses.add("twoClass");
});
b.addEventListener('mouseleave',function(evt){
    var allClasses=b.classList;
    allClasses.remove("twoClass");
    allClasses.add("oneClass");

});
b2.addEventListener('mouseenter',function(evt){
    var allClasses=b2.classList;
    allClasses.remove("oneClass");
    allClasses.add("twoClass");
});
b2.addEventListener('mouseleave',function(evt){
    var allClasses=b2.classList;
    allClasses.remove("twoClass");
    allClasses.add("oneClass");

});
function required(inputtx)
   {
     var empt1 = document.login.username.value;
     var empt2 = document.login.password.value;
     var empt3 = document.login.name.value;
     var empt4 = document.login.email.value;
          if (empt1 == 0 || emp2 == 0|| emp3 == 0|| emp4 == 0)
      {
         alert("Cannot be Empty!!");
         return false;
      }
      return true;
    }

