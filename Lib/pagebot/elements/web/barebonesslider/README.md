Bare-Bones-Slider
=================

Description: jQuery slider with little bloat but lots of customization.

Author: Richard Hung

More documentation and examples: http://www.bbslider.com

## Install

Install it using [Bower](http://bower.io):

```sh
$ bower install bare-bones-slider
```

Install it using [npm](https://www.npmjs.org/):

```sh
$ npm install bare-bones-slider
```

Or [download as ZIP](https://github.com/Richard1320/Bare-Bones-Slider/archive/master.zip).

Key Features
--------------------

* Carousel to show multiple slides simultaneously
* Uses CSS3 transitions with advanced easing
* Mask image for custom animations
* Allows you to make your own pagination and controls
* Public methods that you can call outside of the plugin
* Variables can be retrieved at any time
* Touch controls for phones

How to Use
--------------------

Bare Bones slider has a .js and a .css file in addition to the jQuery library.

```
<link type="text/css" href="css/jquery.bbslider.css" rel="stylesheet" media="screen" />
<script src="http://code.jquery.com/jquery-latest.js"></script>
<script type="text/javascript" src="js/jquery.bbslider.min.js"></script>
```

Create a container for the slider and children for the panels.

```
<div class="slider">
    <div><img src="images/image-1.jpg" alt="first image" /></div>
    <div><img src="images/image-2.jpg" alt="second image" /></div>
    <div><img src="images/image-3.jpg" alt="third image" /></div>
    <div><img src="images/image-4.jpg" alt="forth image" /></div>
    <div><img src="images/image-5.jpg" alt="fifth image" /></div>
</div>
```

Call the slider after the HTML markup and required files.

```
$('.slider').bbslider({
    auto:  true,
    timer: 3000,
    loop:  true
});
```
