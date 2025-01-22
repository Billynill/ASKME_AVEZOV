<script>
$(document).ready(function() {
    $('.like-button').click(function() {
        const postId = $(this).data('post-id');
        updateLikes(postId, 'like');
    });


    $('.dislike-button').click(function() {
        const postId = $(this).data('post-id');
        updateLikes(postId, 'dislike');
    });


    function updateLikes(postId, action) {
        $.ajax({
            url: '/update_likes/',
            method: 'POST',
            data: {
                post_id: postId,
                action: action,
                csrfmiddlewaretoken: '{{ csrf_token }}'
            },
            success: function(response) {

                $('#like-count-' + postId).val(response.likes);
                $('#dislike-count-' + postId).val(response.dislikes);
            },
            error: function(xhr, status, error) {
                console.error('Ошибка при обновлении лайков:', error);
            }
        });
    }
});
</script>