$(document).ready(function () {
  var table = $("#emailTable").DataTable({
    lengthChange: false,
    pageLength: 10,
    info: false,
    language: {
      paginate: {
        previous: "Prev",
        next: "Next",
      },
    },
  });
});

function showDeleteModal(event, email) {
  event.preventDefault();
  $("#deleteEmail").text(email);
  my_modal_1.showModal();
}

$("#confirmDeleteButton").on("click", function (event) {
  event.preventDefault();
  var email = $("#deleteEmail").text();
  var url = "/email-data/email/" + encodeURIComponent(email) + "/delete/";
  $.ajax({
    url: url,
    type: "POST",
    data: $("#deleteForm").serialize(),
    success: function (response) {
      my_modal_1.close();
      Swal.fire({
        icon: "success",
        title: "Deleted!",
        text: "The email has been deleted successfully.",
        confirmButtonColor: "#DD6B20",
      }).then(() => {
        location.reload();
      });
    },
    error: function (xhr, status, error) {
      console.error(xhr.responseText);
      my_modal_1.close();
      Swal.fire({
        icon: "error",
        title: "Error!",
        text: "An error occurred while trying to delete the email. Please try again.",
        confirmButtonColor: "#d33",
      });
    },
  });
});
