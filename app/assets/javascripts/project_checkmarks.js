$(document).ready(function() {
  // Attach event listener to a parent element and delegate it to '.project-checkmark' elements
  $('#projects').on('change', '.project-checkmark', function() {
    var projectId = $(this).data('project-id');
    var checked = $(this).is(':checked');
    var url = '/project_checkmarks'; // Adjust the URL endpoint for project checkmarks
    console.log('Project ID:', projectId); 
    $.ajax({
      url: url,
      type: checked ? 'POST' : 'PATCH', // Use POST for creating new checkmarks and PATCH for updating existing ones
      data: {
        project_checkmark: {
          project_id: projectId,
          checked: checked
        },
        authenticity_token: $('meta[name="csrf-token"]').attr('content')
      },
      success: function(data) {
        console.log('Project checkmark updated successfully.');
      },
      error: function(data) {
        console.log('Error updating project checkmark.');
      }
    });
  });
});