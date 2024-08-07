console.log('스크립트 로드 확인: BASE');

document.addEventListener('DOMContentLoaded', function() {
    updateTime();
    updateTimer();
    setInterval(updateTimer, 1000);
    setInterval(updateTime, 1000);
});


document.addEventListener('DOMContentLoaded', event => {
    const sidebarToggle = document.body.querySelector('#sidebarToggle');
    if (sidebarToggle) {
        // Uncomment Below to persist sidebar toggle between refreshes
        if (localStorage.getItem('sb|sidebar-toggle') === 'true') {
            document.body.classList.toggle('sb-sidenav-toggled');
        }
        sidebarToggle.addEventListener('click', event => {
            event.preventDefault();
            document.body.classList.toggle('sb-sidenav-toggled');
            // console.log('CLICKED@@@@@@@');
            localStorage.setItem('sb|sidebar-toggle', document.body.classList.contains('sb-sidenav-toggled'));
        })
    }

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

// const seconds = ('0' + now.getSeconds()).slice(-2);