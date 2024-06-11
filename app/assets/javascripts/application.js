//= require rails-ujs
//= require turbolinks
//= require_tree .

import Rails from "@rails/ujs"

import * as ActiveStorage from "@rails/activestorage"
import "channels"

Rails.start()

ActiveStorage.start()