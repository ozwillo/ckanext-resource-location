"use strict";

/* location_showbar
 *
 * This JavaScript module shows a loadbar while handling an uploaded file.
 *
 */

ckan.module('location_showbar', function ($) {
  return {
    initialize : function () {
        this.el.click( function() {
            var x = document.getElementById("progress");
            x.style.display = "block";
        })
    }
  };
});