//= require rails-ujs
//= require turbolinks
//= require_tree .



import "@hotwired/turbo-rails"
import "controllers"

import { Turbo } from "@hotwired/turbo-rails"
Turbo.session.drive = false


$(document).on('turbolinks:load', function() {
    $('form').on('submit', function(event) {
      event.preventDefault();
      $.get($(this).attr('action'), $(this).serialize(), null, 'script');
    });
  });


