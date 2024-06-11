// Configure your import map in config/importmap.rb. Read more: https://github.com/rails/importmap-rails
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