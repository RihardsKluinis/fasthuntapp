$(document).ready(function() {
  $('#projects').on('change', '.project-checkmark', function() {
    var projectId = $(this).data('project-id');
    var checked = $(this).is(':checked');
    var url = '/project_checkmarks';
    var method = checked ? 'POST' : 'PATCH';

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
        updateProfileCheckmarks(projectId, checked);
      },
      error: function(data) {
        console.log('Error updating project checkmark.');
      }
    });
  });

  function updateProfileCheckmarks(projectId, checked) {
    $('#projects .profile-checkmark[data-project-id="' + projectId + '"]').each(function() {
      $(this).prop('checked', checked);
    });
  }
});
