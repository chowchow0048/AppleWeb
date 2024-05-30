function confirmPayment(userId, school, grade, name, paymentCount) {
    const excessSessions = -paymentCount; // 초과 수업 횟수
    console.log(userId, school, grade, name, paymentCount);
    let paymentAmount; // 결제 금액
    let unitPrice; // 단위 금액

    if (grade === '1학년') {
        unitPrice = 39;
        paymentAmount = 39 + (paymentCount * (-39 / 4));
    } else {
        unitPrice = 117;
        paymentAmount = 117 + (paymentCount * (-117 / 12));
    }

    if (paymentCount < 0) {
        const message = `[학생정보] ${school} ${grade} ${name}\n` +
                        `[수업 초과 정보] 수업 초과 횟수: ${excessSessions}\n` +
                        `[최종 결제 금액] ${paymentAmount.toFixed(2)}만원\n\n` +
                        `결제를 진행하시겠습니까?`;

        if (confirm(message)) {
            processPayment(userId);
        }
    } else {
        alert('추가 결제 없이 진행됩니다.');
        processPayment(userId);
    }
}

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
        alert(data.message);
        location.reload();
    })
    .catch(error => console.error('Error:', error));
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