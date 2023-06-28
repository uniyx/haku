$(document).ready(function() {
    $('.sort-button').click(function() {
        var currentUrl = window.location.pathname;
        var sortType = $(this).data('sort');
        
        // Check if URL already has a sort parameter and remove it
        currentUrl = currentUrl.replace(/\/(new|top|hot)$/, '');
        
        // Append the new sort parameter
        window.location.href = currentUrl + '/' + sortType;
    })
})