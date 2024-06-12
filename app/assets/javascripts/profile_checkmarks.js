$(document).ready(function() {
  $('#projects').on('change', '.profile-checkmark', function() {
    var profileId = $(this).data('profile-id');
    var checked = $(this).is(':checked');
    var url = '/checkmarks';
    var method = 'POST';
    var checkmarkId = $(this).data('checkmark-id');

    if (checkmarkId) {
      url += '/' + checkmarkId;
      method = 'PATCH';
    }

    console.log('Profile ID:', profileId, "CheckmarkID:", checkmarkId);
    console.log('URL:', url);
    $.ajax({
      url: url,
      type: method,
      data: {
        checkmark: {
          profile_id: profileId,
          checked: checked
        },
        authenticity_token: $('meta[name="csrf-token"]').attr('content')
      },
      success: function(data) {
        console.log('Checkmark updated successfully.');
        if (method === 'POST') {
          // Update the data-checkmark-id attribute with the new checkmark ID
          $('.profile-checkmark[data-profile-id="' + profileId + '"]').data('checkmark-id', data.id);
        }
      },
      error: function(data) {
        console.log('Error updating checkmark.');
      }
    });
  });
});


document.addEventListener('DOMContentLoaded', function() {
  const checkboxes = document.querySelectorAll('.profile-checkmark');

  checkboxes.forEach(checkbox => {
    checkbox.addEventListener('change', function() {
      const profileId = this.getAttribute('data-profile-id');
      const textElement = document.getElementById(`text-${profileId}`);
      if (this.checked) {
        textElement.textContent = 'Done';
      } else {
        textElement.textContent = 'Connect';
      }
    });
  });
});
