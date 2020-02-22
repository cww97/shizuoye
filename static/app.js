$('.ui.checkbox:not(.vue)')
  .checkbox()
;

$('.ui.dropdown').dropdown();

$('.captcha-refresh, img.captcha').click(function(){
    var $form = $(this).parents('form');
    $.getJSON("/captcha/refresh/", {}, function(json) {
        $form.find('input[name="captcha_0"]').val(json.key);
        $form.find('img.captcha').attr('src', json.image_url);
    });
    return false;
});

$('#navbar-small>.dropdown').dropdown();

// File input
$.fn.inputFile = function(data) {
  var sizeLimit = -1;
  if (data !== undefined && data.hasOwnProperty("sizeLimit")) {
    sizeLimit = parseInt(data["sizeLimit"]);
  }
  function changeFunction(e) {
    var file = $(e.target);
    var name = '';
    var size = 0;
    for (var i = 0; i < e.target.files.length; i++) {
      name += e.target.files[i].name + (i + 1 == e.target.files.length ? '' : ', ');
      size += e.target.files[i].size / 1048576;
    }
    $('input:text', file.parent()).val(name);
    if (sizeLimit > 0 && size > sizeLimit) {
      window.alert("File too large! If you insist on uploading, it is likely to fail...");
    }
  }
  if (!this.prop("init")) {
    this.prop("init", true);
    this.find('input:text, .ui.button:not([type="submit"])')
      .on('click', function (e) {
        $(e.target).parent().find('input:file').click();
      })
    ;
    this.on('change', changeFunction);
    this.find('.ui.file.input').on('change', changeFunction);
  }
};
$(".ui.file.input").inputFile();

// editor
$.fn.simpleMDE = function () {
  $(this).each(function () {
    let simplemde = new SimpleMDE({
      element: this,
      forceSync: true,
      spellChecker: false,
      previewRender: function (plainText, preview) {
        $.post("/api/markdown/", {
          s: plainText || ""
        }, function (data) {
          // console.log(data);
          preview.innerHTML = data;
        }.bind(this));
        return "Loading...";
      }
    });
  });
};

$("textarea.markdown").simpleMDE();

// function post and modal related
function postWithLocalData (button) {
  var link = button.data('link');
  var data = button.data();
  data['csrfmiddlewaretoken'] = Cookies.get('csrftoken');
  $.post(link, data, function (data) {
      location.reload();
    }
  );
}

$(".post-link")
  .on('click', function(e) {
    postWithLocalData($(e.currentTarget));
  })
  .attr('href', 'javascript:void(0)');

  $(".modal-link")
  .on('click', function (e) {
    var button = $(e.currentTarget);
    var modal = $(button.data('target'));
    if (button.data('action'))
      modal.find("form").attr("action", button.data('action'));
    if (modal.find("form").length > 0)
      replaceFormData(modal.find("form"), button.data());
    modal
      .modal({
        onApprove: function () {
          var form = $(this).find("form");
          var data = new FormData(form[0]);
          $.ajax({
            url: form.attr("action"),
            type: 'POST',
            data: data,
            processData: false,
            contentType: false,
            success: function (data) {
              if (data.redirect) {
                window.location.href = data.redirect;
              } else {
                location.reload();
              }
            }
          });
        }
      })
      .modal('show');
  })
  .attr('href', 'javascript:void(0)');


$(".post, .get").on('click', function (event) {
    var button = $(event.currentTarget);
    var method = button.hasClass("post") ? "post" : "get";
    var link = button.data("link");
    var extra_input = {};
    if (button.hasClass("gather")) {
      // gather all checkbox information
      extra_input["gather"] = $.makeArray($("input[type='checkbox']").map(function() {
        return this.checked ? this.name : "";
      })).filter(function(n) {
        return n != "all" && n != "";
      }).join(",");
      if (!extra_input["gather"]) {
        alert("Please select cases first!");
        return;
      }
    }
    if (button.hasClass("ask")) {
      extra_input["answer"] = prompt(button.data("question") || "");
      console.log(extra_input["answer"] !== null);
      if (extra_input["answer"] !== null)
        redirect(link, method, extra_input);
    } else if (button.hasClass("prompt")) {
      if (confirm("Are you sure about this?"))
        redirect(link, method, extra_input);
    } else {
      redirect(link, method, extra_input);
    }
  }).attr('href', 'javascript:void(0)');