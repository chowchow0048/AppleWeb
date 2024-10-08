document.addEventListener('DOMContentLoaded', function () {
    const wbWaitBtn = document.getElementById('wb-wait');
    const wbBlackBtn = document.getElementById('wb-black');
    const tableBody = document.getElementById('wb-tbody');
    const searchInput = document.getElementById('wb-search');
    const schoolButtons = document.querySelectorAll('.wb-btn-school');
    
    let isWaitlist = true;  // 대기리스트가 기본 상태
    let selectedSchool = '';  // 선택된 학교 필터
    let searchQuery = '';  // 검색어

    // 대기리스트 버튼 클릭 시
    wbWaitBtn.addEventListener('click', function () {
        isWaitlist = true;
        wbWaitBtn.classList.add('focused');
        wbBlackBtn.classList.remove('focused');  // 블랙리스트 버튼에서 포커스 제거
        
        fetchData('wait', selectedSchool, searchQuery);  // 데이터를 다시 로드
    });

    // 블랙리스트 버튼 클릭 시
    wbBlackBtn.addEventListener('click', function () {
        isWaitlist = false;
        wbBlackBtn.classList.add('focused');
        wbWaitBtn.classList.remove('focused');  // 대기리스트 버튼에서 포커스 제거
        
        fetchData('black', selectedSchool, searchQuery);  // 데이터를 다시 로드
    });

    // 학교 버튼 클릭 시 필터링
    schoolButtons.forEach(button => {
        button.addEventListener('click', function () {
            if (selectedSchool === this.textContent) {
                selectedSchool = '';  // 같은 학교 버튼을 다시 클릭하면 필터 해제
            } else {
                selectedSchool = this.textContent;  // 선택된 학교 업데이트
            }
            updateSchoolButtonFocus();
            const listType = isWaitlist ? 'wait' : 'black';  // 현재 상태에 따라 설정
            fetchData(listType, selectedSchool, searchQuery);  // 데이터를 다시 로드
        });
    });

    // 검색창 입력 시
    searchInput.addEventListener('input', function () {
        searchQuery = this.value.toLowerCase();  // 검색어 업데이트
        const listType = isWaitlist ? 'wait' : 'black';  // 현재 상태에 따라 설정
        fetchData(listType, selectedSchool, searchQuery);  // 데이터를 다시 로드
    });

    // 학교 버튼 포커스 업데이트
    function updateSchoolButtonFocus() {
        schoolButtons.forEach(btn => {
            // 버튼의 텍스트를 비교하여 포커스 상태를 설정
            if (btn.textContent === selectedSchool) {
                btn.classList.add('school-focused');
            } else {
                btn.classList.remove('school-focused');
            }
        });
    }

    // 데이터를 서버에서 가져오는 함수 (jQuery 사용)
    function fetchData(listType, selectedSchool, searchQuery) {
        const url = '/management/wait-blacklist/fetch/';  // URL 설정
        console.log('Fetching data with:', listType, selectedSchool, searchQuery);  // 디버깅 로그

        // AJAX 요청
        $.ajax({
            url: url,
            type: 'GET',
            dataType: 'json',
            data: {
                type: listType,  // 'wait' 또는 'black'
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

    // 삭제 함수
    function deleteEntry(listType, entryId) {
        if (confirm('정말 삭제하시겠습니까?')) {
            window.location.href = `/wait-blacklist/delete/${listType}/${entryId}/`;
        }
    }

    function renderTable(data) {
        console.log(data);  // 데이터를 확인
        tableBody.innerHTML = '';
        data.forEach(item => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td class="wb-td">${item.school}</td>
                <td class="wb-td">${item.grade}</td>
                <td class="wb-td">${item.name}</td>
                <td class="wb-td">${item.phone}</td>
                <td class="wb-td">${item.date}</td>
                <td class="wb-td">${item.note}</td>
            `;
            row.style.cursor = 'pointer';  
            row.onclick = () => {
                console.log('Navigating to:', item.list_type, item.id);  // 클릭 시 URL 디버깅
                const detailUrl = item.list_type === 'wait'
                    ? `/management/wait-blacklist/wait-detail/${item.id}/`
                    : `/management/wait-blacklist/black-detail/${item.id}/`;
                window.location.href = detailUrl;
            };
    
            tableBody.appendChild(row);
        });
    }
    
    

    // 초기 데이터 로드 (대기리스트)
    fetchData('wait', selectedSchool, searchQuery);
});
