// Browser detection for when you get desparate. A measure of last resort.
// http://rog.ie/post/9089341529/html5boilerplatejs
// sample CSS: html[data-useragent*='Chrome/13.0'] { ... }
//
// var b = document.documentElement;
// b.setAttribute('data-useragent',  navigator.userAgent);
// b.setAttribute('data-platform', navigator.platform);

window.addEventListener("awesomplete-selectcomplete", function(e){
  console.log('selected');
  var destination = document.getElementById('family-searcher').getAttribute('data-destination');
  var target = document.getElementById('family-searcher').value;
  window.location = destination + target;
}, false);

// remap jQuery to $
(function($){

  /* trigger when page is ready */
  $(document).ready(function (){

    /*

    $('.nav-global-reveal').click(function() {
      $('html').toggleClass('nav-global-show-nav');
      return false;
    });

    */

    $('.nav-user-reveal').click(function() {
      $('html').toggleClass('nav-user-show-nav');
      return false;
    });

    $('.nav-foundry-reveal').click(function(){
      $('html').toggleClass('nav-foundry-show-nav');
      $('html').removeClass('nav-global-show-nav');
      return false;
    });

    $('.content-options-show-filters').click(function(){
      $('html').toggleClass('filters-reveal');
      return false;
    });

    $('.content-filters-close').click(function(){
      $('html').removeClass('filters-reveal');
      return false;
    });

    $('.button-metadata').click(function(){
      $('.definition-designer').toggleClass('show-all-definitions');
      return false;
    });

    $('.section-landing-toggle-extended').click(function(){
      $(this).toggleClass('toggle-hide');
      $('.section-landing-foundry-extended').toggleClass('show-extended');
      return false;
    });

    $('.content-filters h3 a').each(function(){
      $(this).click(function(){
        $(this).parent().next().toggleClass('content-filters-collapsed');
        $(this).parent().toggleClass('content-filters-group-collapsed');
        return false;
      });
    });

    $('.content-filters-select-header a').each(function(){
      $(this).click(function(){
        $(this).parent().next().toggleClass('content-filters-select-revealed');
        return false;
      });
    });

    $(document).on('click', function(event) {
      if (!$(event.target).closest('.content-filters-select').length) {
        $('.content-filters-select').removeClass('content-filters-select-revealed');
      }
    });

    if(($('.foundry-page .content-filters-select li.active')) != -1) {
      var foundryName = $('.foundry-page .content-filters-select li.active a').html();
      $('.foundry-page .content-filters-select-header a').html(foundryName);
      $('.foundry-page .content-filters-select-header').addClass('content-filter-selected');
    }

    if (window.location.hash) {

      if (window.location.hash.indexOf('subscribe') == 1) {

        $('#subscribe').click(function(e) {

          if (e.target.id === "subscribe"){
                location.hash = '';
            }

        });

      }
    }

  });


  /* optional triggers

  $(window).load(function() {

  });

  */

  $(window).resize(function() {

    $('html').removeClass('nav-global-show-nav');
    $('html').removeClass('nav-foundry-show-nav');
    $('html').removeClass('filters-reveal');

  });

})(window.jQuery);