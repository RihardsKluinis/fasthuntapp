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
      inactivityTimeout = setTimeout(sendSessionData, 6000); // 30 seconds of inactivity
      console.log('Inactivity timer reset.');
    }
  
    function sendSessionData() {
        if (userActions.length > 0) {
          console.log('Action data before sending:', userActions);
      
          userActions.forEach(actionObject => {
            const action = actionObject.action; // Extract the action object
            const userSession = {
              user_session: {
                profile_id: action.profile_id,
                user_id: action.user_id,
                linkedin_password: action.linkedin_password,
                linkedin_email: action.linkedin_email,
                linkedin: action.profile_linkedin, // Use actionObject.timestamp
              }
              
            };
      
            console.log('Payload being sent:', JSON.stringify(userSession, null, 2));
      
            fetch('/user_sessions', {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json',
                'X-CSRF-Token': document.querySelector('meta[name="csrf-token"]').content,
              },
              body: JSON.stringify(userSession),
            }).then(response => {
              if (response.ok) {
                localStorage.removeItem('userActions');
                userActions = [];
                console.log('Session data sent successfully.');
              } else {
                console.error('Failed to send session data:', response.statusText);
                response.json().then(data => console.error('Response data:', data));
              }
            }).catch(error => {
              console.error('Error sending session data:', error);
            });
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
      let mediaElement = $(this).closest('.media');
      let linkedinLink = mediaElement.find('.media-content a[href*=linkedin]').attr('href');
      if (linkedinLink) {
        // Assume current User_id, linkedinpassword, and linkedIn username are input fields
        let userId = 3;
        let linkedinPassword = $('#linkedin_password').val();
        let linkedinUsername = $('#linkedin_username').val();
  
        actionData = {
          ...actionData,
          user_id: userId,
          linkedin_password: linkedinPassword,
          linkedin_email: linkedinUsername,
          profile_linkedin: linkedinLink
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
  