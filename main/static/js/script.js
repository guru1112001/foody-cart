const toggle = document.querySelector(".toggle");
toggle.onclick = () => {
  document.body.classList.toggle("active");
};

$(function () {
  $(".product-card").hover(function () {
    $(this).find(".description").animate(
      {
        height: "toggle",
        opacity: "toggle",
      },
      300
    );
  });
});
