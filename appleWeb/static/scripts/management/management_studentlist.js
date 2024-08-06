document.querySelectorAll('.school-button').forEach(button => {
    button.addEventListener('click', function() {
        const alreadyActive = this.classList.contains('active');
        // 'active' 클래스 제거
        document.querySelectorAll('.school-button').forEach(b => b.classList.remove('active'));
        document.querySelectorAll('.grade-button').forEach(b => b.classList.remove('active'));

        const tableBody = document.querySelector('#student-table tbody');
        tableBody.innerHTML = '';

        // 클릭된 버튼의 현재 상태에 따라 'active' 클래스 토글 및 grade-buttons 표시 조정
        if (!alreadyActive) {
            this.classList.add('active');
            document.getElementById('grade-buttons').style.display = 'flex';
            document.getElementById('student-table').style.display = '';
            
        } else {
            document.getElementById('grade-buttons').style.display = 'none';
            document.getElementById('student-table').style.display = 'none';
        }

        // 학년 버튼의 onclick 이벤트 설정
        document.querySelectorAll('.grade-button').forEach(gbutton => {
            gbutton.onclick = function() {
                const alreadyActive = this.classList.contains('active');
                
                document.querySelectorAll('.grade-button').forEach(b => b.classList.remove('active'));
                const grade = this.getAttribute('data-grade');
                const selectedSchool = document.querySelector('.school-button.active') ? document.querySelector('.school-button.active').getAttribute('data-school') : null;

                if(selectedSchool && !alreadyActive) {
                    this.classList.add('active');
                    document.getElementById('student-table').style.display = '';
                    fetchStudents(selectedSchool, grade);
                } else {
                    document.getElementById('student-table').style.display = 'none';
                    console.error("No school is selected");
                }
            };
        });
    });
});


function fetchStudents(school, grade) {
    // AJAX를 사용하여 서버에서 학생 데이터를 가져오고 테이블에 표시
    fetch(`/management/api/students?school=${school}&grade=${grade}`, {
        credentials: 'include'  // 쿠키를 포함하여 요청
    })
    .then(response => {
        console.log('Response:', response);
        return response.text();  // 응답을 텍스트로 변환
    })
    .then(data => {
        console.log('Data:', data);  // 변환된 텍스트 데이터 출력
        try {
            const jsonData = JSON.parse(data);  // 텍스트 데이터를 JSON으로 파싱
            const tableBody = document.getElementById('student-table').getElementsByTagName('tbody')[0];
            tableBody.innerHTML = ''; // Clear existing rows
            jsonData.forEach(student => {
                const row = tableBody.insertRow();
                row.innerHTML = `
                    <td>${student.school}</td>
                    <td>${student.grade}</td>
                    <td>${student.name}</td>
                    <td>${student.phone}</td>
                    <td>${student.parent_phone}</td>
                    <td>${student.payment_count}</td>
                `;
                // Click on a student row to view more details
                row.onclick = () => {
                    window.location.href = `/management/student_detail/${student.id}/`;
                };
            });
            document.getElementById('student-table').style.display = 'table';
        } catch (error) {
            console.error('Error parsing JSON:', error);  // JSON 파싱 오류 로그
        }
    })
    .catch(error => {
        console.error('Error fetching students:', error);
    });
}
