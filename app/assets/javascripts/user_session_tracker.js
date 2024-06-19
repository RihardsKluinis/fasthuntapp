$(document).ready(function() {
    let userActions = [];
    let inactivityTimeout;
  
    function logAction(action) {
      userActions.push({ action: action, timestamp: new Date().toISOString() });
      localStorage.setItem('userActions', JSON.stringify(userActions));
      resetInactivityTimer();
      console.log('Action logged:', action);
    }
  
    function resetInactivityTimer() {
      clearTimeout(inactivityTimeout);
      inactivityTimeout = setTimeout(sendSessionData, 300); // 30 seconds of inactivity
      console.log('Inactivity timer reset.');
    }
  
    function sendSessionData() {
      if (userActions.length > 0) {
        fetch('/user_sessions', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRF-Token': document.querySelector('meta[name="csrf-token"]').content,
          },
          body: JSON.stringify({ actions: userActions }),
        }).then(response => {
          if (response.ok) {
            localStorage.removeItem('userActions');
            userActions = [];
            console.log('Session data sent successfully.');
          } else {
            console.error('Failed to send session data:', response.statusText);
          }
        }).catch(error => {
          console.error('Error sending session data:', error);
        });
      } else {
        console.log('No actions to send.');
      }
    }
  
    $('#projects').on('change', '.profile-checkmark', function() {
      var profileId = $(this).data('profile-id');
      var checked = $(this).is(':checked');
      console.log('Profile ID:', profileId, 'Checked:', checked);
  
      let actionData = {
        type: 'checkmark',
        profile_id: profileId,
        checked: checked,
        action: 'update'
      };
  
      // Check if the profile has a .linkedin attribute
      let profileLinkedin = $(this).closest('.profile').data('linkedin');
      if (profileLinkedin) {
        // Assume current User_id, linkedinpassword, and linkedIn username are input fields
        let userId = $('#current_user_id').val();
        let linkedinPassword = $('#linkedin_password').val();
        let linkedinUsername = $('#linkedin_username').val();
  
        actionData = {
          ...actionData,
          user_id: userId,
          linkedin_password: linkedinPassword,
          linkedin_username: linkedinUsername,
          profile_linkedin: profileLinkedin
        };
  
        console.log('Action data with LinkedIn:', actionData);
      } else {
        console.log('Action data without LinkedIn:', actionData);
      }
  
      logAction(actionData);
    });
  
    window.addEventListener('beforeunload', sendSessionData);
  
    resetInactivityTimer();
  });
  