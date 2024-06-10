
$(document).ready(function() {
  // Attach event listener to a parent element and delegate it to '.profile-checkmark' elements
  $('#projects').on('change', '.profile-checkmark', function() {
    var profileId = $(this).data('profile-id');
    var checked = $(this).is(':checked');
    var url = '/checkmarks';
    console.log('Profile ID:', profileId); 
    $.ajax({
      url: url,
      type: 'POST',
      data: {
        checkmark: {
          profile_id: profileId,
          checked: checked
        },
        authenticity_token: $('meta[name="csrf-token"]').attr('content')
      },
      success: function(data) {
        console.log('Checkmark updated successfully.');
      },
      error: function(data) {
        console.log('Error updating checkmark.');
      }
    });
  });
});
