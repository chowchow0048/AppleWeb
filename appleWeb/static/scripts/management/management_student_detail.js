document.addEventListener('DOMContentLoaded', function() {
    setupPhoneEdit('phone');
    setupPhoneEdit('parent-phone');
});

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

function formatPhoneNumber(number) {
    if (number.length === 11) {
        return `${number.slice(0,3)}-${number.slice(3,7)}-${number.slice(7)}`;
    } else if (number.length === 10) {
        return `${number.slice(0,3)}-${number.slice(3,6)}-${number.slice(6)}`;
    }
    return number;
}

function toggleEditMode(isEdit, display, input, editBtn, actionBtns) {
    display.classList.toggle('hidden', isEdit);
    input.classList.toggle('hidden', !isEdit);
    editBtn.classList.toggle('hidden', isEdit);
    actionBtns.classList.toggle('hidden', !isEdit);
}

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

function getStudentId() {
    const pathParts = window.location.pathname.split('/');
    return pathParts[pathParts.length - 2];
}