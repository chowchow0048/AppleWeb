document.addEventListener("DOMContentLoaded", function() {
    const selectAllButton = document.getElementById("selectAllPayments");
    const processPaymentsButton = document.getElementById("processPayments");
    const paymentCheckboxes = document.querySelectorAll(".payment-checkbox");
    const searchInput = document.getElementById('pl-search');
    const schoolButtons = document.querySelectorAll('.pl-btn-school');
    const tableBody = document.getElementById("mngpl-tbody");

    let selectedSchool = '';  // 선택된 학교 필터
    let searchQuery = '';  // 검색어

    // 학교 버튼 클릭 시 필터링
    schoolButtons.forEach(button => {
        button.addEventListener('click', function () {
            if (selectedSchool === this.textContent) {
                selectedSchool = '';  // 같은 학교 버튼을 다시 클릭하면 필터 해제
            } else {
                selectedSchool = this.textContent;  // 선택된 학교 업데이트
            }
            updateSchoolButtonFocus();
            fetchData(selectedSchool, searchQuery);  // 데이터를 다시 로드
        });
    });

    // 검색창 입력 시
    searchInput.addEventListener('input', function () {
        searchQuery = this.value.toLowerCase();  // 검색어 업데이트
        fetchData(selectedSchool, searchQuery);  // 데이터를 다시 로드
    });

    // 전체 선택/해제 버튼
    selectAllButton.addEventListener("click", function() {
        const allChecked = Array.from(paymentCheckboxes).every(checkbox => checkbox.checked);
        paymentCheckboxes.forEach(checkbox => {
            checkbox.checked = !allChecked;
        });
    });

    // 결제 처리 버튼
    processPaymentsButton.addEventListener("click", function() {
        const selectedUsers = Array.from(paymentCheckboxes)
                                   .filter(checkbox => checkbox.checked)
                                   .map(checkbox => ({
                                       id: checkbox.getAttribute("data-user-id"),
                                       school: checkbox.closest("tr").querySelector("td:nth-child(1)").textContent,
                                       grade: checkbox.closest("tr").querySelector("td:nth-child(2)").textContent,
                                       name: checkbox.closest("tr").querySelector("td:nth-child(3)").textContent,
                                   }));

        if (selectedUsers.length > 0) {
            const userDetails = selectedUsers.map(user => `${user.school} ${user.grade} ${user.name}`).join("\n");
            const message = `${selectedUsers.length}명의 결제를 진행하시겠습니까?\n\n결제 학생 목록:\n${userDetails}`;

            if (confirm(message)) {
                selectedUsers.forEach(user => {
                    processPayment(user.id);
                });
            }
        } else {
            alert("결제 확인할 학생을 선택하세요.");
        }
    });

    // 결제 처리 함수
    function processPayment(userId) {
        fetch(`/management/confirm-payment/${userId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'Content-Type': 'application/json'
            },
        })
        .then(response => response.json())
        .then(data => {
            location.reload();
        })
        .catch(error => console.error('Error:', error));
    }

    // CSRF 토큰 가져오기
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // 학교 버튼 포커스 업데이트
    function updateSchoolButtonFocus() {
        schoolButtons.forEach(btn => {
            if (btn.textContent === selectedSchool) {
                btn.classList.add('school-focused');
            } else {
                btn.classList.remove('school-focused');
            }
        });
    }

    // 데이터를 서버에서 가져오는 함수 (AJAX 요청)
    function fetchData(selectedSchool, searchQuery) {
        const url = '/management/paylist/fetch/';  // 서버에서 데이터를 가져오는 URL
        console.log('Fetching data with:', selectedSchool, searchQuery);  // 디버깅 로그

        // AJAX 요청
        $.ajax({
            url: url,
            type: 'GET',
            dataType: 'json',
            data: {
                school: selectedSchool,  // 선택된 학교
                query: searchQuery  // 검색어
            },
            success: function(data) {
                renderTable(data);  // 데이터를 성공적으로 받아오면 테이블 렌더링
            },
            error: function(request, status, error) {
                console.error('Error fetching data:', error);
                console.log('Request details:', request.responseText);  // 요청 상세 정보
            }
        });
    }

    // 테이블을 렌더링하는 함수
    function renderTable(data) {
        tableBody.innerHTML = '';  // 기존 데이터를 초기화
        data.forEach(user => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td class='pl-td-school'>${user.school}</td>
                <td class='pl-td-grade'>${user.grade}</td>
                <td class='pl-td-name' onclick="location.href='/management/student_detail/${user.id}/'" style="cursor: pointer;">${user.name}</td>
                <td class='pl-td-phone'>${user.phone ? user.phone : '-'}</td>
                <td class='pl-td-parentphone'>${user.parent_phone}</td>
                <td class='pl-td-paymentcount'>${user.payment_count}</td>
                <td class='pl-td-checkbox'><input type="checkbox" class="payment-checkbox" data-user-id="${user.id}"></td>
            `;
            tableBody.appendChild(row);
        });
    }

    // 페이지가 로드될 때 데이터를 가져옴 (기본 설정)
    fetchData('', '');  // 모든 데이터를 가져옴
});
