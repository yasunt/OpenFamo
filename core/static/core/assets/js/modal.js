<script>
  $(document).ready(function() {
    $('#command').click(function() {
        $.ajax({
          'url': "{% url 'posts:last_answer' %}",
          'type': 'POST',
          'data': {
            csrfmiddlewaretoken: '{{ csrf_token }}',
            'question_id': '{{ question.id }}',
          },
          'dataType': 'json',
          'success': function(response) {
            $('#content').val(response.content);
          }
        })
    })
    $('#submit').click(function() {
      $.ajax({
        'url': "{% url 'counsel:post_answer' %}",
        'type': 'POST',
        'data': {
          csrfmiddlewaretoken: '{{ csrf_token }}',
          'question_id': '{{ question.id }}',
          'content': $("#content").val(),
          'anonymous': $('#demo-human').is(":checked"),
        },
        'dataType': 'json',
        'success': function(response) {
          $('#close').click();
          location.reload();
        }
      });
    });
    $("[id^='good_button']").click(function() {
        if (!'{{ request.user.is_authenticated }}') {
          $('#command').click();
        }
        else {
          var target = this;
          $.ajax({
            'url': "{% url 'posts:evaluate' %}",
            'type': 'POST',
            'data': {
              csrfmiddlewaretoken: '{{ csrf_token }}',
              'user_id': '{{ user.id }}',
              'answer_id': target.id.replace('good_button', ''),
            },
            'dataType': 'json',
            'success': function(response) {
              $(target).text('Good ' + '+' + response.good_rators_count);
              if (response.is_evaluated) {
                target.className = 'button special small';
              }
              else {
                target.className = 'button small';
              }
            }
        });
      }
    });
  });
</script>
