document.addEventListener("DOMContentLoaded", function() {
    const attendanceCheckboxes = document.querySelectorAll(".attendance-checkbox");
    const absenceCheckboxes = document.querySelectorAll(".absence-checkbox");

    document.getElementById("selectAllAttendance").addEventListener("click", function() {
        attendanceCheckboxes.forEach(checkbox => {
            checkbox.checked = true;
            const studentId = checkbox.getAttribute("data-student-id");
            const correspondingAbsenceCheckbox = document.querySelector(`.absence-checkbox[data-student-id="${studentId}"]`);
            correspondingAbsenceCheckbox.checked = false;
        });
    });

    document.getElementById("selectAllAbsence").addEventListener("click", function() {
        absenceCheckboxes.forEach(checkbox => {
            checkbox.checked = true;
            const studentId = checkbox.getAttribute("data-student-id");
            const correspondingAttendanceCheckbox = document.querySelector(`.attendance-checkbox[data-student-id="${studentId}"]`);
            correspondingAttendanceCheckbox.checked = false;
        });
    });

    attendanceCheckboxes.forEach(checkbox => {
        checkbox.addEventListener("change", function() {
            const studentId = this.getAttribute("data-student-id");
            const correspondingAbsenceCheckbox = document.querySelector(`.absence-checkbox[data-student-id="${studentId}"]`);
            if (this.checked) {
                correspondingAbsenceCheckbox.checked = false;
            }
        });
    });

    absenceCheckboxes.forEach(checkbox => {
        checkbox.addEventListener("change", function() {
            const studentId = this.getAttribute("data-student-id");
            const correspondingAttendanceCheckbox = document.querySelector(`.attendance-checkbox[data-student-id="${studentId}"]`);
            if (this.checked) {
                correspondingAttendanceCheckbox.checked = false;
            }
        });
    });

    document.getElementById("submitAttendance").addEventListener("click", function() {
        const course = document.getElementById('course-title')
        const attendanceCount = document.querySelectorAll(".attendance-checkbox:checked").length;
        const absenceCount = document.querySelectorAll(".absence-checkbox:checked").length;
        const absenceDetails = Array.from(document.querySelectorAll(".absence-checkbox:checked")).map(checkbox => {
            const studentId = checkbox.getAttribute("data-student-id");
            const studentName = checkbox.closest("tr").querySelector("td:nth-child(4)").textContent;
            return `${studentName} (ID: ${studentId})`;
        }).join("\n");

        if (confirm(`출석: ${attendanceCount}명\n결석: ${absenceCount}명\n\n결석자 정보:\n${absenceDetails}\n\n출결 처리를 진행하시겠습니까?`)) {
            document.getElementById("attendanceForm").submit();
            alert(`${course.innerText} 수업의 출결처리가 완료되었습니다`);
        }
    });
});
