$(document).ready(function() {
  $('#add_h1').on("click", function(e) {
    e.preventDefault();
    md_insert_h1_to("text");
  });

  $('#add_h2').on("click", function(e) {
    e.preventDefault();
    md_insert_h2_to('text');
  });

  $('#add_h3').on("click", function(e) {
    e.preventDefault();
    md_insert_h3_to('text');
  });

  $('#add_h4').on("click", function(e) {
    e.preventDefault();
    md_insert_h4_to('text');
  });

  $('#add_h5').on("click", function(e) {
    e.preventDefault();
    md_insert_h5_to('text');
  });

  $('#add_h6').on("click", function(e) {
    e.preventDefault();
    md_insert_h6_to('text');
  });

  $('#add_em').on("click", function(e) {
    e.preventDefault();
    md_insert_em_to('text');
  });

  $('#add_strong').on("click", function(e) {
    e.preventDefault();
    md_insert_strong_to('text');
  });

  $('#add_paragraph').on("click", function(e) {
    e.preventDefault();
    md_insert_paragraph_to('text');
  });

  $('#add_blockquote').on("click", function(e) {
    e.preventDefault();
    md_insert_blockquote_to('text');
  });

  $('#add_unord_list').on("click", function(e) {
    e.preventDefault();
    md_insert_unord_list_to('text');
  });

  $('#add_ord_list').on("click", function(e) {
    e.preventDefault();
    md_insert_ord_list_to('text');
  });

  $('#add_link').on("click", function(e) {
    e.preventDefault();
    md_insert_link_to('text');
  });
});

function md_insert_h1_to(element) {
  insertText(element, "\n# ", "\n", "H1")
}

function md_insert_h2_to(element) {
  insertText(element, "\n## ", "\n", "H2")
}

function md_insert_h3_to(element) {
  insertText(element, "\n### ", "\n", "H3")
}

function md_insert_h4_to(element) {
  insertText(element, "\n#### ", "\n", "H4")
}

function md_insert_h5_to(element) {
  insertText(element, "\n##### ", "\n", "H5")
}

function md_insert_h6_to(element) {
  insertText(element, "\n###### ", "\n", "H6")
}

function md_insert_em_to(element) {
  insertText(element, "*", "*", "italic")
}

function md_insert_strong_to(element) {
  insertText(element, "**", "**", "bold")
}

function md_insert_paragraph_to(element) {
  insertText(element, "\n", "\n\n", "paragraph")
}

function md_insert_blockquote_to(element) {
  insertText(element, "\n> ", "\n", "blockquote")
}

function md_insert_unord_list_to(element) {
  insertText(element, "\n* ", "\n", "element")
}

function md_insert_ord_list_to(element) {
  insertText(element, "\n1 ", "\n", "element")
}

function md_insert_link_to(element) {
  insertText(element, "[", "](http://link_address)", "link_name")
}

function insertText(element_name, before_text, after_text, default_text) {
  // get element by name
  var element = document.getElementsByName(element_name)[0];

  //IE specific patch: IE 9 etc.
  if (selection = document.selection) {
    IE_insertText(element, selection, before_text, after_text, default_text);
  //modern browsers
  } else if (element.selectionStart || element.selectionStart == '0') {
    var selection_from       = element.selectionStart;
    var selection_to         = element.selectionEnd;
    var val                  = element.value;
    var text_before_selected = val.substring(0, selection_from);
    var text_after_selected  = val.substring(selection_to, val.length);
    var selected_text        = val.substring(selection_from, selection_to);
    var content;

    // if we didn't select anything we add default text
    if (selection_from == selection_to) {
      content = default_text;
     // otherwise we use selected text  
    } else {
      content = selected_text;
    }

   // updating element value
    element.value = text_before_selected + before_text + content + 
                    after_text + text_after_selected;
    element.focus();

   // do highlight text
    element.selectionStart = selection_from + before_text.length;
    element.selectionEnd   = element.selectionStart + content.length;

    if (selection_from != selection_to) {
      window.getSelection().collapseToEnd();
    }
  //other ones?
  } else {
    alert("still not fully implemented"); 
  }
}



// special function for inserting text in Internet Explorer
function IE_insertText(element, selection, before_text, after_text, 
                       default_text) {
  // firstly have to focus on element to manipulate with range on it
  // otherwise it will break 
  element.focus();

  // grab current selection
  var range = selection.createRange();

  var content;
  // if we didn't select anything we add default text
  if (selection.type == 'None') {
    content = default_text;
  // otherwise we use selected text  
  } else {
    content = range.text;
  }

  // will highlight from that starting point
  var start = IE_currentCursorPosition(element, range.getBookmark());

  // we will highlight text after added before text markdown
  start += before_text.length;

  // highlight till content lenght
  var end = start + content.length;

  // if we selected some text do not highlight it after adding markdown to it
  // reposition cursor after added content
  if (selection.type != 'None') {
    start = end;
  }

  // update content of field
  range.text = before_text + content + after_text;

  // reintroduce in element proper selection of updated content
  // we need new text range
  var text_range = element.createTextRange();
  // do highlight text
  text_range.collapse(true);
  // set proper start and end points 
  text_range.moveEnd("character", end);
  text_range.moveStart("character", start);
  text_range.select();
}


// to calculate Internet Explorer cursor position,
// at the beginning of currently selected text
function IE_currentCursorPosition(element, range_bookmark) {
  var position  = 0;
  var range_dup = element.createTextRange();

  range_dup.moveToBookmark(range_bookmark);

  while (range_dup.moveStart('character' , -1) !== 0) {
    position++;
  }
  return position;
}