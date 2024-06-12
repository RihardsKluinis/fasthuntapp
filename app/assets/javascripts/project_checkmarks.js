$(document).ready(function() {
  $('#projects').on('change', '.project-checkmark', function() {
    var projectId = $(this).data('project-id');
    var checked = $(this).is(':checked');
    var url = '/project_checkmarks';
    var method = 'POST';
    var checkmarkId = $(this).data('checkmark-id');

    if (checkmarkId) {
      url += '/' + checkmarkId;
      method = 'PATCH';
    }

    console.log('Project ID:', projectId, "CheckmarkID:", checkmarkId);
    console.log('URL:', url);
    $.ajax({
      url: url,
      type: method,
      data: {
        project_checkmark: {
          project_id: projectId,
          checked: checked
        },
        authenticity_token: $('meta[name="csrf-token"]').attr('content')
      },
      success: function(data) {
        console.log('Project checkmark updated successfully.');
        if (method === 'POST') {
          $('.project-checkmark[data-project-id="' + projectId + '"]').data('checkmark-id', data.id);
        } else if (method === 'PATCH' && !checked) {
          // Optional: Remove the data-checkmark-id attribute when unchecking the checkbox
          $('.project-checkmark[data-project-id="' + projectId + '"]').removeData('checkmark-id');
        }
      },
      error: function(data) {
        console.log('Error updating project checkmark.');
      }
    });
  });
});
