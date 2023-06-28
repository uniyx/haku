function cardClick(event, element) {
    // If left mouse button is clicked
    if (event.button == 0) {
        // Navigate to link in same tab
        window.location.href = element.getAttribute('data-url');
    }
}

function updateButtonColors(postId, userVote) {
    var upvoteButton = document.querySelector(`[data-post-id="${postId}"][data-vote="1"]`);
    var downvoteButton = document.querySelector(`[data-post-id="${postId}"][data-vote="-1"]`);

    upvoteButton.classList.remove('text-primary');
    downvoteButton.classList.remove('text-danger');
    upvoteButton.classList.add('text-secondary');
    downvoteButton.classList.add('text-secondary');

    if (userVote == 1) {
        upvoteButton.classList.replace('text-secondary', 'text-primary');
    } else if (userVote == -1) {
        downvoteButton.classList.replace('text-secondary', 'text-danger');
    }
}

function vote(button) {
    var postId = button.getAttribute("data-post-id");
    var vote = button.getAttribute("data-vote");

    $.ajax({
        url: '/vote',
        data: JSON.stringify({ 'post_id': postId, 'value': vote }),
        type: 'POST',
        contentType: 'application/json',
        success: function (response) {
            $('#vote-score-' + postId).html(response.new_score);
            updateButtonColors(postId, response.user_vote);
        },
        error: function (error) {
            console.log(error);
        }
    });

    button.disabled = false;
}

function toggleExpandIcon(button) {
    var icon = $(button).find('i');

    if (icon.hasClass('fa-up-right-and-down-left-from-center')) {
        icon.removeClass('fa-up-right-and-down-left-from-center');
        icon.addClass('fa-down-left-and-up-right-to-center');
    } else {
        icon.removeClass('fa-down-left-and-up-right-to-center');
        icon.addClass('fa-up-right-and-down-left-from-center');
    }
}

function savePost(button) {
    var postId = button.getAttribute("data-post-id");

    $.ajax({
        url: '/save_post',
        data: JSON.stringify({ 'post_id': postId }),
        type: 'POST',
        contentType: 'application/json',
        success: function (response) {
            if (response.saved) {
                $(button).removeClass('text-secondary').addClass('text-success');
            } else {
                $(button).removeClass('text-success').addClass('text-secondary');
            }
        },
        error: function (error) {
            console.log(error);
        }
    });
}

$(document).ready(function() {
    $('.sort-button').click(function() {
        var currentUrl = window.location.href;
        var sortType = $(this).data('sort');
        
        console.log("Current URL: " + currentUrl);
        console.log("Sort type: " + sortType);

        if (currentUrl.endsWith('/')) {
            currentUrl = currentUrl.slice(0, -1);
        }
        
        // Check if URL already has a sort parameter and remove it
        currentUrl = currentUrl.replace(/\/(new|top|hot)$/, '');
        
        // Append the new sort parameter
        var newUrl = currentUrl + '/' + sortType;
        console.log("New URL: " + newUrl);
        
        window.location.href = newUrl;
    });
});