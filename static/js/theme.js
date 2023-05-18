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
  if (document.body.scrollTop > 80 || document.documentElement.scrollTop > 10) 
  {
    document.getElementById("navbar").style.padding = "1.2rem 1rem";
    document.getElementById("navbar").style.color = "white !important";
    document.getElementById("navbar").classList.add("bg-nav", "navbar-dark");
    document.getElementById("navbar").classList.remove("bg-transparent", "navbar-light");
    document.getElementById("navbar").style.boxShadow ="0px 0px 15px rgba(255, 255, 255, .1)";
    document.getElementById("navbar").style.fontFamily = null;
  } 
  else 
  {
    document.getElementById("navbar").style.fontFamily = "Chalkduster";
    document.getElementById("navbar").style.color = "black";
    document.getElementById("navbar").style.removeProperty("box-shadow");
    document.getElementById("navbar").classList.add("bg-transparent", "navbar-light");
    document.getElementById("navbar").classList.remove("bg-nav", "navbar-dark");
  }
}
// Nav Link Active JS Script 
// Get all the nav links
const navLinks = document.querySelectorAll('.nav-link');

// Add click event listener to each nav link
navLinks.forEach(link => {
  link.addEventListener('click', function() {
    // Remove active class from all nav links
    navLinks.forEach(link => {
      link.classList.remove('active');
    });

    // Add active class to the clicked nav link
    this.classList.add('active');
  });
});

  