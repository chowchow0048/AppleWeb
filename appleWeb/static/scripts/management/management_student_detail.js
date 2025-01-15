document.addEventListener('DOMContentLoaded', function() {
    setupPhoneEdit('phone');
    setupPhoneEdit('parent-phone');
    setupCourseEdit();
});

//phone edit
function setupPhoneEdit(type) {
    const display = document.getElementById(`${type}-display`);
    const input = document.getElementById(`${type}-input`);
    const editBtn = document.getElementById(`${type}-edit-btn`);
    const actionBtns = document.getElementById(`${type}-action-btns`);
    
    editBtn.addEventListener('click', () => {
        display.classList.add('hidden');
        input.classList.remove('hidden');
        editBtn.classList.add('hidden');
        actionBtns.classList.remove('hidden');
        input.value = input.value.replace(/-/g, '');
    });
    
    const completeBtn = actionBtns.querySelector('.complete-btn');
    completeBtn.addEventListener('click', async () => {
        const phoneNumber = input.value;
        
        // 숫자만 입력 받도록 체크
        if (!/^\d{10,11}$/.test(phoneNumber)) {
            alert('올바른 전화번호 형식이 아닙니다.\n숫자 10-11자리만 입력해주세요.');
            return;
        }
        
        try {
            const response = await fetch('/management/student/update-phone/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({
                    student_id: getStudentId(),
                    phone_type: type,
                    phone_number: phoneNumber
                })
            });
            
            if (response.ok) {
                const formattedNumber = formatPhoneNumber(phoneNumber);
                display.textContent = formattedNumber;
                input.value = formattedNumber;
                toggleEditMode(false, display, input, editBtn, actionBtns);
            } else {
                alert('전화번호 업데이트에 실패했습니다.');
            }
        } catch (error) {
            console.error('Error:', error);
            alert('전화번호 업데이트 중 오류가 발생했습니다.');
        }
    });
    
    const cancelBtn = actionBtns.querySelector('.cancel-btn');
    cancelBtn.addEventListener('click', () => {
        toggleEditMode(false, display, input, editBtn, actionBtns);
        input.value = display.textContent.replace(/-/g, '');  // 원래 값으로 복구
    });
}

//phone edit
function formatPhoneNumber(number) {
    if (number.length === 11) {
        return `${number.slice(0,3)}-${number.slice(3,7)}-${number.slice(7)}`;
    } else if (number.length === 10) {
        return `${number.slice(0,3)}-${number.slice(3,6)}-${number.slice(6)}`;
    }
    return number;
}

//edit mode
function toggleEditMode(isEdit, display, input, editBtn, actionBtns) {
    display.classList.toggle('hidden', isEdit);
    input.classList.toggle('hidden', !isEdit);
    editBtn.classList.toggle('hidden', isEdit);
    actionBtns.classList.toggle('hidden', !isEdit);
}

//cookie
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

//student id
function getStudentId() {
    const pathParts = window.location.pathname.split('/');
    return pathParts[pathParts.length - 2];
}

// 전역 변수로 이동
let deletedCourses = [];

//course edit
function setupCourseEdit() {
    const display = document.getElementById('course-display');
    const editBtn = document.getElementById('course-edit-btn');
    const actionBtns = document.getElementById('course-action-btns');
    const addBtn = display.querySelector('.add-course-btn');
    
    editBtn.addEventListener('click', () => {
        // 수정 모드 시작할 때 배열 초기화
        deletedCourses = [];
        editBtn.classList.add('hidden');
        actionBtns.classList.remove('hidden');
        addBtn.classList.add('show');
        
        // 기존 과목들에 삭제 버튼 추가
        const courseItems = display.querySelectorAll('.course-item');
        courseItems.forEach(item => {
            // course-text가 있는 경우 (기존 과목)
            const courseText = item.querySelector('.course-text');
            if (courseText) {
                // 이미 삭제 버튼이 있는지 확인
                if (!courseText.querySelector('.delete-btn')) {
                    const deleteBtn = document.createElement('button');
                    deleteBtn.className = 'btn btn-danger delete-btn ms-2';
                    deleteBtn.textContent = '삭제';
                    courseText.appendChild(deleteBtn);
                    
                    // 삭제 버튼 이벤트 설정
                    deleteBtn.addEventListener('click', () => {
                        const courseId = item.dataset.courseId;
                        if (courseId) {
                            deletedCourses.push(courseId);
                        }
                        item.remove();
                    });
                }
                // course-text를 보이게 하고 course-edit는 숨김
                courseText.classList.remove('hidden');
                const courseEdit = item.querySelector('.course-edit');
                if (courseEdit) {
                    courseEdit.classList.add('hidden');
                }
            }
        });
    });

    addBtn.addEventListener('click', async () => {
        const userSchool = document.getElementById('user-school').value;
        const userGrade = document.getElementById('user-grade').value;
        console.log('[addBtn click] 현재 학생 정보:', { userSchool, userGrade });
        
        const newCourseItem = createNewCourseItem();
        addBtn.before(newCourseItem);
        await initializeCourseEdit(newCourseItem, userSchool, userGrade);
    });

    // 완료 버튼
    const completeBtn = document.getElementById('course-action-btns').querySelector('.complete-btn');
    completeBtn.addEventListener('click', async () => {
        console.log('[completeBtn] === 완료 버튼 클릭 ===');
        
        const studentId = getStudentId();
        console.log('1. 학생 ID:', studentId);
        console.log('2. 삭제될 과목 IDs:', deletedCourses);

        // 새로 추가된 과목 데이터 수집
        const newCourseItems = display.querySelectorAll('.course-item .course-edit');
        const updates = [];
        
        for (const item of newCourseItems) {
            const school = item.querySelector('.school-select')?.value;
            const grade = item.querySelector('.grade-select')?.value;
            const subject = item.querySelector('.subject-select')?.value;
            const day = item.querySelector('.day-select')?.value;
            const time = item.querySelector('.time-select')?.value;

            if (school && grade && subject && day && time) {
                updates.push({
                    school,
                    grade,
                    subject,
                    day,
                    time
                });
            }
        }

        // 서버로 전송할 데이터
        const requestData = {
            studentId: studentId,
            deletedCourses: deletedCourses,
            updates: updates
        };

        console.log('3. 서버로 전송할 데이터:', requestData);

        try {
            const response = await fetch('/management/student/update-courses/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify(requestData)
            });

            const result = await response.json();
            console.log('4. API 응답:', result);

            if (!response.ok) {
                alert(result.error || '과목 업데이트 중 오류가 발생했습니다.');
                return;
            }

            alert(result.message || '수강 과목이 업데이트되었습니다.');
            location.reload();
        } catch (error) {
            console.error('5. API 오류:', error);
            alert('과목 업데이트 중 오류가 발생했습니다.');
        }
    });

    // 취소 버튼
    const cancelBtn = actionBtns.querySelector('.cancel-btn');
    if (cancelBtn) {
        cancelBtn.addEventListener('click', () => {
            location.reload();
        });
    }
}

function createNewCourseItem() {
    const div = document.createElement('div');
    div.className = 'course-item';
    div.innerHTML = `
        <div class="course-edit">
            <div class="course-edit-row d-flex align-items-center">
                <select class="form-select school-select me-1">
                    <option value="">학교 선택</option>
                    ${['연합반', '세화고', '세화여고', '서울고'].map(school => 
                        `<option value="${school}">${school}</option>`
                    ).join('')}
                </select>
                <select class="form-select grade-select me-1">
                    <option value="">학년 선택</option>
                    ${['예비고1', '1학년', '2학년', '3학년'].map(grade => 
                        `<option value="${grade}">${grade}</option>`
                    ).join('')}
                </select>
                <select class="form-select subject-select me-1" disabled>
                    <option value="">과목 선택</option>
                </select>
                <select class="form-select day-select me-1" disabled>
                    <option value="">요일 선택</option>
                </select>
                <select class="form-select time-select me-1" disabled>
                    <option value="">시간 선택</option>
                </select>
                <button class="btn btn-danger delete-btn ms-auto">삭제</button>
            </div>
        </div>
    `;
    return div;
}

async function initializeCourseEdit(item, userSchool, userGrade) {
    const schoolSelect = item.querySelector('.school-select');
    const gradeSelect = item.querySelector('.grade-select');
    
    // 학생의 학교/학년으로 초기값 설정
    if (userSchool && userGrade) {
        console.log('[initializeCourseEdit] 학생 정보로 초기화:', { userSchool, userGrade });
        schoolSelect.value = userSchool;
        gradeSelect.value = userGrade;
        
        // 학교/학년이 설정되었으므로 과목 선택 활성화
        const subjectSelect = item.querySelector('.subject-select');
        subjectSelect.disabled = false;
        await loadSubjects(item, userSchool, userGrade);
    }
    
    // 삭제 버튼 설정
    setupDeleteButton(item);
    
    // 이벤트 리스너 설정
    setupSelectChangeHandlers(item);
}

function setupDeleteButton(item) {
    const deleteBtn = item.querySelector('.delete-btn');
    deleteBtn.addEventListener('click', () => {
        if (item.dataset.courseId) {
            deletedCourses.push(item.dataset.courseId);
        }
        item.remove();
    });
}

function validateCourses() {
    const courseItems = document.querySelectorAll('.course-item');
    const userSchool = document.getElementById('user-school').value;
    const userGrade = document.getElementById('user-grade').value;
    
    // 선택된 모든 과목을 저장할 Set
    const selectedCourses = new Set();

    for (const item of courseItems) {
        const school = item.querySelector('.school-select').value;
        const grade = item.querySelector('.grade-select').value;
        const subject = item.querySelector('.subject-select').value;
        const day = item.querySelector('.day-select').value;
        const time = item.querySelector('.time-select').value;

        // 학교와 학년 검사
        if (school !== userSchool) {
            alert('학생의 학교와 동일한 수업만 신청할 수 있습니다.');
            return false;
        }
        
        if (grade !== userGrade) {
            alert('학생의 학년과 동일한 수업만 신청할 수 있습니다.');
            return false;
        }

        // 중복 수업 검사
        const courseKey = `${subject}-${day}-${time}`;
        if (selectedCourses.has(courseKey)) {
            alert('동일한 수업을 중복해서 신청할 수 없습니다.');
            return false;
        }
        selectedCourses.add(courseKey);
    }
    return true;
}

async function populateSelects(item, school, grade) {
    const schoolSelect = item.querySelector('.school-select');
    const gradeSelect = item.querySelector('.grade-select');

    // 학교 옵션 설정
    const schools = ['연합반', '세화고', '세화여고', '서울고'];
    schoolSelect.innerHTML = '<option value="">학교 선택</option>';
    schools.forEach(s => {
        const option = document.createElement('option');
        option.value = s;
        option.textContent = s;
        schoolSelect.appendChild(option);
    });

    // 학년 옵션 설정
    const grades = ['예비고1', '1학년', '2학년', '3학년'];
    gradeSelect.innerHTML = '<option value="">학년 선택</option>';
    grades.forEach(g => {
        const option = document.createElement('option');
        option.value = g;
        option.textContent = g;
        gradeSelect.appendChild(option);
    });

    // 초기값 설정
    if (school) schoolSelect.value = school;
    if (grade) gradeSelect.value = grade;
}

async function loadSubjects(item, school, grade) {
    console.log('[loadSubjects] === 시작 ===');
    const select = item.querySelector('.subject-select');
    const currentValue = select.value;
    console.log('[loadSubjects] 1. 현재 값:', currentValue);
    
    select.disabled = false;
    
    try {
        const response = await fetch(`/management/api/available-subjects/?school=${school}&grade=${grade}`);
        const subjects = await response.json();
        console.log('[loadSubjects] 2. API로부터 받은 subjects:', subjects);
        
        select.innerHTML = '<option value="">과목 선택</option>';
        subjects.forEach(subject => {
            const option = document.createElement('option');
            option.value = subject;
            option.textContent = subjectTranslations[subject] || subject;
            select.appendChild(option);
        });
        
        console.log('[loadSubjects] 3. 옵션 설정 후 현재 값:', select.value);
        if (currentValue && Array.from(select.options).some(opt => opt.value === currentValue)) {
            select.value = currentValue;
            console.log('[loadSubjects] 4. 이전 값 복원:', currentValue);
        }
    } catch (error) {
        console.error('[loadSubjects] Error:', error);
    }
    console.log('[loadSubjects] === 종료 ===');
}

async function loadDays(item, school, grade, subject) {
    console.log('[loadDays] === 시작 ===');
    const select = item.querySelector('.day-select');
    const currentValue = select.value;
    console.log('[loadDays] 1. 현재 값:', currentValue);
    
    select.disabled = false;

    try {
        const response = await fetch(`/management/api/available-days/?school=${school}&grade=${grade}&subject=${subject}`);
        const days = await response.json();
        console.log('[loadDays] 2. API로부터 받은 days:', days);
        
        select.innerHTML = '<option value="">요일 선택</option>';
        days.forEach(day => {
            const option = document.createElement('option');
            option.value = day;
            option.textContent = day;
            select.appendChild(option);
        });
        
        console.log('[loadDays] 3. 옵션 설정 후 현재 값:', select.value);
        if (currentValue && Array.from(select.options).some(opt => opt.value === currentValue)) {
            select.value = currentValue;
            console.log('[loadDays] 4. 이전 값 복원:', currentValue);
        }
    } catch (error) {
        console.error('[loadDays] Error:', error);
    }
    console.log('[loadDays] === 종료 ===');
}

async function loadTimes(item, school, grade, subject, day) {
    console.log('[loadTimes] === 시작 ===');
    const select = item.querySelector('.time-select');
    const currentValue = select.value;
    console.log('[loadTimes] 1. 현재 값:', currentValue);
    
    select.disabled = false;

    try {
        const response = await fetch(`/management/api/available-times/?school=${school}&grade=${grade}&subject=${subject}&day=${day}`);
        const times = await response.json();
        console.log('[loadTimes] 2. API로부터 받은 times:', times);
        
        select.innerHTML = '<option value="">시간 선택</option>';
        times.forEach(time => {
            const option = document.createElement('option');
            option.value = time;  // '10:00' 형식 저장
            option.textContent = convertTimeFormatReverse(time.split(':')[0]);  // 표시는 '오전 10시' 형식
            select.appendChild(option);
        });
        
        console.log('[loadTimes] 3. 옵션 설정 후 현재 값:', select.value);
        if (currentValue && Array.from(select.options).some(opt => opt.value === currentValue)) {
            select.value = currentValue;
            console.log('[loadTimes] 4. 이전 값 복원:', currentValue);
        }
    } catch (error) {
        console.error('[loadTimes] Error:', error);
    }
    console.log('[loadTimes] === 종료 ===');
}

function setupSelectChangeHandlers(item) {
    const schoolSelect = item.querySelector('.school-select');
    const gradeSelect = item.querySelector('.grade-select');
    const subjectSelect = item.querySelector('.subject-select');
    const daySelect = item.querySelector('.day-select');

    // 학교/학년 변경 시
    schoolSelect.addEventListener('change', async () => {
        if (schoolSelect.value && gradeSelect.value) {
            subjectSelect.disabled = false;
            await loadSubjects(item, schoolSelect.value, gradeSelect.value);
        }
    });

    gradeSelect.addEventListener('change', async () => {
        if (schoolSelect.value && gradeSelect.value) {
            subjectSelect.disabled = false;
            await loadSubjects(item, schoolSelect.value, gradeSelect.value);
        }
    });

    // 과목 변경 시
    subjectSelect.addEventListener('change', async () => {
        if (subjectSelect.value) {
            daySelect.disabled = false;
            await loadDays(item, schoolSelect.value, gradeSelect.value, subjectSelect.value);
        }
    });

    // 요일 변경 시
    daySelect.addEventListener('change', async () => {
        if (daySelect.value) {
            const timeSelect = item.querySelector('.time-select');
            timeSelect.disabled = false;
            await loadTimes(item, schoolSelect.value, gradeSelect.value, subjectSelect.value, daySelect.value);
        }
    });

    // 시간 선택 변경 시
    const timeSelect = item.querySelector('.time-select');
    timeSelect.addEventListener('change', () => {
        const selectedData = {
            school: item.querySelector('.school-select').value,
            grade: item.querySelector('.grade-select').value,
            subject: item.querySelector('.subject-select').value,
            day: item.querySelector('.day-select').value,
            time: timeSelect.value
        };
        console.log('[timeSelect change] 선택된 값들:', selectedData);
    });
}

// 과목 한국어 매핑 객체
const subjectTranslations = {
    'integrated_science': '통합과학',
    'physics': '물리',
    'chemistry': '화학',
    'biology': '생명과학',
    'earth_science': '지구과학'
};

// 과목 영어-한글 매핑 객체
const subjectTranslationsReverse = {
    '통합과학': 'integrated_science',
    '물리': 'physics',
    '화학': 'chemistry',
    '생명과학': 'biology',
    '지구과학': 'earth_science'
};

function collectCourseUpdates() {
    // 모든 course-item을 선택
    const courseItems = document.querySelectorAll('.course-item');
    const updates = [];

    courseItems.forEach(item => {
        // 각 select 요소 가져오기
        const school = item.querySelector('.school-select').value;
        const grade = item.querySelector('.grade-select').value;
        const subject = item.querySelector('.subject-select').value;
        const day = item.querySelector('.day-select').value;
        const time = item.querySelector('.time-select').value;

        // 모든 필드가 채워져 있는지 확인
        if (school && grade && subject && day && time) {
            const update = {
                school: school,
                grade: grade,
                subject: subjectTranslationsReverse[subject] || subject, // 한글을 영어로 변환
                day: day,
                time: time
            };

            // 기존 과목 수정인 경우 courseId 추가
            if (item.dataset.courseId) {
                update.courseId = item.dataset.courseId;
            }

            updates.push(update);
        }
    });

    return updates;
}

// 시간 형식 변환 함수
function convertTimeFormat(timeStr) {
    const [period, hour] = timeStr.split(' ');  // '오전', '10시'
    const hourNum = parseInt(hour);
    
    if (period === '오전') {
        return hourNum < 10 ? `0${hourNum}:00` : `${hourNum}:00`;
    } else {
        return `${hourNum + 12}:00`;
    }
}

// 시간 역변환 함수 (API 응답 -> 표시용)
function convertTimeFormatReverse(time24h) {
    const hour = parseInt(time24h);
    if (hour < 12) {
        return `오전 ${hour}시`;
    } else if (hour === 12) {
        return `오후 12시`;
    } else {
        return `오후 ${hour - 12}시`;
    }
}