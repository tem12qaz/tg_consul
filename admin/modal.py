html = '''<style>
body {font-family: Arial, Helvetica, sans-serif;}

/* The Modal (background) */
.modal_chat_read {
  display: none; /* Hidden by default */
  position: fixed; /* Stay in place */
  z-index: 1; /* Sit on top */
  padding-top: 100px; /* Location of the box */
  left: 0;
  top: 0;
  width: 100%; /* Full width */
  height: 100%; /* Full height */
  overflow: auto; /* Enable scroll if needed */
  background-color: rgb(0,0,0); /* Fallback color */
  background-color: rgba(0,0,0,0.4); /* Black w/ opacity */
}

/* Modal Content */
.modal-content_chat_read {
  background-color: #fefefe;
  margin: auto;
  padding: 20px;
  border: 1px solid #888;
  width: 80%;
}

/* The Close Button */
.close_chat_readid_replace {
  color: #aaaaaa;
  float: right;
  font-size: 28px;
  font-weight: bold;
}

.close_chat_readid_replace:hover,
.close_chat_readid_replace:focus {
  color: #000;
  text-decoration: none;
  cursor: pointer;
}
</style>
</head>
<body>
<!-- Trigger/Open The Modal -->
<button id="myBtnid_replace">Read</button>

<!-- The Modal -->
<div id="myModalid_replace" class="modal_chat_read">

  <!-- Modal content -->
  <div class="modal-content_chat_read">
    <span class="close_chat_readid_replace">&times;</span>
    <p>to_replace</p>
  </div>

</div>

<script>
// Get the modal
var modalid_replace = document.getElementById("myModalid_replace");

// Get the button that opens the modal
var btnid_replace = document.getElementById("myBtnid_replace");

// Get the <span> element that closes the modal
var spanid_replace = document.getElementsByClassName("close_chat_readid_replace")[0];

// When the user clicks the button, open the modal
btnid_replace.onclick = function() {
  modalid_replace.style.display = "block";
}

// When the user clicks on <span> (x), close the modal
spanid_replace.onclick = function() {
  modalid_replace.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  if (event.target == modalid_replace) {
    modalid_replace.style.display = "none";
  }
}
</script>'''