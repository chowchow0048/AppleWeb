let studentsData = [];  // 불러온 학생 데이터를 저장할 전역 변수

// 학교 버튼 클릭 이벤트
document.querySelectorAll('.school-button').forEach(button => {
    button.addEventListener('click', function() {
        const alreadyActive = this.classList.contains('active');
        document.querySelectorAll('.school-button').forEach(b => b.classList.remove('active'));
        document.querySelectorAll('.grade-button').forEach(b => b.classList.remove('active'));
        document.querySelectorAll('.sort-button').forEach(b => b.classList.remove('active'));

        const tableBody = document.querySelector('#student-table tbody');
        tableBody.innerHTML = '';  // 기존 데이터를 초기화

        if (!alreadyActive) {
            this.classList.add('active');
            document.getElementById('grade-buttons').style.display = 'flex';
        } else {
            document.getElementById('sort-buttons').style.display = 'none';
            document.getElementById('grade-buttons').style.display = 'none';
            document.getElementById('student-table').style.display = 'none';
        }

        document.querySelectorAll('.grade-button').forEach(gbutton => {
            gbutton.onclick = function() {
                const alreadyActive = this.classList.contains('active');
                document.querySelectorAll('.grade-button').forEach(b => b.classList.remove('active'));

                const grade = this.getAttribute('data-grade');
                const selectedSchool = document.querySelector('.school-button.active') ? document.querySelector('.school-button.active').getAttribute('data-school') : null;

                if (selectedSchool && !alreadyActive) {
                    console.log(selectedSchool, alreadyActive);
                    this.classList.add('active');
                    const searchForm = document.getElementById('search-form');
                    searchForm.style.display = '';  // 표시
                    searchForm.classList.add('flex-row');  // flex-row 클래스 추가
                    fetchStudents(selectedSchool, grade);  // 학생 정보 불러오기
                } else {
                    const searchForm = document.getElementById('search-form');
                    searchForm.style.display = 'none';  // 숨김
                    searchForm.classList.remove('flex-row');  // flex-row 클래스 제거
                    document.getElementById('student-table').style.display = 'none';
                }
            };
        });

        // 정렬 버튼 클릭 이벤트
        document.querySelectorAll('.sort-button').forEach(button => {
            button.addEventListener('click', function() {
                document.querySelectorAll('.sort-button').forEach(b => b.classList.remove('active'));
                this.classList.add('active');

                const sortValue = this.getAttribute('value');
                const sortedData = sortStudents(studentsData, sortValue);
                renderTable(sortedData);
            });
        });
    });
});

// 학생 데이터를 불러오는 함수
function fetchStudents(school, grade) {
    $.ajax({
        url: '/management/api/students/',
        type: 'GET',
        dataType: 'json',
        data: {
            'school': school,
            'grade': grade
        },
        success: function(data) {
            studentsData = data;  // 불러온 데이터를 전역 변수에 저장
            renderTable(studentsData);  // 처음에는 정렬 없이 바로 테이블에 렌더링
            document.getElementById('student-table').style.display = 'table';
        },
        error: function(request, status, error) {
            console.error('Error fetching students:', error);
        }
    });
}

// 검색 기능
document.getElementById('student-search').addEventListener('input', function() {
    const searchValue = this.value.toLowerCase();
    const filteredData = studentsData.filter(student => student.name.toLowerCase().includes(searchValue));
    renderTable(filteredData);
});


// 학생 데이터를 테이블에 렌더링하는 함수
function renderTable(data) {
    const tableBody = document.getElementById('student-table').getElementsByTagName('tbody')[0];
    tableBody.innerHTML = '';  // 기존 데이터를 초기화

    data.forEach(student => {
        const row = tableBody.insertRow();
        row.innerHTML = `
            <td>${student.school}</td>
            <td>${student.grade}</td>
            <td>${student.name}</td>
            <td>${student.phone}</td>
            <td>${student.parent_phone}</td>
            <td>${student.payment_count}</td>
        `;
        row.onclick = () => {
            window.location.href = `/management/student_detail/${student.id}/`;
        };
    });
}

// 정렬 로직을 처리하는 함수
function sortStudents(data, sortBy) {
    return data.slice().sort((a, b) => {
        if (sortBy === 'name-asc') {
            return a.name.localeCompare(b.name);  // 이름 오름차순
        } else if (sortBy === 'name-desc') {
            return b.name.localeCompare(a.name);  // 이름 내림차순
        } else if (sortBy === 'payment-asc') {
            return a.payment_count - b.payment_count;  // 결제 횟수 오름차순
        } else if (sortBy === 'payment-desc') {
            return b.payment_count - a.payment_count;  // 결제 횟수 내림차순
        }
        return 0;
    });
}