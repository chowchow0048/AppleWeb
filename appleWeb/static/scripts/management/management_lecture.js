document.addEventListener("DOMContentLoaded", function() {
    const attendanceCheckboxes = document.querySelectorAll(".attendance-checkbox");
    const attendanceAllCheckButton = document.getElementById("selectAllAttendance");
    const day = new Date().toLocaleDateString('ko-KR', { weekday: 'long' }).toLowerCase();
    const courseDay = document.getElementById("course-title").innerHTML.split(' ')[5];

    attendanceAllCheckButton.addEventListener("click", function() {
        attendanceCheckboxes.forEach(checkbox => {
            checkbox.checked = true;
        });
    });

    attendanceCheckboxes.forEach(checkbox => {
        if(day != courseDay) {
            checkbox.disabled = true;
        }
    });

    document.getElementById("submitAttendance").addEventListener("click", function() {
        const course = document.getElementById('course-title')
        const attendanceCount = document.querySelectorAll(".attendance-checkbox:checked").length;
        const totalStudents = document.querySelectorAll(".attendance-checkbox").length;
        const absenceCount = totalStudents - attendanceCount;
        
        const absentStudents = Array.from(document.querySelectorAll(".attendance-checkbox:not(:checked)")).map(checkbox => {
            const studentRow = checkbox.closest("tr");
            const studentName = studentRow.querySelector("td:nth-child(4)").textContent;
            return `${studentName.trim()} (ID: ${checkbox.value})`;
        }).join("\n");

        if (confirm(`출석: ${attendanceCount}명\n결석: ${absenceCount}명\n\n결석자 정보:\n${absentStudents}\n\n출결 처리를 진행하시겠습니까?`)) {
            document.getElementById("attendanceForm").submit();
            alert(`${course.innerText} 수업의 출결처리가 완료되었습니다`);
        }
    });
});