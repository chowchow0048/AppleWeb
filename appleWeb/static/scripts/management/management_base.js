document.addEventListener('DOMContentLoaded', function() {
    updateTime();
    updateTimer();
    setInterval(updateTimer, 1000);
    setInterval(updateTime, 1000);
});


document.addEventListener('DOMContentLoaded', event => {
    // 양쪽 토글 버튼에 대한 이벤트 리스너 추가
    const sidebarToggle = document.querySelector('#sidebarToggle');
    const sidebarClose = document.querySelector('#sidebarClose');
    
    // 토글 기능을 함수로 분리
    const toggleSidebar = (event) => {
        event.preventDefault();
        document.body.classList.toggle('sb-sidenav-toggled');
    };
    
    // 양쪽 버튼에 같은 토글 기능 적용
    if (sidebarToggle) {
        sidebarToggle.addEventListener('click', toggleSidebar);
    }
    if (sidebarClose) {
        sidebarClose.addEventListener('click', toggleSidebar);
    }
    
    // 기존 시간 업데이트 코드는 그대로 유지
});

let sessionTime = 90 * 60;  // 90분을 초로 환산

function updateTimer() {
    const timerElement = document.getElementById('sessionTimer');
    if (!timerElement) return;

    let minutes = parseInt(sessionTime / 60, 10);
    let seconds = parseInt(sessionTime % 60, 10);

    minutes = minutes < 10 ? "0" + minutes : minutes;
    seconds = seconds < 10 ? "0" + seconds : seconds;

    timerElement.textContent = minutes + ":" + seconds;

    // 시간 감소
    sessionTime--;

    // 시간이 0 이하면 타이머를 멈추고 세션 만료 처리
    if (sessionTime < 0) {
        clearInterval(timerInterval);
        alert('세션 만료되었습니다. 다시 로그인 해주세요.');
        window.location = "{% url 'user_login' %}"; // 로그인 페이지로 리디렉션
    }
}

function updateTime() {
    const now = new Date();
    const year = now.getFullYear();
    const month = ('0' + (now.getMonth() + 1)).slice(-2);
    const date = ('0' + now.getDate()).slice(-2);
    const hours = ('0' + now.getHours()).slice(-2);
    const minutes = ('0' + now.getMinutes()).slice(-2);
    const day = now.toLocaleDateString('ko-KR', { weekday: 'long' });

    const formattedDate = `${year}-${month}-${date}`;
    const formattedTime = `${hours}:${minutes}`;
    const displayString = `${formattedDate} \t ${formattedTime} \t ${day}`;
    
    const dateDisplayElement = document.getElementById('date-display');
    if (dateDisplayElement) {
        dateDisplayElement.textContent = displayString;
    }
}