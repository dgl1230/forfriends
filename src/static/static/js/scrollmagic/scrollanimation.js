/*$(document).ready(function($)	{
var controller = new ScrollMagic();


var scene = new ScrollScene({triggerElement: "", triggerHook: "onEnter"})
                .addTo(controller);
                .on("start", function (e)	{
                	if (!$("#loader").hasClass("active"))	{
                		console
                	}
                })

// add multiple scenes at once
var scene2;
controller.addScene([
    scene, // add above defined scene
    scene2 = new ScrollScene({duration: 200}), // add scene and assign handler "scene2"
    new ScrollScene({offset: 20}) // add anonymous scene
]);
