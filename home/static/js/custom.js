function required(inputtx)
   {
     var empt1 = document.login.username.value;
     var empt2 = document.login.password.value;
          if (empt1 == 0 || emp2 == 0)
      {
         alert("Cannot be Empty!!");
         return false;
      }
      return true;
    }

var b=document.querySelector('#login');

b.addEventListener('click',function(evt){
     b.style.color="black";
     b.style.backgroundColor="white";
});


