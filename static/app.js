$('.ui.checkbox:not(.vue)')
  .checkbox()
;

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