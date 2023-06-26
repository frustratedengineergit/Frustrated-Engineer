// Custom theme code

if (document.getElementsByClassName("clean-gallery").length > 0) {
  baguetteBox.run(".clean-gallery", { animation: "slideIn" });
}

if (document.getElementsByClassName("clean-product").length > 0) {
  window.onload = function () {
    vanillaZoom.init("#product-preview");
  };
}

window.onscroll = function () {
  scrollFunction();
};

function scrollFunction() 
{
  var nav_logo = document.getElementById('nav-logo');
  var navbar = document.getElementById('navbar');
  if (document.body.scrollTop > 80 || document.documentElement.scrollTop > 10) 
  {
    navbar.style.color = "white !important";
    navbar.classList.add("bg-nav", "navbar-dark");
    navbar.classList.remove("bg-transparent", "navbar-light");
    navbar.style.boxShadow ="0px 0px 15px rgba(255, 255, 255, .1)";
    navbar.style.fontFamily = null;
    nav_logo.src = "/static/img/white_logo.png";
  } 
  else 
  {
    navbar.style.fontFamily = 'Fredericka the Great';
    navbar.style.color = "black";
    navbar.style.removeProperty("box-shadow");
    navbar.classList.add("bg-transparent", "navbar-light");
    navbar.classList.remove("bg-nav", "navbar-dark");
    nav_logo.src = "/static/img/dark_logo2.0(lighter-shade).png";
  }
}

  