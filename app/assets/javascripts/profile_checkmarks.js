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
          $('.profile-checkmark[data-profile-id="' + profileId + '"]').data('checkmark-id', data.id);
        }
        updateProjectCheckmark(profileId);
      },
      error: function(data) {
        console.log('Error updating checkmark.');
      }
    });
  });

  function updateProjectCheckmark(profileId) {
    var projectId = $('.profile-checkmark[data-profile-id="' + profileId + '"]').data('project-id');
    var allChecked = true;

    $('.profile-checkmark[data-project-id="' + projectId + '"]').each(function() {
      if (!$(this).is(':checked')) {
        allChecked = false;
      }
    });

    var projectCheckmark = $('.project-checkmark[data-project-id="' + projectId + '"]');
    if (allChecked) {
      projectCheckmark.prop('checked', true);
    } else {
      projectCheckmark.prop('checked', false);
    }
  }
});
