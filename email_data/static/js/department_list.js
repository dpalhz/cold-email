/*
Edit Mode: Menggunakan data attribute (data-edit-mode) untuk menandai apakah form sedang dalam mode edit atau create.
Autofill Data: Ketika tombol edit diklik, form akan diisi dengan data department yang sesuai menggunakan AJAX request.
Submit Form: Menggunakan AJAX untuk melakukan request PUT jika dalam mode edit, atau POST jika dalam mode create.
Helper Functions:

toggleCreateForm(): Mengatur tampilan form tergantung pada apakah sedang dalam mode edit atau create.
resetForm(): Mereset form ketika user membatalkan atau selesai melakukan edit.
*/

$(document).ready(function () {
  // Handle create/edit button click
  $("#createDepartmentButton").on("click", function (event) {
    event.preventDefault();
    resetForm();
    $("#modeSubmit").text("Save");
    $("#formTitle").text("Create Department");
    console.log($(this).text());
    if ($(this).text() === "<") {
      toggleCreateForm(false);
    } else {
      console.log("testing");
      toggleCreateForm(true);
    }
  });

  $("#cancelCreateDepartmentButton").on("click", function (event) {
    event.preventDefault();
    resetForm();
    toggleCreateForm();
  });

  // Submit create or edit form
  $("#createDepartmentForm").on("submit", function (event) {
    event.preventDefault();
    const isEditMode = $(this).data("edit-mode");
    const departmentId = $(this).data("department-id");
    const csrftoken = getCSRFToken();

    const url = isEditMode
      ? `/email-data/department/edit/${departmentId}/`
      : "/email-data/department/create/";

    $.ajax({
      url: url,
      type: "POST",
      data: $(this).serialize(),
      headers: {
        "X-CSRFToken": csrftoken,
      },
      success: function (response) {
        Swal.fire({
          icon: "success",
          title: isEditMode ? "Department Updated!" : "Department Created!",
          text: `The department has been ${
            isEditMode ? "updated" : "created"
          } successfully.`,
          confirmButtonColor: "#030712",
        }).then(() => {
          location.reload(); // Reload page untuk memperbarui data department
        });
      },
      error: function (xhr, status, error) {
        Swal.fire({
          icon: "error",
          title: "Error!",
          text: `An error occurred while trying to ${
            isEditMode ? "update" : "create"
          } the department. Please try again.`,
          confirmButtonColor: "#d33",
        });
      },
    });
  });

  $(".editButton").on("click", function (event) {
    event.preventDefault();
    const $li = $(this).closest("li");
    const departmentId = $(this).data("id");
    const departmentNama = $li.data("nama");
    const departmentDeskripsi = $li.data("deskripsi");

    $("#modeSubmit").text("Edit");
    $("#formTitle").text("Edit Department");

    // Autofill form fields
    $("#id_nama").val(departmentNama);
    $("#id_deskripsi").val(departmentDeskripsi);

    $("#createDepartmentForm")
      .data("edit-mode", true)
      .data("department-id", departmentId);
    toggleCreateForm(true);
  });

  function getCSRFToken() {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
      const cookies = document.cookie.split(";");
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, 10) === "csrftoken=") {
          cookieValue = decodeURIComponent(cookie.substring(10));
          break;
        }
      }
    }
    return cookieValue;
  }

  // Event handler untuk tombol delete
  $(".deleteButton").on("click", function (event) {
    event.preventDefault();
    const departmentId = $(this).data("id");
    const csrftoken = getCSRFToken();
    Swal.fire({
      title: "Are you sure?",
      text: "You won't be able to revert this!",
      icon: "warning",
      showCancelButton: true,
      confirmButtonColor: "#d33",
      cancelButtonColor: "#030712",
      confirmButtonText: "Yes, delete it!",
    }).then((result) => {
      if (result.isConfirmed) {
        $.ajax({
          url: `/email-data/department/delete/${departmentId}/`, // URL view delete department
          type: "DELETE",
          headers: {
            "X-CSRFToken": csrftoken,
          },
          success: function (response) {
            Swal.fire({
              title: "Deleted!",
              text: "The department has been deleted.",
              icon: "success",
              confirmButtonColor: "#030712",
            }).then(() => {
              location.reload(); // Reload page untuk memperbarui data department
            });
          },
          error: function (xhr, status, error) {
            Swal.fire({
              icon: "error",
              title: "Error!",
              text: "An error occurred while trying to delete the department. Please try again.",
              confirmButtonColor: "#030712",
            });
          },
        });
      }
    });
  });

  // Helper functions
  function toggleCreateForm(showForm = false) {
    if (showForm) {
      $("#createDepartmentFormContainer").show();
      $("#createDepartmentButton")
        .text("<")
        .removeClass("bg-orange-500 hover:bg-orange-600 hover:text-orange-100")
        .addClass("bg-red-600 hover:bg-red-700 hover:text-red-100");
    } else {
      $("#createDepartmentFormContainer").toggle();
      $("#createDepartmentButton")
        .text("+")
        .removeClass("bg-red-600 hover:bg-red-700 hover:text-red-100")
        .addClass("bg-orange-500 hover:bg-orange-600 hover:text-orange-100");
    }
  }

  function resetForm() {
    $("#createDepartmentForm")[0].reset();
    $("#createDepartmentForm")
      .data("edit-mode", false)
      .removeData("department-id");
  }
});
