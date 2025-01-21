$(document).ready(function() {
    // Обработка клика по кнопке лайка
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
                // Обновляем количество лайков
                $("#like-count-" + postId).val(response.new_likes);
            },
            error: function(response) {
                alert("Error: " + response.responseJSON.error);
            }
        });
    });

    // Обработка клика по кнопке дизлайка
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
                // Обновляем количество дизлайков
                $("#dislike-count-" + postId).val(response.new_dislikes);
            },
            error: function(response) {
                alert("Error: " + response.responseJSON.error);
            }
        });
    });
});
