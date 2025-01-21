$(document).ready(function() {
    $(".like-button").click(function() {
        var postId = $(this).data("post-id");

        $.ajax({
            url: "{% url 'like_dislike' %}",
            type: "POST",
            data: {
                post_id: postId,
                action: 'like',
                csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val()
            },
            success: function(response) {

                $("#like-count-" + postId).val(response.new_likes);
            },
            error: function(response) {
                alert("Error: " + response.responseJSON.error);
            }
        });
    });


    $(".dislike-button").click(function() {
        var postId = $(this).data("post-id");

        $.ajax({
            url: "{% url 'like_dislike' %}",
            type: "POST",
            data: {
                post_id: postId,
                action: 'dislike',
                csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val()
            },
            success: function(response) {
                $("#dislike-count-" + postId).val(response.new_dislikes);
            },
            error: function(response) {
                alert("Error: " + response.responseJSON.error);
            }
        });
    });
});
